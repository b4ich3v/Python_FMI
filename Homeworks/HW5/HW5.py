import re

class Kid(type):
    _all_kids = {}
    _kid_indexes = {}
    _kid_list = []
    _next_index = 0

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if "__call__" not in attrs:
            has_call = any(hasattr(base, "__call__") for base in bases)
            if not has_call:
                raise NotImplementedError("Bruhhh")

        def decorate_with_exception_handling(method):
            def wrapper(self, *args, **kwargs):
                kid_id = id(self)
                try:
                    return method(self, *args, **kwargs)
                except Exception:
                    santa = Santa()
                    kid_index = Kid._kid_indexes[kid_id]
                    santa.kid_naughty_mask |= (1 << kid_index)  # Marking the kid as naughty
                    raise
            return wrapper

        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                setattr(cls, attr_name, decorate_with_exception_handling(attr_value))

        return cls

    def __call__(cls, *args, **kwargs):
        # Register a new kid instance globally
        obj = super().__call__(*args, **kwargs)
        kid_id = id(obj)
        Kid._all_kids[kid_id] = obj
        kid_index = Kid._next_index
        Kid._kid_list.append(obj)
        Kid._kid_indexes[kid_id] = kid_index
        Kid._next_index += 1

        Santa().register_kid(obj)
        
        return obj


class Santa:
    _instance = None
    AGE_LIMIT = 5  

    def __new__(cls):
        if cls._instance is None:
            obj = super().__new__(cls)
            cls._instance = obj
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.xmas_count = 0
            self.kid_birth_xmas = {}  # kid_id - xmas_count when the kid was created
            self.last_requests = {}  # kid_id - last requested gift this year
            self.requests_since_last_xmas = []
            self.kid_naughty_mask = 0  # Bitmask for naughty kids
            self.kids_requested_mask = 0  # Bitmask for kids who requested a gift this year
            self.initialized = True

    def register_kid(self, kid):
        kid_id = id(kid)
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count

    def __call__(self, kid, input_string):
        gift = self._get_gift(input_string)
        kid_id = id(kid)
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count

        self.requests_since_last_xmas.append((kid_id, gift))
        self.last_requests[kid_id] = gift
        kid_index = Kid._kid_indexes[kid_id]
        # Mark this kid as having requested a gift this year
        self.kids_requested_mask |= (1 << kid_index)

    def __matmul__(self, input_string):
        gift = self._get_gift(input_string)
        kid_id = self._get_kid_id_from_letter(input_string)
        kid = Kid._all_kids[kid_id]
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count

        self.requests_since_last_xmas.append((kid_id, gift))
        self.last_requests[kid_id] = gift
        kid_index = Kid._kid_indexes[kid_id]
        # Mark this kid as having requested a gift this year
        self.kids_requested_mask |= (1 << kid_index)

        return self

    def _get_gift(self, input_string):
        pattern = r'(["\'])([A-Za-z0-9 ]+)\1'
        match = re.search(pattern, input_string)
        if not match:
            raise ValueError("Error")
        return match.group(2)

    def _get_kid_id_from_letter(self, input_string):
        match = re.search(r'^\s*(\d+)\s*$', input_string, re.MULTILINE)
        if match:
            kid_id = int(match.group(1))
            if kid_id in Kid._all_kids:
                return kid_id
        raise ValueError("Error")

    def __iter__(self):
        return iter(self.last_requests.values())

    def xmas(self):
        if not self.requests_since_last_xmas:
            self._reset()
            return

        chosen_most_wanted = self._most_wanted_gift()
        self._deliver(chosen_most_wanted)
        self._reset()

    def _most_wanted_gift(self):
        if not self.last_requests:
            return None

        gift_counts = {}
        for gift in self.last_requests.values():
            gift_counts[gift] = gift_counts.get(gift, 0) + 1

        if not gift_counts:
            return None

        max_count = max(gift_counts.values())
        most_wanted = [g for g, c in gift_counts.items() if c == max_count]
        return most_wanted[0] if most_wanted else None  

    def _deliver(self, chosen_most_wanted):
        for kid_id, kid in Kid._all_kids.items():
            birth = self.kid_birth_xmas.get(kid_id, self.xmas_count)
            age = self.xmas_count - birth
            if age >= self.AGE_LIMIT:
                continue
            kid_index = Kid._kid_indexes[kid_id]
            naughty = (self.kid_naughty_mask & (1 << kid_index)) != 0  # Checking if the child is naughty

            if kid_id in self.last_requests:
                gift = self.last_requests[kid_id]
            else:
                gift = chosen_most_wanted
                if gift is None:
                    continue

            if naughty:
                gift = "coal"

            kid(gift)  # Call the kid with the chosen gift

    def _reset(self):
        # Reset state for the next year
        self.xmas_count += 1
        self.requests_since_last_xmas.clear()
        self.last_requests.clear()
        self.kid_naughty_mask = 0
        self.kids_requested_mask = 0
