class KalkulyatorStudenta:
    def __init__(self, dengi, dni):
        # zapominaem peremennye vnutri klassa cherez self
        self.dengi = dengi
        self.dni = dni
        self.na_odin_den = 0
        
        # tseny na studencheskuyu edu (v rublyah)
        self.eda = {
            "Doshirak s govyadinoi": 65,
            "Rollton v paketike": 30,
            "Baton 'Krasnaya tsena' + mayonez": 55,
            "Pelmeni 'Kazhdyi den' (iz kartona)": 130,
            "Sosiski 'Druzhnaya semeyka'": 85,
            "Grechka bez masla i soli": 40,
            "Energetik 'Flash' po skeedke": 60,
            "Shaurma na vokzale (korolevskiy pir)": 260
        }

    def schitat_dnevnoi_byudzhet(self):
        if self.dni <= 0:
            return 0
        self.na_odin_den = self.dengi / self.dni
        return self.na_odin_den

    def status_vyzhivaniya(self):
        den = self.schitat_dnevnoi_byudzhet()
        if den <= 0:
            return "Prazdnik: ty uzhe trup, idi prosit edu u sosedey"
        if den < 70:
            return "Opasno: pitaemsya kipyatkom i solyu, perehodim na fotosintez"
        if den < 200:
            return "Norm: rezhym zhyostkoy ekonomii, no do stipuhi dotyanesh"
        if den < 500:
            return "Horosho: mozhno dazhe zhiravat i kupit syrok 'B.Yu. Aleksandrov'"
        if den >= 500:
            return "Oligarh obshagi: mozhno ugoshchat ves etazh"

    def raschet_edy(self):
        den = self.schitat_dnevnoi_byudzhet()
        print("\n--- SKOLKO EDY TY MOZHESH POEST NA SUTKI: ---")
        for nazvanie in self.eda:
            tsena = self.eda[nazvanie]
            shtuk_v_den = den / tsena
            # kleim stroki cherez plyusy
            if shtuk_v_den >= 1:
                print(nazvanie + " -> mozhno tselih " + str(int(shtuk_v_den)) + " shtuk v den!")
            else:
                skolko_nado_kopit = tsena / (den if den > 0 else 1)
                print(nazvanie + " -> ne hvataet, nado kopit " + str(round(skolko_nado_kopit, 1)) + " dney")


# === OSNOVNAYA PROGRAMMA ===

babki = float(input("Skolko deneg na karte ostalos (rub): "))
skolko_dney = int(input("Skolko dney do stipuhi / roditeley: "))

# sozdayom obyekt klassa (kopiruem shablon v peremennuyu)
student = KalkulyatorStudenta(babki, skolko_dney)

byudzhet = student.schitat_dnevnoi_byudzhet()

print("\n================ REZULTAT ================")
print("Tvoi byudzhet na den: " + str(round(byudzhet, 2)) + " rubley")
print("Status vyzhivaniya: " + student.status_vyzhivaniya())
student.raschet_edy()
print("==========================================")
