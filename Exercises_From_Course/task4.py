def optimizer(func):
    memory = {}
    def wrapper(arg):
        if arg in memory:
            return memory[arg]

        result = func(arg)
        memory[arg] = result
        return result
    return wrapper

@optimizer
def fibonacci(x):
    if x in (0, 1):
        return 1
    return fibonacci(x - 1) + fibonacci(x - 2)
