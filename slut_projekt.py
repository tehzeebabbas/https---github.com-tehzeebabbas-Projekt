from datetime import datetime

class Transaktion:
    def __init__(self, typ, belopp, motpart=None):
        self.typ = typ
        self.belopp = belopp
        self.motpart = motpart
        self.datum = datetime.now()

    def __str__(self):
        if self.motpart:
            return f"{self.datum} | {self.typ} | {self.belopp} kr | Motpart: {self.motpart}"
        return f"{self.datum} | {self.typ} | {self.belopp} kr"

class Konto:
    def __init__(self, kontonummer, ägare):
        self.kontonummer = kontonummer
        self.ägare = ägare
        self.saldo = 0
        self.transaktioner = []

    def sätt_in(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        self.saldo += belopp
        self.transaktioner.append(Transaktion("Insättning", belopp))
        print(f"Du satte in {belopp} kr. Nytt saldo: {self.saldo} kr")

    def ta_ut(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > self.saldo:
            raise ValueError("Otillräckligt saldo")

        self.saldo -= belopp
        self.transaktioner.append(Transaktion("Uttag", belopp))
        print(f"Du har tagit ut {belopp} kr. Nytt saldo: {self.saldo} kr")

    def överför(self, belopp, annat_konto):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > self.saldo:
            raise ValueError("Otillräckligt saldo")

        self.saldo -= belopp
        annat_konto.saldo += belopp

        self.transaktioner.append(
            Transaktion("Överföring ut", belopp, annat_konto.kontonummer)
        )

        annat_konto.transaktioner.append(
            Transaktion("Överföring in", belopp, self.kontonummer)
        )

        print(f"Du överförde {belopp} kr till konto {annat_konto.kontonummer}")
        print(f"Ditt nya saldo: {self.saldo} kr")

    def visa_transaktioner(self):
        if len(self.transaktioner) == 0:
            print("Det finns inga transaktioner ännu.")
        else:
            for t in self.transaktioner:
                print(t)

    def visa_info(self):
        print(
            f"Vanligt konto | Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | Saldo: {self.saldo} kr"
        )


class Sparkonto(Konto):
    def __init__(self, kontonummer, ägare):
        super().__init__(kontonummer, ägare)
        self.ränta = 0.02

    def lägg_till_ränta(self):
        ränta_belopp = self.saldo * self.ränta
        self.saldo += ränta_belopp

        self.transaktioner.append(
            Transaktion("Ränta", ränta_belopp)
        )

        print(f"Ränta tillagd: {ränta_belopp} kr")
        print(f"Nytt saldo: {self.saldo} kr")

    def visa_info(self):
        print(
            f"Sparkonto | Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | "
            f"Saldo: {self.saldo} kr | Ränta: {self.ränta * 100}%"
        )


class Bank:
    def __init__(self, namn):
        self.namn = namn
        self.konton = {}

    def skapa_konto(self):
        ägare = input("Vad heter kontoinnehavaren? ")
        kontonummer = int(input("Vilket kontonummer vill du ha? "))

        if kontonummer in self.konton:
            raise ValueError("Det kontonumret finns redan i denna bank")

        print("Vilken typ av konto vill du skapa?")
        print("1. Vanligt konto")
        print("2. Sparkonto")

        val = input("Välj kontotyp: ")

        if val == "1":
            konto = Konto(kontonummer, ägare)
        elif val == "2":
            konto = Sparkonto(kontonummer, ägare)
        else:
            raise ValueError("Ogiltig kontotyp")

        self.konton[kontonummer] = konto
        print(f"Konto skapat i {self.namn} för {ägare}! Kontonummer: {kontonummer}")

    def hämta_konto(self, kontonummer):
        if kontonummer in self.konton:
            return self.konton[kontonummer]
        else:
            raise ValueError("Kontot finns inte i denna bank")

    def överför_till_annan_bank(self, belopp, från_konto, mottagarbank, till_konto):
        konto1 = self.hämta_konto(från_konto)
        konto2 = mottagarbank.hämta_konto(till_konto)

        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > konto1.saldo:
            raise ValueError("Otillräckligt saldo")

        konto1.saldo -= belopp
        konto2.saldo += belopp

        konto1.transaktioner.append(
            Transaktion(
                "Överföring till annan bank",
                belopp,
                f"{mottagarbank.namn} konto {till_konto}"
            )
        )

        konto2.transaktioner.append(
            Transaktion(
                "Överföring från annan bank",
                belopp,
                f"{self.namn} konto {från_konto}"
            )
        )

        print(f"Du överförde {belopp} kr från {self.namn} till {mottagarbank.namn}")


def välj_bank(banker):
    print("\n--- VÄLJ BANK ---")
    print("1. Nordea")
    print("2. Swedbank")
    print("3. SEB")

    val = input("Välj bank: ")

    if val in banker:
        return banker[val]
    else:
        raise ValueError("Ogiltig bank")


def meny():
    banker = {
        "1": Bank("Nordea"),
        "2": Bank("Swedbank"),
        "3": Bank("SEB")
    }

    bank = välj_bank(banker)
    print(f"Du använder nu banken: {bank.namn}")

    while True:
        print(f"\n--- BANKSYSTEM: {bank.namn} ---")
        print("1. Skapa konto")
        print("2. Sätt in pengar")
        print("3. Ta ut pengar")
        print("4. Överför pengar inom samma bank")
        print("5. Visa saldo")
        print("6. Visa transaktioner")
        print("7. Lägg till ränta på sparkonto")
        print("8. Visa kontoinfo")
        print("9. Byt bank")
        print("10. Överför pengar till annan bank")
        print("11. Avsluta")

        val = input("Välj: ").strip()

        try:
            if val == "1":
                bank.skapa_konto()

            elif val == "2":
                nr = int(input("Kontonummer: "))
                belopp = float(input("Belopp: "))
                konto = bank.hämta_konto(nr)
                konto.sätt_in(belopp)

            elif val == "3":
                nr = int(input("Kontonummer: "))
                belopp = float(input("Belopp: "))
                konto = bank.hämta_konto(nr)
                konto.ta_ut(belopp)

            elif val == "4":
                från = int(input(f"Från konto i {bank.namn}: "))
                till = int(input(f"Till konto i {bank.namn}: "))
                belopp = float(input("Belopp: "))

                konto1 = bank.hämta_konto(från)
                konto2 = bank.hämta_konto(till)

                konto1.överför(belopp, konto2)

            elif val == "5":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)
                print(f"Ägare: {konto.ägare}")
                print(f"Bank: {bank.namn}")
                print(f"Saldo: {konto.saldo} kr")

            elif val == "6":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)
                konto.visa_transaktioner()

            elif val == "7":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)

                if isinstance(konto, Sparkonto):
                    konto.lägg_till_ränta()
                else:
                    print("Det här är inte ett sparkonto.")

            elif val == "8":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)
                print(f"Bank: {bank.namn}")
                konto.visa_info()

            elif val == "9":
                bank = välj_bank(banker)
                print(f"Du använder nu banken: {bank.namn}")

            elif val == "10":
                print("Välj mottagarbank:")
                mottagarbank = välj_bank(banker)

                från = int(input(f"Från konto i {bank.namn}: "))
                till = int(input(f"Till konto i {mottagarbank.namn}: "))
                belopp = float(input("Belopp: "))

                bank.överför_till_annan_bank(belopp, från, mottagarbank, till)

            elif val == "11":
                print("Hej då!")
                break

            else:
                print("Ogiltigt val")

        except Exception as e:
            print("Fel:", e)


meny()