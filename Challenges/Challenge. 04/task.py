class LockPicker_OMI0600328:
    DEFAULT_VALUES = {
        int: 0,
        str: "",
        float: 0.0,
        bool: False,
        list: [],
        dict: {},
        set: set(),
        tuple: (),
        complex: complex(0, 0)
    }

    def __init__(self, lock):
        self.lock = lock
        self.attempted_args = set()

    def _handle_type_error(self, exc, args):
        if exc.position is None:
            expected_count = exc.expected
            return [None] * expected_count

        position = exc.position - 1
        expected_type = exc.expected
        
        if (position, expected_type) in self.attempted_args:
            return args
        
        args[position] = self.DEFAULT_VALUES.get(expected_type, None)
        self.attempted_args.add((position, expected_type))
        return args

    def _handle_value_error(self, ex, args):
        position = ex.position - 1
        expected_value = ex.expected
        args[position] = expected_value
        return args

    def unlock(self):
        args = []

        while True:
            try:
                if self.lock.pick(*args):
                    break
            except Exception as ex:
                if isinstance(ex, TypeError):
                    args = self._handle_type_error(ex, args)
                elif isinstance(ex, ValueError):
                    args = self._handle_value_error(ex, args)

