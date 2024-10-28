def prepare_meal(number):
    if not isinstance(number, int):
        print("Tup")
    else:
        counter_for_three = 0
        counter_for_five = 0
        str = ""
        while number:
            if number % 3 == 0:
                number //= 3
                counter_for_three += 1
            elif number % 5 == 0:
                number //= 5
                counter_for_five += 1
            else:
                break
        for i in range(counter_for_three):
            str += "spam "
        if counter_for_five != 0 and counter_for_three != 0:
            str += "and "
        for i in range(counter_for_five):
            str += "eggs "
        return str
