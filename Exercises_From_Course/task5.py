def lazy_super(rewrite_return):
    def decorator(func):
        def decorated(self, *args, **kwargs):
            func_result = func(self, *args, **kwargs)
            super_name = func.__name__
            super_result = getattr(super(self.__class__, self),
                                   super_name)(*args, **kwargs)
            return super_result if rewrite_return else func_result
        return decorated
    return decorator
