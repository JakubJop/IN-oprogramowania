import unittest

class KontoBankowe:
    def __init__(self, wlasciciel):
        self.wlasciciel = wlasciciel
        self.saldo = 0
        self.dezaktywowane = False
        self.zamkniete = False
        print(f"Powiadomienie: Konto '{self.wlasciciel}' zostało aktywowane.")

    def wplata(self, kwota):
        if self.zamkniete:
            return "Konto jest zamknięte. Nie można wpłacić środków."
        if self.dezaktywowane:
            self.dezaktywowane = False
        self.saldo += kwota
        return f"Wpłacono {kwota} zł."

    def wyplata(self, kwota, weryfikacja=False):
        if self.zamkniete:
            return "Konto jest zamknięte. Nie można wypłacić środków."
        if not weryfikacja:
            return "Weryfikacja tożsamości nie powiodła się."
        if self.dezaktywowane:
            self.dezaktywowane = False
        if self.saldo < kwota:
            return "Brak wystarczających środków."
        self.saldo -= kwota
        return f"Wypłacono {kwota} zł."

    def dezaktywuj_konto(self):
        if self.zamkniete:
            return "Nie można dezaktywować zamkniętego konta."
        self.dezaktywowane = True
        return "Konto zostało dezaktywowane."

    def zamknij_konto(self):
        self.zamkniete = True
        return "Konto zostało zamknięte."


class TestKontoBankowe(unittest.TestCase):
    def setUp(self):
        self.konto = KontoBankowe("Anna Nowak")

    def test_wplata(self):
        wynik = self.konto.wplata(100)
        self.assertEqual(self.konto.saldo, 100)
        self.assertEqual(wynik, "Wpłacono 100 zł.")

    def test_wyplata_bez_weryfikacji(self):
        self.konto.wplata(100)
        wynik = self.konto.wyplata(50)
        self.assertEqual(wynik, "Weryfikacja tożsamości nie powiodła się.")

    def test_wyplata_niewystarczajace_srodki(self):
        self.konto.wplata(100)
        wynik = self.konto.wyplata(200, weryfikacja=True)
        self.assertEqual(wynik, "Brak wystarczających środków.")

    def test_wyplata_poprawna(self):
        self.konto.wplata(100)
        wynik = self.konto.wyplata(50, weryfikacja=True)
        self.assertEqual(self.konto.saldo, 50)
        self.assertEqual(wynik, "Wypłacono 50 zł.")

    def test_dezaktywacja(self):
        self.konto.dezaktywuj_konto()
        self.assertTrue(self.konto.dezaktywowane)

    def test_reaktywacja_przez_wplate(self):
        self.konto.dezaktywuj_konto()
        self.konto.wplata(50)
        self.assertFalse(self.konto.dezaktywowane)

    def test_reaktywacja_przez_wyplate(self):
        self.konto.wplata(100)
        self.konto.dezaktywuj_konto()
        self.konto.wyplata(50, weryfikacja=True)
        self.assertFalse(self.konto.dezaktywowane)

    def test_zamkniecie_konta(self):
        self.konto.zamknij_konto()
        self.assertTrue(self.konto.zamkniete)

    def test_operacje_na_zamknietym_koncie(self):
        self.konto.zamknij_konto()
        wynik_wplaty = self.konto.wplata(50)
        wynik_wyplaty = self.konto.wyplata(50, weryfikacja=True)
        self.assertEqual(wynik_wplaty, "Konto jest zamknięte. Nie można wpłacić środków.")
        self.assertEqual(wynik_wyplaty, "Konto jest zamknięte. Nie można wypłacić środków.")

    def test_dezaktywacja_zamknietego_konta(self):
        self.konto.zamknij_konto()
        wynik = self.konto.dezaktywuj_konto()
        self.assertEqual(wynik, "Nie można dezaktywować zamkniętego konta.")


if __name__ == "__main__":
    unittest.main()
