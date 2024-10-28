signs = (
    ('Водолей', 20, (31, 29)),
    ('Риби', 19, (29, 31)),
    ('Овен', 21, (31, 30)),
    ('Телец', 21, (30, 31)),
    ('Близнаци', 21, (31, 30)),
    ('Рак', 21, (30, 31)),
    ('Лъв', 22, (31, 30)),
    ('Дева', 23, (30, 31)),
    ('Везни', 23, (31, 30)),
    ('Скорпион', 23, (30, 31)),
    ('Стрелец', 22, (31, 30)),
    ('Козирог', 22, (30, 31)),
)

def what_is_my_sign(day, month):
    if not isinstance(day, int) or not isinstance(month, int):
        print("Tup")
    elif day >= signs[month - 1][1]:
        current_day_1 = signs[month - 1][2][0]
        current_day_2 = signs[month - 1][2][1]
        if day > current_day_1 or day < current_day_2:
            print("Tup")
        return signs[month - 1][0]
    else:
        previous_month = month - 1
        return signs[previous_month - 1][0]
