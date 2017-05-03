from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import sqlite3
import time

app = Flask("Kosomokourjet")
app.secret_key = 'YOLOBITCHOMMEGLE45612165216'


@app.route('/')
def index():
    if 'username' in session:
        return render_template('base.html', username = escape(session['username']))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    hash_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    conn = sqlite3.connect('donnees.db')
    c = conn.cursor()
    pseudo =  str(request.form['pseudo'] )
    c.execute("SELECT password_hash FROM account WHERE pseudo ='%s'" % pseudo)
    resultat = c.fetchone()[0]

    if resultat is None :
        error_login = "Votre pseudo n'existe pas"
        return render_template('login.html', message = error_login)

    if resultat != hash_password :
        error_login = "Votre mot de passe est erroné"
        return render_template('login.html', message = error_login)

    session['username'] = request.form['pseudo']
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    info_logout = "Vous vous êtes déconnecté"
    return render_template('login.html', message = info_logout)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password1'] == request.form['password2']:
            conn = sqlite3.connect('donnees.db')
            pseudo = request.form['pseudo']
            c = conn.cursor()
            c.execute("""SELECT player_id FROM account WHERE pseudo = '%s'""" % pseudo)
            resultat = c.fetchone()




            if resultat is None :
                #inscription en BD
                hash_password = hashlib.sha256(request.form['password1'].encode()).hexdigest()
                c.execute("INSERT INTO account(pseudo, password_hash) VALUES(?,?)", (pseudo, hash_password) )
                conn.commit()
                info_inscription = "Votre inscription a été prise en compte, vous pouvez désormais vous connecter."
                return render_template('login.html', message = info_inscription)

            else :
                return "erreur, pseudo déja utilisé"

        else:
            return "erreur, mots de passe différents"

    return render_template('register.html')







# CREATION B DONNEES













app.run(port = 5001)
