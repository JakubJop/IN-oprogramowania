# klasa kontoBankowe
class KontoBankowe:
    def __init__(self, wlasciciel):
        self.wlasciciel = wlasciciel
        self.saldo = 0.0
        self.zamkniete = False
        self.dezaktywowane = False

    def wplata(self, kwota):
        if self.zamkniete:
            return "Konto jest zamknięte. Nie można wpłacić środków."

        if self.dezaktywowane:
            self.aktywuj_konto()

        self.saldo += kwota
        return f"Wpłacono {kwota} zł."

    def wyplata(self, kwota, zweryfikowano_tozsamosc=False):
        if self.zamkniete:
            return "Konto jest zamknięte. Nie można wypłacić środków."

        if self.dezaktywowane:
            self.aktywuj_konto()

        if not zweryfikowano_tozsamosc:
            return "Weryfikacja tożsamości nie powiodła się."

        if kwota > self.saldo:
            return "Brak wystarczających środków."

        self.saldo -= kwota
        return f"Wypłacono {kwota} zł."

    def zamknij_konto(self):
        self.zamkniete = True
        return "Konto zostało zamknięte."

    def dezaktywuj_konto(self):
        if not self.zamkniete:
            self.dezaktywowane = True
            return "Konto zostało dezaktywowane."
        return "Nie można dezaktywować zamkniętego konta."

    def aktywuj_konto(self):
        if not self.zamkniete:
            self.dezaktywowane = False
            self.akcja_przy_aktywacji()
            return "Konto zostało ponownie aktywowane."
        return "Nie można aktywować zamkniętego konta."

    def akcja_przy_aktywacji(self):
        print(f"Powiadomienie: Konto '{self.wlasciciel}' zostało aktywowane.")


#Testy jednostkowe


import unittest

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
        wynik = self.konto.wyplata(150, True)
        self.assertEqual(wynik, "Brak wystarczających środków.")

    def test_wyplata_poprawna(self):
        self.konto.wplata(100)
        wynik = self.konto.wyplata(50, True)
        self.assertEqual(wynik, "Wypłacono 50 zł.")
        self.assertEqual(self.konto.saldo, 50)

    def test_dezaktywacja(self):
        wynik = self.konto.dezaktywuj_konto()
        self.assertTrue(self.konto.dezaktywowane)
        self.assertEqual(wynik, "Konto zostało dezaktywowane.")

    def test_reaktywacja_przez_wplate(self):
        self.konto.dezaktywuj_konto()
        wynik = self.konto.wplata(50)
        self.assertFalse(self.konto.dezaktywowane)
        self.assertEqual(self.konto.saldo, 50)

    def test_reaktywacja_przez_wyplate(self):
        self.konto.wplata(100)
        self.konto.dezaktywuj_konto()
        wynik = self.konto.wyplata(20, True)
        self.assertFalse(self.konto.dezaktywowane)
        self.assertEqual(self.konto.saldo, 80)

    def test_zamkniecie_konta(self):
        wynik = self.konto.zamknij_konto()
        self.assertTrue(self.konto.zamkniete)
        self.assertEqual(wynik, "Konto zostało zamknięte.")

    def test_operacje_na_zamknietym_koncie(self):
        self.konto.zamknij_konto()
        wynik1 = self.konto.wplata(100)
        wynik2 = self.konto.wyplata(50, True)
        self.assertEqual(wynik1, "Konto jest zamknięte. Nie można wpłacić środków.")
        self.assertEqual(wynik2, "Konto jest zamknięte. Nie można wypłacić środków.")

    def test_dezaktywacja_zamknietego_konta(self):
        self.konto.zamknij_konto()
        wynik = self.konto.dezaktywuj_konto()
        self.assertEqual(wynik, "Nie można dezaktywować zamkniętego konta.")


# Uruchomienie testów

if __name__ == '__main__':
    unittest.main()
