from collections import deque

# Response time tracker (last 10 Groq calls)
response_times = deque(maxlen=10)

def record_response_time(ms: int):
    """Record a Groq API response time."""
    response_times.append(ms)

def get_avg_response_time() -> float:
    """Return average of last 10 response times."""
    if not response_times:
        return 0.0
    return round(sum(response_times) / len(response_times), 2)

def get_response_times_count() -> int:
    """Return how many response times are tracked."""
    return len(response_times)