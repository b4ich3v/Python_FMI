class ExceptionStore:
    def __init__(self):
        self.unhandled_exceptions = []
        self.exception = None

    def log_exception(self, exc_value, exc_type):
        self.unhandled_exceptions.append((exc_value, exc_type))
        self.exception = exc_value


class ProtectedSection(ExceptionStore):
    def __init__(self, log=(), suppress=()):
        if not all(issubclass(exc, Exception) for exc in log):
            raise TypeError("Must be exception types")
        if not all(issubclass(exc, Exception) for exc in suppress):
            raise TypeError("Must be exception types")

        super().__init__()
        self.log = log
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if exc_type in self.log:
                self.exception = exc_value
                return True
            elif exc_type in self.suppress:
                return True
            else:
                self.log_exception(exc_value, exc_type)
                return False
        return False
