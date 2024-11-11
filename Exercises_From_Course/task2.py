import time

class КуртолисайСе(Exception):
    pass

class Пустиняк:
    _global_cooldown = 3
    _global_last_called = 0

    def __init__(self):
        self._method_last_called = {}

    def _check_global_timer(self):
        if time.time() - Пустиняк._global_last_called < Пустиняк._global_cooldown:
            remaining = Пустиняк._global_cooldown - (time.time() - Пустиняк._global_last_called)
            raise КуртолисайСе(f"Запри се, баце, оста'ат още {remaining} секунди!")

    def _check_method_timer(self, method_name, cooldown):
        if method_name in self._method_last_called:
            elapsed_time = time.time() - self._method_last_called[method_name]
            
            if elapsed_time < cooldown:
                remaining = cooldown - elapsed_time
                raise КуртолисайСе(f"{method_name} - оста'ат още {remaining} секунди, баце!")

    @staticmethod
    def _update_global_timer():
        Пустиняк._global_last_called = time.time()

    def чекей(self, cooldown):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                self._check_method_timer(func.__name__, cooldown)
                self._method_last_called[func.__name__] = time.time()
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def ептем_чекай(self, func):
        def wrapper(self, *args, **kwargs):
            self._check_global_timer()
            Пустиняк._update_global_timer()
            return func(self, *args, **kwargs)
        return wrapper


баце = Пустиняк()

class Пустиняк:

    @баце.ептем_чекай
    def буай(self, target):
        print("Ела я да ти кажа, изклесяк такъв!")

    @баце.чекей(5)
    def юсни(self):
        print("Малиии баце, ке прекина от таз скоросмъртница, ама е на нерез!")

    @баце.ептем_чекай
    @баце.чекей(10)
    def дудни(self, target):
        print("От тебе по-голям абич не съм виждал!")
