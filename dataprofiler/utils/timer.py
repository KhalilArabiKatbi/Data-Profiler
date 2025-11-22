import time


class Timer:
    def __init__(self, name: str = "task"):
        self.name = name
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end = time.perf_counter()
        return False

    def elapsed(self) -> float:
        if self.start is None:
            return 0.0
        end = self.end if self.end is not None else time.perf_counter()
        return float(end - self.start)