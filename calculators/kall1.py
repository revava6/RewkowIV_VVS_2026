chislo1 = float(input("vvedi chislo 1: "))
znak = input("znak: ")
chislo2 = float(input("vvedi chislo 2: "))

otvet = 0

if znak == '+':
    otvet = chislo1 + chislo2
    print("otvet poluchilsya: " + str(otvet))

if znak == '-':
    otvet = chislo1 - chislo2
    print("otvet poluchilsya: " + str(otvet))

if znak == '*':
    otvet = chislo1 * chislo2
    print("otvet poluchilsya: " + str(otvet))

if znak == '/':
    if chislo2 == 0:
        print("na nol delit nelzya durak")
    if chislo2 != 0:
        otvet = chislo1 / chislo2
        print("otvet poluchilsya: " + str(otvet))
