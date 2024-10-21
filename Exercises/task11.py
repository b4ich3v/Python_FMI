def func(n, *args):
    list_of_procent = [0, 0, 0, 0, 0]

    for value in args:
        if value < 200:
            list_of_procent[0] += 1
        elif 200 <= value < 400:
            list_of_procent[1] += 1
        elif 400 <= value < 600:
            list_of_procent[2] += 1
        elif 600 <= value < 800:
            list_of_procent[3] += 1
        else:  # value >= 800
            list_of_procent[4] += 1

    if n > 0:
        list_of_procent = [round((count * 100) / n, 2) for count in list_of_procent]

    print(list_of_procent)

n = int(input())
args = []

for i in range(n):
    value = int(input())
    args.append(value)

func(n, *args)
