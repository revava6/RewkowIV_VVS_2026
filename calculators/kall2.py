otvetik = 0

def plus(x, y):
    global otvetik
    otvetik = x + y
    return otvetik

def minus(pervoe, vtoroe):
    rez = pervoe - vtoroe
    return rez

def umnozh(a, b):
    c = a * b
    return c

def delenie(chisloA, chisloB):
    if chisloB == 0:
        return "oshibka nol"
    else:
        d = chisloA / chisloB
        return d

nomer1 = float(input("chislo 1: "))
deystvie = input("deystvie (+, -, *, /): ")
nomer2 = float(input("chislo 2: "))

if deystvie == "+":
    print("Resultat: ", plus(nomer1, nomer2))
elif deystvie == "-":
    print("Resultat: ", minus(nomer1, nomer2))
elif deystvie == "*":
    print("Resultat: ", umnozh(nomer1, nomer2))
elif deystvie == "/":
    print("Resultat: ", delenie(nomer1, nomer2))
else:
    print("chto-to poshlo ne tak...")
