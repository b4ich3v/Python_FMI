def optimize_exception_check(attr_name):
    def decorator(func):
        def wrapper(self, exc_type):
            cache = getattr(self, attr_name)
            if exc_type in cache:
                return True

            result = func(self, exc_type)  # True or False
            if result:
                cache.add(exc_type)
            return result
        return wrapper
    return decorator


class ProtectedSection:
    __counter = 0

    def __init__(self, log=(), suppress=()):
        if log is not None:
            for exc in log:
                if not issubclass(exc, Exception):
                    raise TypeError("Not a valid exception type")

        if suppress is not None:
            for exc in suppress:
                if not issubclass(exc, Exception):
                    raise TypeError("Not a valid exception type")

        self._current_exception = None  # Saves the specific or last "updated" exception in case of reuse of an already created instance
        self.log_exceptions = set(log)
        self.suppress_exceptions = set(suppress)
        self._checked_exceptions_logs = set()  # Optimization to avoid checking one exception n times
        self._checked_exceptions_suppress = set()  # Optimization to avoid checking one exception n times
        self.exceptions_by_session = {}  # Dictionary to store exceptions with their session ID

    @optimize_exception_check("_checked_exceptions_logs")
    def is_exception_logged(self, exc_type):
        return exc_type in self.log_exceptions

    @optimize_exception_check("_checked_exceptions_suppress")
    def is_exception_suppressed(self, exc_type):
        return exc_type in self.suppress_exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if self.is_exception_logged(exc_type):
                self.exceptions_by_session[self.__counter] = exc_value
                self.__counter += 1
                self._current_exception = exc_value
                return True

            if self.is_exception_suppressed(exc_type):
                self._current_exception = None
                self.__counter += 1
                return True

        return False

    @property
    def exception(self):
        return self._current_exception

    @property
    def exceptions(self):
        return self.exceptions_by_session

    def get_exception_by_session(self, session_id):
        return self.exceptions_by_session.get(session_id, None)
