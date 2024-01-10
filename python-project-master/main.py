from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, flash, redirect, url_for
from modelss.models import Magazyny, Pracownicy, Klienci, Towar, Dostep, Zamowienia, Base
from modelss.db_tools import show_magazyny, show_pracownicy, show_klienci, show_towar, show_dostep, show_zamowienia, \
    delete_magazyn, edit_magazyn, search_magazyn, add_magazyn, search_pracownik, add_pracownik, delete_pracownik, \
    edit_pracownik, search_klient, add_klient, delete_klient, edit_klient, search_towar, add_towar, delete_towar, \
    edit_towar, search_dostep, add_dostep, delete_dostep, search_zamowienia, add_zamowienia, delete_zamowienia, \
    count_magazyny, count_miasta, count_pracownicy, count_klienci, count_towary, dostep_stat, count_zamowienia

app = Flask(__name__)
app.secret_key = "aofk3l5k3ldasdlk5l39wka5l"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///instance/projekt.db"

Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/magazyny")
def magazyny():
    return render_template("magazyny.html", magazyny=show_magazyny(), liczba_magazynow=count_magazyny(), liczba_miast=count_miasta())


@app.route("/pracownicy")
def pracownicy():
    return render_template("pracownicy.html", pracownicy=show_pracownicy(), magazyny=show_magazyny(), liczba_pracownikow=count_pracownicy())


@app.route("/klienci")
def klienci():
    return render_template("klienci.html", klienci=show_klienci(), liczba_klientow=count_klienci())


@app.route("/towar")
def towar():
    return render_template("towar.html", towary=show_towar(), liczba_towarow=count_towary())


@app.route("/dostep")
def dostep():
    return render_template("dostep.html", dostepy=show_dostep(), magazyny=show_magazyny(), towary=show_towar(), dostep_stat=dostep_stat())


@app.route("/zamowienia")
def zamowienia():
    return render_template("zamowienia.html", zamowienia=show_zamowienia(), pracownicy=show_pracownicy(),
                           klienci=show_klienci(), magazyny=show_magazyny(), towary=show_towar(), liczba_zamowien=count_zamowienia())


@app.route("/search_magazyn", methods=["POST"])
def search_magazyn_route():
    nazwa = request.form['search_name']
    adres = request.form['search_adress']

    wyniki = search_magazyn(nazwa, adres)

    return render_template("magazyny.html", magazyny=wyniki)


@app.route("/add_magazyn", methods=["POST"])
def add_magazyn_route():
    nazwa = request.form['newMagazynName']
    adres = request.form['newMagazynAdres']

    success, message = add_magazyn(nazwa, adres)
    flash(message)

    return render_template("magazyny.html", magazyny=show_magazyny())


@app.route("/delete_magazyn/<int:magazyn_id>", methods=["POST"])
def delete_magazyn_route(magazyn_id):
    success, message = delete_magazyn(magazyn_id)
    flash(message)
    return redirect(url_for("magazyny"))


@app.route("/edit_magazyn/<int:magazyn_id>", methods=["POST"])
def edit_magazyn_route(magazyn_id):
    new_name = request.form.get("new_name")
    new_adress = request.form.get("new_adress")

    success, message = edit_magazyn(magazyn_id, new_name, new_adress)
    flash(message)

    return redirect(url_for("magazyny"))


@app.route("/search_pracownik", methods=["POST"])
def search_pracownik_route():
    name = request.form['search_name']
    lastname = request.form['search_lastname']
    magazyn = request.form['search_magazyn']

    wyniki = search_pracownik(name, lastname, magazyn)
    return render_template("pracownicy.html", pracownicy=wyniki, magazyny=show_magazyny())


@app.route("/add_pracownik", methods=["POST"])
def add_pracownik_route():
    name = request.form['newPracownikName']
    lastname = request.form['newPracownikSurname']
    magazyn = request.form['newPracownikMagazyn']

    success, message = add_pracownik(name, lastname, magazyn)
    flash(message)

    return render_template("pracownicy.html", pracownicy=show_pracownicy(), magazyny=show_magazyny())


@app.route("/delete_pracownik/<int:pracownik_id>", methods=["POST"])
def delete_pracownik_route(pracownik_id):
    success, message = delete_pracownik(pracownik_id)
    flash(message)
    return redirect(url_for("pracownicy"))


@app.route("/edit_pracownik/<int:pracownik_id>", methods=["POST"])
def edit_pracownik_route(pracownik_id):
    new_name = request.form.get("new_name")
    new_lastname = request.form.get("new_lastname")
    new_magazyn = request.form.get("new_magazyn")

    success, message = edit_pracownik(pracownik_id, new_name, new_lastname, new_magazyn)
    flash(message)

    return redirect(url_for("pracownicy"))


@app.route("/search_klient", methods=["POST"])
def search_klient_route():
    name = request.form['search_name']
    lastname = request.form['search_lastname']

    wyniki = search_klient(name, lastname)
    return render_template("klienci.html", klienci=wyniki)


@app.route("/add_klient", methods=["POST"])
def add_klient_route():
    name = request.form['newKlientName']
    lastname = request.form['newKlientSurname']

    success, message = add_klient(name, lastname)
    flash(message)

    return render_template("klienci.html", klienci=show_klienci())


@app.route("/delete_klient/<int:klient_id>", methods=["POST"])
def delete_klient_route(klient_id):
    success, message = delete_klient(klient_id)
    flash(message)
    return redirect(url_for("klienci"))


@app.route("/edit_klient/<int:klient_id>", methods=["POST"])
def edit_klient_route(klient_id):
    new_name = request.form.get("new_name")
    new_lastname = request.form.get("new_lastname")

    success, message = edit_klient(klient_id, new_name, new_lastname)
    flash(message)

    return redirect(url_for("klienci"))


@app.route("/search_towar", methods=["POST"])
def search_towar_route():
    name = request.form['search_name']

    wyniki = search_towar(name)
    return render_template("towar.html", towary=wyniki)


@app.route("/add_towar", methods=["POST"])
def add_towar_route():
    name = request.form['newTowarName']
    price = request.form['newTowarPrice']

    success, message = add_towar(name, price)
    flash(message)

    return render_template("towar.html", towary=show_towar())


@app.route("/delete_towar/<int:towar_id>", methods=["POST"])
def delete_towar_route(towar_id):
    success, message = delete_towar(towar_id)
    flash(message)
    return redirect(url_for("towar"))


@app.route("/edit_towar/<int:towar_id>", methods=["POST"])
def edit_towar_route(towar_id):
    new_name = request.form.get("new_name")
    new_price = request.form.get("new_price")

    success, message = edit_towar(towar_id, new_name, new_price)
    flash(message)

    return redirect(url_for("towar"))


@app.route("/search_dostep", methods=["POST"])
def search_dostep_route():
    name = request.form['search_name']
    towarr = request.form['search_towar']

    wyniki = search_dostep(name, towarr)
    return render_template("dostep.html", dostepy=wyniki, magazyny=show_magazyny(), towary=show_towar())


@app.route("/add_dostep", methods=["POST"])
def add_dostep_route():
    magazyn = request.form['newDostepMagazyn']
    towarr = request.form['newDostepTowar']
    ilosc = request.form['newDostepAmount']

    success, message = add_dostep(magazyn, towarr, ilosc)
    flash(message)

    return render_template("dostep.html", dostepy=show_dostep(), magazyny=show_magazyny(), towary=show_towar())


@app.route("/delete_dostep/<int:dostep_id>", methods=["POST"])
def delete_dostep_route(dostep_id):
    success, message = delete_dostep(dostep_id)
    flash(message)
    return redirect(url_for("dostep"))


@app.route("/edit_dostep/<int:dostep_id>", methods=["POST"])
def edit_dostep_route(dostep_id):
    new_amount = request.form.get("new_name")

    success, message = edit_dostep(dostep_id, new_amount)
    flash(message)

    return redirect(url_for("dostep"))


@app.route("/search_zamowienia", methods=["POST"])
def search_zamowienia_route():
    name_klient = request.form['search_name_klient']
    lastname_klient = request.form['search_lastname_klient']
    towarr = request.form['search_towar']
    magazyn = request.form['search_magazyn']
    name_pracownik = request.form['search_name_pracownik']
    lastname_pracownik = request.form['search_lastname_pracownik']

    wyniki = search_zamowienia(name_klient, lastname_klient, towarr, magazyn, name_pracownik, lastname_pracownik)
    return render_template("zamowienia.html", zamowienia=wyniki, pracownicy=show_pracownicy(),
                           klienci=show_klienci(), magazyny=show_magazyny(), towary=show_towar())


@app.route("/add_zamowienie", methods=["POST"])
def add_zamowienie_route():
    klient = request.form['addZamowieniaKlient']
    towarr = request.form['addZamowieniaTowar']
    magazyn = request.form['addZamowieniaMagazyn']
    pracownik = request.form['addZamowieniaPracownik']

    success, message = add_zamowienia(klient, towarr, magazyn, pracownik)
    flash(message)

    return render_template("zamowienia.html", zamowienia=show_zamowienia(), pracownicy=show_pracownicy(),
                           klienci=show_klienci(), magazyny=show_magazyny(), towary=show_towar())


@app.route("/delete_zamowienie/<int:zamowienia_id>", methods=["POST"])
def delete_zamowienie_route(zamowienia_id):
    success, message = delete_dostep(zamowienia_id)
    flash(message)
    return redirect(url_for("zamowienia"))


with app.app_context():

    app.run(host='0.0.0.0', port=81, debug=True)
