import re
import random

ALL_KIDS = {}
KID_INDEXES = {}
KID_LIST = []

class Kid(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, dict(attrs))

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
                    if Santa._instance is not None:
                        santa = Santa._instance
                        kid_index = KID_INDEXES[kid_id]
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
        ALL_KIDS[kid_id] = obj
        kid_index = len(KID_LIST)
        KID_LIST.append(obj)
        KID_INDEXES[kid_id] = kid_index
        return obj


class Santa:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            obj = super().__new__(cls)
            cls._instance = obj
            obj.xmas_count = 0
            obj.kid_birth_xmas = {}  # kid_id -> xmas_count when the kid was created
            obj.last_requests = {}  # kid_id -> last requested gift this year
            obj.requests_since_last_xmas = []

            obj.kid_naughty_mask = 0  # Bitmask for naughty kids
            obj.kids_requested_mask = 0  # Bitmask for kids who requested a gift this year

        return cls._instance

    def __init__(self):
        pass

    def __call__(self, kid, input_string):
        gift = self._get_gift(input_string)
        kid_id = id(kid)
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count

        self.requests_since_last_xmas.append((kid_id, gift))
        self.last_requests[kid_id] = gift
        kid_index = KID_INDEXES[kid_id]
        # Mark this kid as having requested a gift this year
        self.kids_requested_mask |= (1 << kid_index)

    def __matmul__(self, input_string):
        gift = self._get_gift(input_string)
        kid_id = self._get_kid_id_from_letter(input_string)
        kid = ALL_KIDS[kid_id]
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count

        self.requests_since_last_xmas.append((kid_id, gift))
        self.last_requests[kid_id] = gift
        kid_index = KID_INDEXES[kid_id]
        # Mark this kid as having requested a gift this year
        self.kids_requested_mask |= (1 << kid_index)

        return self

    def _get_gift(self, input_string):
        pattern = r'(["\'])([A-Za-z0-9 ]+)\1'
        match = re.search(pattern, input_string)
        if not match:
            raise ValueError("Error")
        return match.group(2).strip() # Removing this kind of symbols : "\t", "\n" ...

    def _get_kid_id_from_letter(self, input_string):
        for line in input_string.split('\n'):
            line_stripped = line.strip()
            if self._is_all_digits(line_stripped):
                kid_id = int(line_stripped)
                if kid_id in ALL_KIDS:
                    return kid_id
                else:
                    raise ValueError("Error")
        raise ValueError("Error")

    @staticmethod
    def _is_all_digits(input_string):
        if not input_string:
            return False  
        for current in input_string:
            if not ("0" <= current <= "9"):
                return False
        return True

    def __iter__(self):
        return (gift for (unused, gift) in self.requests_since_last_xmas)

    def xmas(self):
        if not self.requests_since_last_xmas:
            self._no_requests_this_year()
            return

        chosen_most_wanted = self._most_wanted_gift()
        self._deliver(chosen_most_wanted)
        self._reset()

    def _no_requests_this_year(self):
        self.xmas_count += 1
        self.kid_naughty_mask = 0
        self.last_requests.clear()
        self.kids_requested_mask = 0

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
        return random.choice(most_wanted) if most_wanted else None

    def _deliver(self, chosen_most_wanted):
        for kid_id, kid in ALL_KIDS.items():
            birth = self.kid_birth_xmas.get(kid_id, self.xmas_count)
            age = self.xmas_count - birth
            if age >= 6:
                continue
            kid_index = KID_INDEXES[kid_id]
            naughty = (self.kid_naughty_mask & (1 << kid_index)) != 0  # Checking if the child is naughty

            if kid_id in self.last_requests:
                gift = self.last_requests[kid_id]
                if naughty:
                    gift = "coal"
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
