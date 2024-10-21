def ivancho_living_budget(inherited_money, end_year):
    age = 18
    remaining_money = inherited_money

    for year in range(1800, end_year + 1):
        if year % 2 == 0:
            remaining_money -= 12000
        else:
            remaining_money -= 12000 + (50 * (age + (year - 1800)))

        if remaining_money < 0:
            return f"He will need {abs(remaining_money):.2f} dollars to survive."

    return f"Yes! He will live a carefree life and will have {remaining_money:.2f} dollars left."

inherited_money = float(input())
end_year = int(input())
print(ivancho_living_budget(inherited_money, end_year))
