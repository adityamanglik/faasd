def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def handle(event, context):
    try:
        # Decode bytes to string
        body_str = event.body.decode().strip()

        # Convert to integer
        n = int(body_str)

        result = fib(n)
        response_body = f"Fibonacci({n}) = {result} from fib1"

        return {
            "statusCode": 200,
            "body": response_body
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": f"Invalid input. Please provide an integer. Error: {e}"
        }