import time

def wait_for_input_or_timeout(timeout):
    start_time = time.time()
    while True:
        # Check if input is available
        if input_available():
            user_input = input("Enter something: ")
            print("You entered:", user_input)
            break
        # Check if timeout has been reached
        elif time.time() - start_time >= timeout:
            print("Timeout reached.")
            break
        # Sleep for a short duration to avoid high CPU usage
        time.sleep(0.1)

def input_available():
    import sys
    import select

    # Check if input is ready
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

if __name__ == "__main__":
    timeout = 10  # Set the timeout to 10 seconds
    print(f"Waiting for input or {timeout} seconds timeout...")
    wait_for_input_or_timeout(timeout)
