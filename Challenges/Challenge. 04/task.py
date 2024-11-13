class LockPicker_0MI0600328:
    DEFAULT_VALUES = {
        int: int(),
        str: str(),
        float: float(),
        bool: bool(),
        list: list(),
        dict: dict(),
        set: set(),
        tuple: tuple(),
        complex: complex()
    }

    def __init__(self, lock):
        self.lock = lock
        self.args = []

    def _handle_type_error(self, exc):
        if exc.position is None:
            return [None] * exc.expected

        args_copy = self.args[:]
        position = exc.position - 1
        expected_type = exc.expected

        args_copy[position] = self.DEFAULT_VALUES.get(expected_type, None)
        return args_copy

    def _handle_value_error(self, exc):
        args_copy = self.args[:]
        position = exc.position - 1
        expected_value = exc.expected

        args_copy[position] = expected_value
        return args_copy

    def unlock(self):
        while True:
            try:
                if self.lock.pick(*self.args):
                    break
            except TypeError as exc:
                self.args = self._handle_type_error(exc)
            except ValueError as exc:
                self.args = self._handle_value_error(exc)

