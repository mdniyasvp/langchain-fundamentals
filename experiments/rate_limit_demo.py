import time
from collections import deque


class SlidingWindowRateLimiter:

    def __init__(self, max_requests, window_seconds):

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times = deque()

    def acquire(self):

        now = time.monotonic()

        # Remove expired request timestamps
        while (
            self.request_times
            and now - self.request_times[0] >= self.window_seconds
        ):
            self.request_times.popleft()

        # Wait if request limit is reached
        if len(self.request_times) >= self.max_requests:

            wait_time = (
                self.window_seconds
                - (now - self.request_times[0])
            )

            print(
                f"Rate limit reached. "
                f"Waiting {wait_time:.2f} seconds..."
            )

            time.sleep(wait_time)

            return self.acquire()

        # Record the new request
        self.request_times.append(time.monotonic())

        print(
            f"Request allowed. "
            f"Requests in window: {len(self.request_times)}"
        )


# Allow 3 requests in 5 seconds
limiter = SlidingWindowRateLimiter(
    max_requests=3,
    window_seconds=5
)


# Simulate 5 requests
for i in range(1, 6):

    print(f"\nRequest {i}")

    limiter.acquire()

    print("API request executed.")