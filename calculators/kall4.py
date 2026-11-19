class KalkulyatorStudenta:
    def __init__(self, dengi, dni):
        self.dengi = dengi
        self.dni = dni
        self.na_odin_den = 0

        self.eda = {
            "Доширак с говядиной": 65,
            "Роллтон в пакетике": 30,
            "Батон «Красная цена» + майонез": 55,
            "Пельмени «Каждый день» (из картона)": 130,
            "Сосиски «Дружная семейка»": 85,
            "Гречка без масла и соли": 40,
            "Энергетик «Флеш» по скидке": 60,
            "Шаурма на вокзале (королевский пир)": 260
        }

    def schitat_dnevnoi_byudzhet(self):
        if self.dni <= 0:
            return 0
        self.na_odin_den = self.dengi / self.dni
        return self.na_odin_den

    def status_vyzhivaniya(self):
        den = self.schitat_dnevnoi_byudzhet()
        if den <= 0:
            return "Праздник: ты уже труп, иди просить еду у соседей"
        if den < 70:
            return "Опасно: питаемся кипятком и солью, переходим на фотосинтез"
        if den < 200:
            return "Норм: режим жёсткой экономии, но до стипухи дотянешь"
        if den < 500:
            return "Хорошо: можно даже шикануть и купить сырок «Б. Ю. Александров»"
        if den >= 500:
            return "Олигарх общаги: можно угощать весь этаж"

    def raschet_edy(self):
        den = self.schitat_dnevnoi_byudzhet()
        dengi_dlya_rascheta = 1
        if den > 0:
            dengi_dlya_rascheta = den

        print("\n--- СКОЛЬКО ЕДЫ МОЖНО КУПИТЬ НА ДЕНЬ ---")
        for nazvanie, tsena in self.eda.items():
            shtuk_v_den = den / tsena

            if shtuk_v_den >= 1:
                print(nazvanie + " -> можно целых " + str(int(shtuk_v_den)) + " шт. в день!")
            else:
                skolko_nado_kopit = tsena / dengi_dlya_rascheta
                print(nazvanie + " -> не хватает, надо копить " + str(round(skolko_nado_kopit, 1)) + " дн.")


babki = float(input("Сколько денег осталось на карте (руб.): "))
skolko_dney = int(input("Сколько дней до стипендии или перевода от родителей: "))

student = KalkulyatorStudenta(babki, skolko_dney)

byudzhet = student.schitat_dnevnoi_byudzhet()

print("\n================ РЕЗУЛЬТАТ ================")
print("Твой бюджет на день: " + str(round(byudzhet, 2)) + " руб.")
print("Статус выживания: " + student.status_vyzhivaniya())
student.raschet_edy()
print("==========================================")
