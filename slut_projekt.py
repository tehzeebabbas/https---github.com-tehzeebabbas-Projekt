import requests
import json
from datetime import datetime

#Klass för transaktioner
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

#Grundklass för konto
class Konto:
    def __init__(self, kontonummer, ägare):
        self.kontonummer = kontonummer
        self.ägare = ägare
        self.saldo = 0

        #Lista med alla transaktioner
        self.transaktioner = []

    def sätt_in(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")
           
        #Lägger till pengar på konto
        self.saldo += belopp

        #Sparar transaktionen
        self.transaktioner.append(Transaktion("Insättning", belopp))
        print(f"Du satte in {belopp} kr. Nytt saldo: {self.saldo} kr")

    def ta_ut(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > self.saldo:
            raise ValueError("Otillräckligt saldo")

        #Tar ut pengar
        self.saldo -= belopp

        #Sparar transaktionen
        self.transaktioner.append(Transaktion("Uttag", belopp))
        print(f"Du har tagit ut {belopp} kr. Nytt saldo: {self.saldo} kr")

    def överför(self, belopp, annat_konto):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > self.saldo:
            raise ValueError("Otillräckligt saldo")

        #Tar pengar från första konto
        self.saldo -= belopp

        #Lägger pengar på andra konto
        annat_konto.saldo += belopp
 
        #Sparar transaktion på konto 1
        self.transaktioner.append(
            Transaktion("Överföring ut", belopp, annat_konto.kontonummer)
        )

        #Sparar transaktion på konto 2
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

    #Polymorfism, samma metoed i sparkonton okcså men det fungerar på olika sätt
    def visa_info(self):
        print(
            f"Vanligt konto | Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | Saldo: {self.saldo} kr"
        )

#Arv från konto
class Sparkonto(Konto):
    def __init__(self, kontonummer, ägare):
        super().__init__(kontonummer, ägare)

        #Ränta
        self.ränta = 0.02

    def lägg_till_ränta(self):

        #Ränta beräknas
        ränta_belopp = self.saldo * self.ränta

        #Ränta läggs till på saldo
        self.saldo += ränta_belopp

        #Sparar transaktion
        self.transaktioner.append(
            Transaktion("Ränta", ränta_belopp)
        )

        print(f"Ränta tillagd: {ränta_belopp} kr")
        print(f"Nytt saldo: {self.saldo} kr")

    #Polymorfism, visar bara sparkonton's information
    def visa_info(self):
        print(
            f"Sparkonto | Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | "
            f"Saldo: {self.saldo} kr | Ränta: {self.ränta * 100}%"
        )

#Arv från Konto
class Kreditkonto(Konto):
    def __init__(self, kontonummer, ägare):
        super().__init__(kontonummer, ägare)

        #Konto får gå minus
        self.kreditgräns = -5000

    def ta_ut(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        #Kreditkonto får gå minus
        if self.saldo - belopp < self.kreditgräns:
            raise ValueError("Du har nått kreditgränsen")

        self.saldo -= belopp

        self.transaktioner.append(Transaktion("Kredituttag", belopp))

        print(f"Du tog ut {belopp} kr")
        print(f"Nytt saldo: {self.saldo} kr")

    #Polymorfism
    def visa_info(self):
        print(f"Kreditkonto | "
            f"Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | "
            f"Saldo: {self.saldo} kr | "
            f"Kreditgräns: {self.kreditgräns} kr"
        )

#Arv från konto
class Premiumkonto(Konto):
    def __init__(self, kontonummer, ägare):
        super().__init__(kontonummer, ägare)

        #Högre ränta
        self.ränta = 0.05

        #Bonus
        self.bonus = 500

    def lägg_till_ränta(self):

        ränta_belopp = self.saldo * self.ränta
        self.saldo += ränta_belopp

        self.transaktioner.append(
        Transaktion("Premiumränta", ränta_belopp))
       
        print(f"Premiumränta tillagd: {ränta_belopp} kr")
        print(f"Nytt saldo: {self.saldo} kr")

    def lägg_till_bonus(self):

        #Bonus läggs till
        self.saldo += self.bonus

        #Sparar bonus som transaktion
        self.transaktioner.append(
            Transaktion("Premiumbonus", self.bonus)
        )
        print(f"Bonus tillagd: {self.bonus} kr")
        print(f"Nytt saldo: {self.saldo} kr")

    #Polymorfism
    def visa_info(self):
        print(
            f"Premiumkonto | "
            f"Ägare: {self.ägare} | "
            f"Kontonummer: {self.kontonummer} | "
            f"Saldo: {self.saldo} kr | "
            f"Ränta: {self.ränta * 100}% | "
            f"Bonus: {self.bonus} kr"
        )

#Klass för bank
class Bank:
    def __init__(self, namn):
        self.namn = namn

        #Dictionary med alla konton
        self.konton = {}

    def skapa_konto(self):
        ägare = input("Vad heter kontoinnehavaren? ")
        kontonummer = int(input("Vilket kontonummer vill du ha? "))

        if kontonummer in self.konton:
            raise ValueError("Kontonumret finns redan")
        print("1. Vanligt konto")
        print("2. Sparkonto")
        print("3. Kreditkonto")
        print("4. Premiumkonto")

        val = input("Välj kontotyp: ")
        if val == "1":
            konto = Konto(kontonummer, ägare)

        elif val == "2":
            konto = Sparkonto(kontonummer, ägare)

        elif val == "3":
            konto = Kreditkonto(kontonummer, ägare)

        elif val == "4":
            konto = Premiumkonto(kontonummer, ägare)

        else:
            raise ValueError("Ogiltig kontotyp")

        #Sparar konto i dictionary
        self.konton[kontonummer] = konto
        print(f"Konto skapat i {self.namn}")

    def hämta_konto(self, kontonummer):
        if kontonummer in self.konton:
            return self.konton[kontonummer]

        else:
            raise ValueError("Kontot finns inte")

    #API från Riksbanken
    def visa_riksbank_data(self):
        url = "https://api.riksbank.se/swea/v1/CalendarDays/{from}"
        try:
            #Hämtar data från internet
            response = requests.get(url)

            #Om allt fungerar
            if response.status_code == 200:

                #Gör om JSON till Python-data
                data = response.json()
                print("\nData från Riksbanken:\n")

                #Skriver ut JSON snyggt
                print(json.dumps(data, indent=4,ensure_ascii=False))

            else:
                print("Kunde inte hämta data")

        except Exception as e:
            print("Fel vid API:", e)

    #Sparar konton som JSON
    def spara_konton(self):
        data = {}

        #Går igenom alla konton
        for nummer, konto in self.konton.items():

            data[nummer] = {
                "ägare": konto.ägare,
                "saldo": konto.saldo,
                "typ": konto.__class__.__name__
            }

        #Skapar JSON-fil
        with open("konton.json", "w", encoding="utf-8") as fil:
            json.dump(data, fil, indent=4, ensure_ascii=False)
        print("Konton sparade i JSON-fil")

#Funktion för att välja bank
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
        print(f"\nBANKSYSTEM: {bank.namn}")
        print("1. Skapa konto")
        print("2. Sätt in pengar")
        print("3. Ta ut pengar")
        print("4. Överför pengar")
        print("5. Visa saldo")
        print("6. Visa transaktioner")
        print("7. Lägg till ränta på sparkonto")
        print("8. Lägg till ränta på premiumkonto")
        print("9. Visa kontoinfo")
        print("10. Visa Riksbank API-data")
        print("11. Spara konton som JSON")
        print("12. Byt bank")
        print("13. Avsluta")

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
                från = int(input("Från konto: "))
                till = int(input("Till konto: "))
                belopp = float(input("Belopp: "))   
                konto1 = bank.hämta_konto(från)
                konto2 = bank.hämta_konto(till)
                konto1.överför(belopp, konto2)

            elif val == "5":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)
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
                    print("Det här är inte ett sparkonto")

            elif val == "8":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)

                if isinstance(konto, Premiumkonto):
                    konto.lägg_till_bonus()

                else:
                    print("Det här är inte ett premiumkonto")
           
            elif val == "9":
                nr = int(input("Kontonummer: "))
                konto = bank.hämta_konto(nr)
                konto.visa_info()

            elif val == "9":
                bank.visa_riksbank_data()

            elif val == "10":
                bank.spara_konton()

            elif val == "11":
                bank = välj_bank(banker)

            elif val == "12":
                print("Hej då!")
                break

            else:
                print("Ogiltigt val")

        except ValueError as e:
            print("ValueError:", e)

        except Exception as e:
            print("Fel:", e)

#Startar programmet
meny()