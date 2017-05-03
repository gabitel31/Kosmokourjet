from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import sqlite3
import time
import generation_univers

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
    resultat = c.fetchone()

    if resultat is None :
        error_login = "Votre pseudo n'existe pas"
        return render_template('login.html', message = error_login)

    if resultat[0] != hash_password :
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

        if len(request.form['password1']) < 5 :
            info_inscription = "erreur, mot de passe top court (min. 6 caractères)" #Vérification longuieur password
            return render_template('login.html', message = info_inscription)

        if len(request.form['pseudo']) < 4 :
            info_inscription = "erreur, pseudo trop court (ctb, min. 5 caractères)" #Vérification longuieur pseudo
            return render_template('login.html', message = info_inscription)

        if request.form['password1'] == request.form['password2'] :  #Véridication pseudo conforme x2
            conn = sqlite3.connect('donnees.db')
            pseudo = request.form['pseudo']
            c = conn.cursor()
            c.execute("""SELECT player_id FROM account WHERE pseudo = '%s'""" % pseudo) #Vérification pseudo inexistant
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




univers = generation_univers.gen_univ(30,99,99,1)

#INSCRITION EN BD DES SYSTEMES SOLAIRES
conn = sqlite3.connect('donnees.db')
c = conn.cursor()
c.execute("""SELECT id_system FROM planetary_system""") #Vérification Univers
resultat = c.fetchone()

if resultat is None : #SI BD VIDE
    print("Génération de l'univers en cours...")
    for index in range(1,3):   #KIKI DUR
        print("."*index)
        time.sleep(0.7)


    for systeme in univers:
        c = conn.cursor()
        c.execute("INSERT INTO planetary_system(coord_x, coord_y, name) VALUES(?,?,?)", (systeme[0], systeme[1],systeme [2])) #Vérification pseudo inexistant
    conn.commit()
    print("Univers généré avec succès !")
else:
    print("Univers deja existant.")


app.run(port = 5001)
