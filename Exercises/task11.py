def func(n, *args):
    listOfProcent = [0, 0, 0, 0, 0]

    for value in args:
        if value < 200:
            listOfProcent[0] += 1
        elif 200 <= value < 400:
            listOfProcent[1] += 1
        elif 400 <= value < 600:
            listOfProcent[2] += 1
        elif 600 <= value < 800:
            listOfProcent[3] += 1
        else:  # value >= 800
            listOfProcent[4] += 1

    if n > 0:
        listOfProcent = [round((count * 100) / n, 2) for count in listOfProcent]

    print(listOfProcent)

n = int(input())
args = []

for i in range(n):
    value = int(input())
    args.append(value)

func(n, *args)
