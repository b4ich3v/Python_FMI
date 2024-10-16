def function_that_says_ni(*args, **kwargs):
    total_cost = 0.0
    unique_letters = set()
    variable_type = (int, float)
    types_of_shrubs = {"храст", "shrub", "bush"}

    for arg in args:
        if type(arg) is dict and "name" in arg:
            name_value = arg["name"].lower()
            if name_value not in types_of_shrubs:
                return "Ni!"
            if "cost" in arg:
                cost = arg["cost"]
                if type(cost) in variable_type and cost >= 0:
                    total_cost += round(cost, 2)
                else:
                    return "Ni!"
            else:
                continue

    for key, value in kwargs.items():
        if type(value) is dict and "name" in value:
            name_value = value["name"].lower()
            if name_value in types_of_shrubs:
                for letter in key:
                    unique_letters.add(letter)
            else:
                return "Ni!"
            if "cost" in value:
                cost = value["cost"]
                if type(cost) in variable_type and cost >= 0:
                    total_cost += round(cost, 2)
                else:
                    return "Ni!"
            else:
                continue

    if total_cost > 42.00:
        return "Ni!"

    integer_cost = int(total_cost)
    if integer_cost == 0 or len(unique_letters) % integer_cost != 0:
        return "Ni!"

    return f"{total_cost:.2f}лв"
