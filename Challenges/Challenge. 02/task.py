class HauntedMansion:
    HELPER = ("_data", "spooky_")

    def __init__(self, **kwargs):
        self._data = {}  # "protected"
        for key, value in kwargs.items():
            self._data[key] = value

    def __getattr__(self, name):
        if self._pref_validator(name):
            original_name = name[len(self.HELPER[1]):]
            if original_name in self._data:
                return self._data[original_name]
        return "Booooo, only ghosts here!"

    def __setattr__(self, name, value):
        if name == self.HELPER[0]:  # protect the actual data of the class
            object.__setattr__(self, name, value)  # prevents an endless cycle
        else:
            self._data[name] = value

    def _pref_validator(self, name):
        if len(name) < len(self.HELPER[1]):
            return False
        for i in range(len(self.HELPER[1])):
            if name[i] != self.HELPER[1][i]:
                return False
        return True
