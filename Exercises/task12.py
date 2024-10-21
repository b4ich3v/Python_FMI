def moneyForLili(n, x, p):
    starting_money = 10.00
    total = 0.00
    toys_received = 0

    for i in range(1, n + 1):
        if i % 2 == 1:
            toys_received += 1
        else:
            money_received = starting_money
            total += money_received
            total -= 1.00
            starting_money += 10.00

    total += toys_received * p

    if total >= x:
        print("Yes")
    else:
        print("No")


n = int(input())
x = float(input())
p = float(input())  

moneyForLili(n, x, p)


