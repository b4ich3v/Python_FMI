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
                    santa._mark_naughty(kid_index)  
                    raise
            return wrapper

        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                setattr(cls, attr_name, decorate_with_exception_handling(attr_value))

        return cls

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        kid_id = id(obj)
        Kid._all_kids[kid_id] = obj
        kid_index = Kid._next_index
        Kid._kid_list.append(obj)
        Kid._kid_indexes[kid_id] = kid_index
        Kid._next_index += 1

        Santa()._register_kid(obj)  # Register the kid with Santa

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
            self.kid_birth_xmas = {}  # Tracks the Christmas count when the kid was registered
            self.last_requests = {}  # Stores the last gift requested by each kid
            self.requests_since_last_xmas = []  # List of all requests since last Christmas
            self.kid_flags_mask = 0  # Bitmask to track kid statuses
            self.initialized = True

    def _mark_naughty(self, kid_index):
        self.kid_flags_mask |= (1 << (kid_index * 3))  

    def _is_naughty(self, kid_index):
        return bool(self.kid_flags_mask & (1 << (kid_index * 3)))

    def _mark_requested(self, kid_index):
        self.kid_flags_mask |= (1 << (kid_index * 3 + 1))  

    def _is_requested(self, kid_index):
        return bool(self.kid_flags_mask & (1 << (kid_index * 3 + 1)))

    def _set_age_flag(self, kid_index, is_over_age):
        if is_over_age:
            self.kid_flags_mask &= ~(1 << (kid_index * 3 + 2))  
        else:
            self.kid_flags_mask |= (1 << (kid_index * 3 + 2))  

    def _is_over_age(self, kid_index):
        return not bool(self.kid_flags_mask & (1 << (kid_index * 3 + 2)))

    def _register_kid(self, kid):
        kid_id = id(kid)
        if kid_id not in self.kid_birth_xmas:
            # Register the kid's birth Christmas
            self.kid_birth_xmas[kid_id] = self.xmas_count
            kid_index = Kid._kid_indexes[kid_id]
            self._set_age_flag(kid_index, is_over_age=False)

    def __call__(self, kid, input_string):
        gift = self._get_gift(input_string)
        kid_id = id(kid)
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count  # Register the kid if not already registered

        self.requests_since_last_xmas.append((kid_id, gift))  # Add the request to the lists
        self.last_requests[kid_id] = gift
        kid_index = Kid._kid_indexes[kid_id]
        self._mark_requested(kid_index) 

    def __matmul__(self, input_string):
        gift = self._get_gift(input_string)
        kid_id = self._get_kid_id_from_letter(input_string)
        kid = Kid._all_kids[kid_id]
        if kid_id not in self.kid_birth_xmas:
            self.kid_birth_xmas[kid_id] = self.xmas_count  # Register the kid if not already registered

        self.requests_since_last_xmas.append((kid_id, gift))  # Add the request to the lists
        self.last_requests[kid_id] = gift
        kid_index = Kid._kid_indexes[kid_id]
        self._mark_requested(kid_index)  

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
            kid_index = Kid._kid_indexes[kid_id]

            if age >= self.AGE_LIMIT:
                self._set_age_flag(kid_index, is_over_age=True)  # Mark the kid as over age and skip delivery
                continue
            else:
                self._set_age_flag(kid_index, is_over_age=False)  # Reset the age flag if kid is not over age

            naughty = self._is_naughty(kid_index)  

            if kid_id in self.last_requests:
                gift = self.last_requests[kid_id]
            else:
                gift = chosen_most_wanted
                if gift is None:
                    continue

            if naughty:
                gift = "coal"

            kid(gift)  

    def _reset(self):
        # Reset the state for the next Christmas
        self.xmas_count += 1
        self.requests_since_last_xmas.clear()
        self.last_requests.clear()
        self.kid_flags_mask = 0  
