from flask import Flask, request, Response
import requests
import itertools

app = Flask(__name__)

# List of faasd function URLs
backends = [
    "http://127.0.0.1:8080/function/fib1",
    "http://127.0.0.1:8080/function/fib2",
    "http://127.0.0.1:8080/function/fib3"
]

# Round-robin iterator
backend_iter = itertools.cycle(backends)

@app.route('/', methods=["GET", "POST"])
def proxy():
    target_url = next(backend_iter)

    raw_data = request.get_data(as_text=False)
    print(f"[PROXY DEBUG] Forwarding to {target_url}")
    print(f"[PROXY DEBUG] Body received: {raw_data}")

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key.lower() != 'host'},
            data=raw_data,
            cookies=request.cookies,
            allow_redirects=False
        )

        return Response(resp.content, resp.status_code, resp.headers.items())

    except requests.exceptions.RequestException as e:
        return Response(f"Error forwarding to backend: {e}", status=502)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
