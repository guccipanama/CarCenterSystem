import time


class LoginAttemptTracker:
    def __init__(self, max_attempts=3, lock_time=60):
        self.max_attempts = max_attempts
        self.lock_time = lock_time
        self.attempts = 0
        self.locked_until = None

    def reset(self):
        self.attempts = 0
        self.locked_until = None

    def is_locked(self):
        if self.locked_until and time.time() < self.locked_until:
            return True
        return False

    def register_failed_attempt(self):
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.locked_until = time.time() + self.lock_time

    def can_attempt(self):
        if self.is_locked():
            return False
        return True