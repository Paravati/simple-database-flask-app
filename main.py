from flask import Flask, g
from flask import render_template
import os
import sqlite3
from datetime import datetime
from flask import flash, redirect, url_for, request

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = 'bardzosekretnawartosc',   # wartość wykorzystywana do obsługi sesji
    DATABASE = os.path.join(app.root_path, 'db.sqlite'),  # scieżka do pliku bazy
    SITE_NAME = 'What is your name?'  # nazwa aplikacji
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


@app.route('/users', methods=['GET', 'POST'])
def users():
    error=None
    if request.method=='POST':
        # name = request.form['name'].strip()
        name = request.form['name']
        surname = request.form['surname']
        if len(name) >0:
            data_dodania = datetime.now()
            db = get_db()  # utworzenie obiektu bazy danych
            db.execute('INSERT INTO users VALUES (?, ?, ?, ?);', [None, name, surname, data_dodania])
            db.commit()
            flash('New user added.')
            return redirect(url_for('users'))
        error= 'You cannot add empty user!'  # komunikat o błędzie

    db = get_db()
    kursor = db.execute('SELECT * FROM users ORDER BY name ASC;')
    # kursor = db.execute('SELECT * FROM users ORDER BY name ASC LIMIT 5;')
    users = kursor.fetchall()  #fetchall zwraca dane w formie listy
    return render_template('user.html', users=users, error=error)

#
@app.route('/')
def index():
    return render_template('index.html')

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
    # page=2
    # page = request.args('page')
    users_per_page = 15
    start_at = page*users_per_page
    db = get_db()
    kursor = db.execute('SELECT * FROM users ORDER BY name ASC LIMIT %s OFFSET %s;' % (start_at,users_per_page))
    users = kursor.fetchall()  #fetchall zwraca dane w formie listy
    return render_template('user.html', users=users)

# @app.route('/zrobione', methods=['POST'])
# def zrobione():  # zmiana statusu zadania na wykonane
#     zadanie_id = request.form['id']
#     db = get_db()
#     db.execute('UPDATE zadania SET zrobione=1 WHERE id=?', [zadanie_id])
#     db.commit()
#     flash('Zmieniono status zadania')
#     return redirect(url_for('zadania'))


if __name__ == '__main__':
    app.run(debug=True)



    # TO run script schema.sql which creates db.sqlite:
    # sqlite3 db.sqlite < schema.sql
    #
    # Command to open sqlite3 terminal and execute sql commands:
    # sqlite3 db.sqlite
