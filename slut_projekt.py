from datetime import datetime

#Transaktion klass
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

# Konto-klass
class Konto:
    def __init__(self, kontonummer):
        self.kontonummer = kontonummer
        self.saldo = 0
        self.transaktioner = []

    def sätt_in(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        self.saldo += belopp
        self.transaktioner.append(Transaktion("Insättning", belopp))

    def ta_ut(self, belopp):
        if belopp <= 0:
            raise ValueError("Belopp måste vara större än 0")

        if belopp > self.saldo:
            raise ValueError("Otillräckligt saldo")

        self.saldo -= belopp
        self.transaktioner.append(Transaktion("Uttag", belopp))

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

    def visa_transaktioner(self):
        for t in self.transaktioner:
            print(t)


