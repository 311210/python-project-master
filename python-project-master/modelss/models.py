from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///instance/projekt.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Magazyny(Base):
    __tablename__ = 'Magazyny'
    id_magazynu = Column(Integer, primary_key=True)
    nazwa = Column(String(50), nullable=False, unique=True)
    adres = Column(String(100), nullable=False)


class Pracownicy(Base):
    __tablename__ = 'Pracownicy'
    id_pracownika = Column(Integer, primary_key=True)
    imie = Column(String(20), nullable=False)
    nazwisko = Column(String(30), nullable=False)
    id_magazynu = Column(Integer, ForeignKey('Magazyny.id_magazynu'))
    mail = Column(String(30))
    magazyn = relationship("Magazyny", backref="Pracownicy")


class Klienci(Base):
    __tablename__ = 'Klienci'
    id_klienta = Column(Integer, primary_key=True)
    imie = Column(String(100), nullable=False)
    nazwisko = Column(String(100), nullable=False)
    saldo = Column(Integer)


class Towar(Base):
    __tablename__ = 'Towar'
    id_towaru = Column(Integer, primary_key=True)
    nazwa = Column(String(100), nullable=False)
    cena = Column(Integer, nullable=False)


class Dostep(Base):
    __tablename__ = 'Dostep'
    id_dostepu = Column(Integer, primary_key=True)
    id_magazynu = Column(Integer, ForeignKey('Magazyny.id_magazynu'), primary_key=True)
    id_towaru = Column(Integer, ForeignKey('Towar.id_towaru'), primary_key=True)
    ilosc = Column(Integer)
    magazyn = relationship("Magazyny", backref="Dostep")
    towar = relationship("Towar", backref="Dostep")


class Zamowienia(Base):
    __tablename__ = 'Zamowienia'
    id_zamowienia = Column(Integer, primary_key=True)
    id_klienta = Column(Integer, ForeignKey('Klienci.id_klienta'))
    id_towaru = Column(Integer, ForeignKey('Towar.id_towaru'))
    id_magazynu = Column(Integer, ForeignKey('Magazyny.id_magazynu'))
    klient = relationship("Klienci", backref="Zamowienia")
    towar = relationship("Towar", backref="Zamowienia")
    magazyn = relationship("Magazyny", backref="Zamowienia")
