CHINESE_SIGN = ["rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse",
                "sheep", "monkey", "rooster", "dog", "pig"]

WESTERN_SIGN = [(20, "capricorn", "aquarius"), (19, "aquarius", "pisces"),
                (20, "pisces", "aries"), (20, "aries", "taurus"),
                (20, "taurus", "gemini"), (20, "gemini", "cancer"),
                (22, "cancer", "leo"), (22, "leo", "virgo"),
                (22, "virgo", "libra"), (22, "libra", "scorpio"),
                (21, "scorpio", "sagittarius"),
                (21, "sagittarius", "capricorn")]

def interpret_western_sign(day, month):
    if type(day, month) is not (int, int):
        print("Tup")
    else:
        sign = WESTERN_SIGN[month - 1]
        return sign[1] if day <= sign[0] else sign[2]


def interpret_chinese_sign(year):
    if type(year) is not int:
        print("Tup")
    else:
        return CHINESE_SIGN[(year - 4) % 12]


def interpret_both_signs(day, month, year):
    if type(day, month, year) is not (int, int, int):
        print("Tup")
    else:
        return (interpret_western_sign(day, month), interpret_chinese_sign(year))
