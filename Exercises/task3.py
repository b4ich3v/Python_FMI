def marko_polo():
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print("МаркоПоло")
        elif i % 3 == 0:
            print("Марко")
        elif i % 5 == 0:
            print("Поло")
        else:
            print(i)
