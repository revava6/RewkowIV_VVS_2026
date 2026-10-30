def poschitat_vsyo():
    c1 = input("chislo odin: ")
    c2 = input("chislo dva: ")
    z = input("znachok (+ - * /): ")
    c1 = float(c1)
    c2 = float(c2)
    
    if z == '+':
        r = c1 + c2
    elif z == '-':
        r = c1 - c2
    elif z == '*':
        r = c1 * c2
    elif z == '/':
        if c2 != 0:
            r = c1 / c2
        else:
            r = "nelzya delit na 0!!!"
    else:
        r = "neponyatno"
    return r

flag = True
while flag == True:
    itog = poschitat_vsyo()
    print("REZULTAT: ", itog)
    
    eshe = input("eshe schetat budesh? (da/net): ")
    if eshe == "net" or eshe == "n" or eshe == "NO" or eshe == "Net" or eshe == "не":
        print("poka")
        flag = False
        break
    else:
        pass
