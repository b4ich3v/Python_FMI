def optimize_exception_check_for_logs(func):
    def wrapper(self, exc_type):
        if exc_type in self._checked_exceptions_logs:
            return self._checked_exceptions_logs[exc_type]

        result = func(self, exc_type) # 1 or 0
        self._checked_exceptions_logs[exc_type] = result

        return result
    return wrapper

def optimize_exception_check_for_suppress(func):
    def wrapper(self, exc_type):
        if exc_type in self._checked_exceptions_suppress:
            return self._checked_exceptions_suppress[exc_type]

        result = func(self, exc_type) # 1 or 0
        self._checked_exceptions_suppress[exc_type] = result

        return result
    return wrapper


class ProtectedSection:
    def __init__(self, log=(), suppress=()):
        if log is not None:
            for exc in log:
                if not issubclass(exc, Exception):
                    raise TypeError("Not a valid exception type")

        if suppress is not None:
            for exc in suppress:
                if not issubclass(exc, Exception):
                    raise TypeError("Not a valid exception type")

        self.log_exceptions = log
        self.suppress_exceptions = suppress
        self.exception = None
        self._checked_exceptions_logs = {}  # Optimization to avoid checking one exception n times
        self._checked_exceptions_suppress = {} # Optimization to avoid checking one exception n times

    @optimize_exception_check_for_logs
    def is_exception_logged(self, exc_type):
        return exc_type in self.log_exceptions

    @optimize_exception_check_for_suppress
    def is_exception_suppressed(self, exc_type):
        return exc_type in self.suppress_exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if self.is_exception_logged(exc_type):
                self.exception = exc_value
                return True

            if self.is_exception_suppressed(exc_type):
                self.exception = None
                return True

        return False
