class ExceptionStore:
    def __init__(self):
        self.all_exceptions = []
        self.exception = None

    def log_exception(self, exc_value, exc_type):
        self.all_exceptions.append((exc_value, exc_type))
        self.exception = exc_value


class ProtectedSection(ExceptionStore):
    def __init__(self, log=(), suppress=()):
        if not all(isinstance(exc, type) and issubclass(exc, BaseException) for exc in log):
            raise TypeError("Мust be exception types")
        if not all(isinstance(exc, type) and issubclass(exc, BaseException) for exc in suppress):
            raise TypeError("Мust be exception types")

        super().__init__()
        self.log = log
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if any(issubclass(exc_type, log_exc) for log_exc in self.log):
                self.exception = exc_value
                return True
            elif any(issubclass(exc_type, suppress_exc) for suppress_exc in self.suppress):
                self.exception = exc_value
                return True
            else:
                self.log_exception(exc_value, exc_type)
                return False
        return False
