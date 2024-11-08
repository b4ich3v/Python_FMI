class ProtectedSection:
    def __init__(self, log=(), suppress=()):
        self.log = log
        self.suppress = suppress
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if any(issubclass(exc_type, log_exc) for log_exc in self.log):
                self.exception = exc_value
                return True
            elif any(issubclass(exc_type, suppress_exc) for suppress_exc in self.suppress):
                return True
        return False
