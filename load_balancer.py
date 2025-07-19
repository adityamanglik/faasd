from flask import Flask, request, Response
import requests
import itertools

app = Flask(__name__)

# List of faasd function URLs
backends = [
    "http://127.0.0.1:8080/function/goll1",
    "http://127.0.0.1:8080/function/goll2",
    "http://127.0.0.1:8080/function/goll3"
]

request_counter = 0

@app.route('/', methods=["GET", "POST"])
def proxy():
    global request_counter
    index = request_counter % len(backends)
    print(f"[PROXY DEBUG] Request counter: {request_counter}, forwarding to backend index: {index}")
    target_url = backends[index]
    # Reset counter every 1000 requests to prevent overflow
    request_counter = (request_counter + 1) % 1000
    print(f"[PROXY DEBUG] Forwarding request to: {target_url}")
    raw_data = request.get_data(as_text=False)
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key.lower() != 'host'},
            data=raw_data,
        )
        
        # Parse and format specific fields from JSON response
        try:
            import json
            response_text = resp.text
            # Try to find and parse JSON in the response
            json_start = response_text.find('{')
            if json_start != -1:
                json_part = response_text[json_start:]
                json_end = json_part.find('}') + 1
                json_str = json_part[:json_end]
                
                data = json.loads(json_str)
                
                # Extract the fields you want
                metrics = {
                    "executionTime": data.get("executionTime", "N/A"),
                    "heapAlloc": data.get("heapAlloc", "N/A"), 
                    "NextGC": data.get("NextGC", "N/A"),
                    "NumGC": data.get("NumGC", "N/A"),
                    "containerId": data.get("containerId", "N/A")
                }
                print(metrics)
                
            else:
                print(f"[PROXY DEBUG] Response Text: {response_text}")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[PROXY DEBUG] Could not parse JSON response: {e}")
            print(f"[PROXY DEBUG] Response Text: {resp.text}")
        except UnicodeDecodeError:
            print(f"[PROXY DEBUG] Response contains binary data, length: {len(resp.content)} bytes")
        
        return Response(resp.content, resp.status_code, resp.headers.items())
        
    except requests.exceptions.RequestException as e:
        print(f"[PROXY ERROR] Error forwarding to backend: {e}")
        return Response(f"Error forwarding to backend: {e}", status=502)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)