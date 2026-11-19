def poschitat_vsyo():
    c1 = input("Первое число: ")
    c2 = input("Второе число: ")
    z = input("Знак (+, -, *, /): ")
    c1 = float(c1)
    c2 = float(c2)

    if z == '+':
        return c1 + c2
    if z == '-':
        return c1 - c2
    if z == '*':
        return c1 * c2
    if z == '/':
        if c2 == 0:
            return "На ноль делить нельзя!"
        return c1 / c2
    return "Неизвестный знак."


while True:
    print("Результат:", poschitat_vsyo())

    eshe = input("Ещё считать? (да/нет): ").strip().lower()
    if eshe in ("нет", "н", "не", "net", "n", "no"):
        print("Пока!")
        break
