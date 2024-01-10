from modelss.models import Base
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, joinedload
from modelss.models import Magazyny, Pracownicy, Klienci, Towar, Dostep, Zamowienia, Base

engine = create_engine('sqlite:///instance/projekt.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()


def show_magazyny():
    magazyny = session.query(Magazyny).all()
    return magazyny


def show_pracownicy():
    pracownicy = session.query(Pracownicy, Magazyny.nazwa) \
        .join(Magazyny, Pracownicy.id_magazynu == Magazyny.id_magazynu) \
        .filter(Pracownicy.id_magazynu == Magazyny.id_magazynu) \
        .all()
    return pracownicy


def show_klienci():
    klienci = session.query(Klienci).all()
    return klienci


def show_towar():
    towar = session.query(Towar).all()
    return towar


def show_dostep():
    dostep = session.query(Dostep, Magazyny.nazwa.label('nazwa_magazynu'), Towar.nazwa.label('nazwa_towaru')) \
        .join(Magazyny, Dostep.id_magazynu == Magazyny.id_magazynu) \
        .join(Towar, Dostep.id_towaru == Towar.id_towaru) \
        .filter(Dostep.id_magazynu == Magazyny.id_magazynu) \
        .filter(Dostep.id_towaru == Towar.id_towaru) \
        .all()
    return dostep


def show_zamowienia():
    zamowienia = session \
        .query(Zamowienia, Magazyny.nazwa.label('nazwa_magazynu'), Towar.nazwa.label('nazwa_towaru'),
               Klienci.imie.label('imie_klienta'), Klienci.nazwisko.label('nazwisko_klienta')) \
        .join(Magazyny, Zamowienia.id_magazynu == Magazyny.id_magazynu) \
        .join(Towar, Zamowienia.id_towaru == Towar.id_towaru) \
        .join(Klienci, Zamowienia.id_klienta == Klienci.id_klienta) \
        .filter(Zamowienia.id_magazynu == Magazyny.id_magazynu) \
        .filter(Zamowienia.id_towaru == Towar.id_towaru) \
        .filter(Zamowienia.id_klienta == Klienci.id_klienta) \
        .all()
    return zamowienia


def search_magazyn(nazwa, adres):
    wyniki = session.query(Magazyny).filter(Magazyny.nazwa.like(f"%{nazwa}%")) \
        .filter(Magazyny.adres.like(f"%{adres}%")) \
        .all()

    return wyniki


def add_magazyn(nazwa, adres):
    try:
        nowy_magazyn = Magazyny(nazwa=nazwa, adres=adres)
        session.add(nowy_magazyn)
        session.commit()
        return True, "Magazyn został dodany."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania magazynu: {str(e)}"


def delete_magazyn(magazyn_id):
    magazyn_to_delete = session.query(Magazyny).filter_by(id_magazynu=magazyn_id).first()

    try:
        session.delete(magazyn_to_delete)
        session.commit()
        return True, "Magazyn został usunięty."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania magazynu: {str(e)}"


def edit_magazyn(magazyn_id, new_name, new_adress):
    magazyn_to_edit = session.query(Magazyny).filter_by(id_magazynu=magazyn_id).first()

    try:
        magazyn_to_edit.nazwa = new_name
        magazyn_to_edit.adres = new_adress
        session.commit()
        return True, "Dane magazynu zostały zaktualizowane."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas aktualizacji danych magazynu: {str(e)}"


def search_pracownik(name, lastname, magazyn):
    wyniki = session.query(Pracownicy, Magazyny.nazwa) \
        .join(Magazyny, Pracownicy.id_magazynu == Magazyny.id_magazynu) \
        .filter(Pracownicy.imie.like(f"%{name}%")) \
        .filter(Pracownicy.nazwisko.like(f"%{lastname}%")) \
        .filter(Magazyny.nazwa.like(f"%{magazyn}%")) \
        .all()

    return wyniki


def add_pracownik(name, lastname, magazyn):
    try:
        new_pracownik = Pracownicy(imie=name, nazwisko=lastname, id_magazynu=magazyn)
        session.add(new_pracownik)
        session.commit()
        return True, "Pracownik został dodany."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania pracownika: {str(e)}"


def delete_pracownik(pracownik_id):
    pracownik_to_delete = session.query(Pracownicy).filter_by(id_pracownika=pracownik_id).first()

    try:
        session.delete(pracownik_to_delete)
        session.commit()
        return True, "Pracownik został usunięty."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania pracownika: {str(e)}"


def edit_pracownik(pracownik_id, new_name, new_lastname, new_magazyn):
    pracownik_to_edit = session.query(Pracownicy).filter_by(id_pracownika=pracownik_id).first()

    try:
        pracownik_to_edit.imie = new_name
        pracownik_to_edit.nazwisko = new_lastname
        pracownik_to_edit.id_magazynu = new_magazyn
        session.commit()
        return True, "Dane pracownika zostały zaktualizowane."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas aktualizacji danych pracownika: {str(e)}"


def search_klient(name, lastname):
    wyniki = session.query(Klienci) \
        .filter(Klienci.imie.like(f"%{name}%")) \
        .filter(Klienci.nazwisko.like(f"%{lastname}%")) \
        .all()

    return wyniki


def add_klient(name, lastname):
    try:
        new_klient = Klienci(imie=name, nazwisko=lastname)
        session.add(new_klient)
        session.commit()
        return True, "Klient został dodany."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania klienta: {str(e)}"


def delete_klient(klient_id):
    klient_to_delete = session.query(Klienci).filter_by(id_klienta=klient_id).first()

    try:
        session.delete(klient_to_delete)
        session.commit()
        return True, "Klient został usunięty."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania klienta: {str(e)}"


def edit_klient(klient_id, new_name, new_lastname):
    klient_to_edit = session.query(Klienci).filter_by(id_pklienta=klient_id).first()

    try:
        klient_to_edit.imie = new_name
        klient_to_edit.nazwisko = new_lastname
        session.commit()
        return True, "Dane klienta zostały zaktualizowane."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas aktualizacji danych klienta: {str(e)}"


def search_towar(name):
    wyniki = session.query(Towar) \
        .filter(Towar.nazwa.like(f"%{name}%")) \
        .all()
    return wyniki


def add_towar(name, price):
    try:
        new_towar = Towar(nazwa=name, cena=price)
        session.add(new_towar)
        session.commit()
        return True, "Towar został dodany."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania towaru: {str(e)}"


def delete_towar(towar_id):
    towar_to_delete = session.query(Towar).filter_by(id_towaru=towar_id).first()

    try:
        session.delete(towar_to_delete)
        session.commit()
        return True, "Towar został usunięty."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania towaru: {str(e)}"


def edit_towar(towar_id, new_name, new_price):
    towar_to_edit = session.query(Towar).filter_by(id_towaru=towar_id).first()

    try:
        towar_to_edit.nazwa = new_name
        towar_to_edit.cena = new_price
        session.commit()
        return True, "Dane towaru zostały zaktualizowane."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas aktualizacji danych towaru: {str(e)}"


def search_dostep(magazyn, towar):
    wyniki = session.query(Dostep, Magazyny.nazwa.label('nazwa_magazynu'), Towar.nazwa.label('nazwa_towaru')) \
        .join(Magazyny, Dostep.id_magazynu == Magazyny.id_magazynu) \
        .join(Towar, Dostep.id_towaru == Towar.id_towaru) \
        .filter(Dostep.id_magazynu == Magazyny.id_magazynu) \
        .filter(Dostep.id_towaru == Towar.id_towaru) \
        .filter(Magazyny.nazwa.like(f"%{magazyn}%")) \
        .filter(Towar.nazwa.like(f"%{towar}%")) \
        .all()
    return wyniki


def add_dostep(magazyn, towar, amount):
    try:
        new_dostep = Dostep(id_magazynu=magazyn, id_towaru=towar, ilosc=amount)
        session.add(new_dostep)
        session.commit()
        return True, "Dostep został dodany."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania dostepu: {str(e)}"


def delete_dostep(dostep_id):
    dostep_to_delete = session.query(Dostep).filter_by(id_dostepu=dostep_id).first()

    try:
        session.delete(dostep_to_delete)
        session.commit()
        return True, "Dostep został usunięty."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania dostepu: {str(e)}"


def search_zamowienia(name_klient, lastname_klient, magazyn, towar):
    wyniki = session \
        .query(Zamowienia, Magazyny.nazwa.label('nazwa_magazynu'), Towar.nazwa.label('nazwa_towaru'),
               Klienci.imie.label('imie_klienta'), Klienci.nazwisko.label('nazwisko_klienta'))\
        .join(Magazyny, Zamowienia.id_magazynu == Magazyny.id_magazynu) \
        .join(Towar, Zamowienia.id_towaru == Towar.id_towaru) \
        .join(Klienci, Zamowienia.id_klienta == Klienci.id_klienta) \
        .filter(Zamowienia.id_magazynu == Magazyny.id_magazynu) \
        .filter(Zamowienia.id_towaru == Towar.id_towaru) \
        .filter(Zamowienia.id_klienta == Klienci.id_klienta) \
        .filter(Klienci.imie.like(f"%{name_klient}%")) \
        .filter(Klienci.nazwisko.like(f"%{lastname_klient}%")) \
        .filter(Magazyny.nazwa.like(f"%{magazyn}%")) \
        .filter(Towar.nazwa.like(f"%{towar}%")) \
        .all()
    return wyniki


def add_zamowienia(klient, towar, magazyn):
    try:
        new_zamowienie = Zamowienia(id_klienta=klient, id_towaru=towar, id_magazynu=magazyn)
        session.add(new_zamowienie)
        session.commit()
        return True, "Zamowienie zostało dodane."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas dodawania zamówienia: {str(e)}"


def delete_zamowienia(zamowienie_id):
    zamowienie_to_delete = session.query(Dostep).filter_by(id_zamowienia=zamowienie_id).first()

    try:
        session.delete(zamowienie_to_delete)
        session.commit()
        return True, "Zamówienie zostało usunięte."
    except Exception as e:
        session.rollback()
        return False, f"Błąd podczas usuwania zamówienia: {str(e)}"

def count_magazyny():
    liczba_magazynow = session.query(Magazyny).count()
    return liczba_magazynow
def count_miasta():
    liczba_miast = session.query(func.count(func.distinct(Magazyny.adres))).scalar()
    return liczba_miast

def count_pracownicy():
    liczba_pracownikow = session.query(Pracownicy).count()
    return liczba_pracownikow

def count_klienci():
    liczba_klientow = session.query(Klienci).count()
    return liczba_klientow

def count_towary():
    liczba_towarow = session.query(Towar).count()
    return liczba_towarow

def dostep_stat():
    dostep_stat = session.query(Magazyny.nazwa.label('nazwa_magazynu'), func.count(Dostep.id_dostepu).label('liczba_rekordow')) \
        .join(Dostep, Dostep.id_magazynu == Magazyny.id_magazynu) \
        .group_by(Magazyny.nazwa) \
        .all()
    return dostep_stat

def count_zamowienia():
    liczba_zamowien = session.query(Zamowienia).count()
    return liczba_zamowien