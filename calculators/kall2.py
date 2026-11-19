def plus(x, y):
    return x + y


def minus(pervoe, vtoroe):
    return pervoe - vtoroe


def umnozh(a, b):
    return a * b


def delenie(chisloA, chisloB):
    if chisloB == 0:
        return "На ноль делить нельзя!"
    return chisloA / chisloB


nomer1 = float(input("Первое число: "))
deystvie = input("Действие (+, -, *, /): ")
nomer2 = float(input("Второе число: "))

if deystvie == "+":
    print("Результат:", plus(nomer1, nomer2))
elif deystvie == "-":
    print("Результат:", minus(nomer1, nomer2))
elif deystvie == "*":
    print("Результат:", umnozh(nomer1, nomer2))
elif deystvie == "/":
    print("Результат:", delenie(nomer1, nomer2))
else:
    print("Что-то пошло не так...")
