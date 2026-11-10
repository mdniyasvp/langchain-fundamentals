import time
import random


# Simulate a temporary API failure
class TransientAPIError(Exception):
    pass


# Simulated external API
attempt_counter = 0


def mock_external_api():

    global attempt_counter
    attempt_counter += 1

    print(f"API attempt: {attempt_counter}")

    # Fail on first two attempts
    if attempt_counter <= 2:
        raise TransientAPIError(
            "Temporary server error (503)"
        )

    return "API request successful!"


# Retry configuration
MAX_RETRIES = 3
INITIAL_DELAY = 0.5
BACKOFF_FACTOR = 2
MAX_DELAY = 5
JITTER = 0.2


def call_with_retry():

    for attempt in range(MAX_RETRIES + 1):

        try:
            result = mock_external_api()

            print("SUCCESS:", result)
            return result

        except TransientAPIError as error:

            if attempt == MAX_RETRIES:
                print("ERROR: Maximum retries reached.")
                raise

            delay = min(
                INITIAL_DELAY * (BACKOFF_FACTOR ** attempt),
                MAX_DELAY
            )

            # Add random jitter
            delay += random.uniform(0, JITTER)

            print("ERROR:", error)
            print(f"Retrying after {delay:.2f} seconds...")

            time.sleep(delay)


if __name__ == "__main__":
    call_with_retry()