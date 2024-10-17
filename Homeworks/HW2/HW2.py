def function_that_says_ni(*args, **kwargs):
    total_cost = 0.0
    unique_letters = set()
    variable_type = (int, float)
    types_of_shrubs = {"храст", "shrub", "bush"}

    def check_item(element):
        if "name" not in element or type(element["name"]) is not str:
            return False
        name_value = element["name"].lower()
        if name_value not in types_of_shrubs:
            return False
        if "cost" in element:
            cost = element["cost"]
            if type(cost) not in variable_type or cost < 0:
                return False
        return True

    def add_cost(element):
        if "cost" in element:
            return round(element["cost"], 2)
        return 0.0

    for arg in args:
        if type(arg) is dict and check_item(arg):
            total_cost += add_cost(arg)
        else:
            return "Ni!"

    for key, value in kwargs.items():
        if type(key) is not str:
            return "Ni!"
        if type(value) is dict and check_item(value):
            unique_letters.update(letter for letter in key if letter.islower() or letter == '_')
            total_cost += add_cost(value)
        else:
            return "Ni!"

    if total_cost > 42.00:
        return "Ni!"

    integer_cost = int(total_cost)
    if integer_cost == 0 or len(unique_letters) % integer_cost != 0:
        return "Ni!"

    return f"{total_cost:.2f}лв"
