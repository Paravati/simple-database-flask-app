from flask import Flask, g
from flask import render_template
import os
import sqlite3
from datetime import datetime
from flask import flash, redirect, url_for, request

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',  # wartość wykorzystywana do obsługi sesji
    DATABASE=os.path.join(app.root_path, 'db.sqlite'),  # scieżka do pliku bazy
    SITE_NAME='What is your name?'  # nazwa aplikacji
))


def get_db():
    '''Tworzenie połączenia z bazą danych'''
    if not g.get('db'):  # jezeli brak połączenia to je tworzymy
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        g.db = conn  # zapisujemy połączenie w kontekście aplikacji
    return g.db  # zwracamy połączenie z bazą


@app.teardown_appcontext
def close_db(error):
    '''Zamykanie połączenia z bazą'''
    if g.get('db'):
        g.db.close()


@app.route('/users', methods=['GET', 'POST'])  # show all of the records on the one page
def users():
    db = get_db()
    kursor = db.execute('SELECT * FROM users ORDER BY name ASC;')
    users = kursor.fetchall()  # fetchall zwraca dane w formie listy
    return render_template('user.html', users=users)


@app.route('/', methods=['GET','POST'])
def index():
    name = ""
    surname = ""
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        if len(name) > 0:
            if len(surname)!=0:
                data_dodania = datetime.now()
                db = get_db()  # utworzenie obiektu bazy danych
                db.execute('INSERT INTO users VALUES (?, ?, ?, ?);', [None, name, surname, data_dodania])
                db.commit()
                flash('New user added.')
                return redirect(url_for('index'))
            else:
                flash('Please add all data.')
                # return redirect(url_for('index'))
        elif (len(name) == 0 and len(surname) == 0) or (len(name)==0 and len(surname)!=0):
            flash('Please add all data.')
    print("rendering template")
    return render_template('index.html', name=name, surname=surname)


# @app.route('/users/<page>', methods=['GET', 'POST'])
# def users_pages(page):
#     # page=2
#     # page = request.args('page')
#     users_per_page = 15
#     start_at = page*users_per_page
#     db = get_db()
#     kursor = db.execute('SELECT * FROM users ORDER BY name ASC LIMIT %s OFFSET %s;' % (start_at,users_per_page))
#     users = kursor.fetchall()  #fetchall zwraca dane w formie listy
#     return render_template('user.html', users=users)


@app.route('/page=<page>', methods=['GET', 'POST'])
def users_pages(page):
    users_per_page = 10
    start_at = int(page) * users_per_page
    db = get_db()
    kursor = db.execute('SELECT * FROM users ORDER BY name ASC LIMIT %s OFFSET %s;' % (users_per_page, start_at))
    users = kursor.fetchall()  # fetchall zwraca dane w formie listy
    return render_template('user.html', users=users, page=page)


if __name__ == '__main__':
    app.run(debug=True)

    # TO run script schema.sql which creates db.sqlite:
    # sqlite3 db.sqlite < schema.sql
    #
    # Command to open sqlite3 terminal and execute sql commands:
    # sqlite3 db.sqlite




#TODO: gdy chce dodać user'a tylko z samym imieniem lub z nazwiskiem to wyswietla mi sie
#komunikat 'Please add all data.' ale dane z formularza mi się usuwają a chce żeby wciąż były uzupełnione