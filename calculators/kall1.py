chislo1 = float(input("Введи первое число: "))
znak = input("Знак (+, -, *, /): ")
chislo2 = float(input("Введи второе число: "))

otvet = None

if znak == '+':
    otvet = chislo1 + chislo2
elif znak == '-':
    otvet = chislo1 - chislo2
elif znak == '*':
    otvet = chislo1 * chislo2
elif znak == '/':
    if chislo2 == 0:
        print("На ноль делить нельзя!")
    else:
        otvet = chislo1 / chislo2

if otvet is not None:
    print("Ответ:", otvet)
