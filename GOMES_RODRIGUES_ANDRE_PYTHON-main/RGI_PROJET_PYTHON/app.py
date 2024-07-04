##Ver avec utilisation de session
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import pymysql, os
import hashlib

app = Flask(__name__)
# Configuration de l'application à partir des variables d'environnement
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Fonction pour se connecter à la BDD
def connect_db():
    cx = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        charset="utf8mb4",
    )
    return cx

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
mail = Mail(app)

# Fonction email de confirmation de réservation
def send_confirmation_email(to_email, date, horaire):
    msg = Message("Confirmation de votre réservation",
                recipients=[to_email])
    msg.body = f"Votre réservation pour le {date} à {horaire} a été confirmée."
    mail.send(msg)

# Fonction email de notification de réservation au formateur
def send_notification_email(to_email, date, horaire, nom_Alternant):
    msg = Message("Nouvelle réservation de créneau",
                recipients=[to_email])
    msg.body = f"L'Alternant(e) {nom_Alternant} a réservé un créneau pour le {date} à {horaire}."
    mail.send(msg)


# Fonction email de confirmation d'annulation
def send_cancellation_email(to_email, date, horaire):
    msg = Message("Annulation de votre réservation",
                recipients=[to_email])
    msg.body = f"Votre réservation pour le {date} à {horaire} a été annulée."
    mail.send(msg)

# Fonction email de notification d'annulation au formateur
def send_cancellation_notification_email(to_email, date, horaire, Alternant_id=None, nom_Alternant=None):
    msg = Message("Annulation de réservation de créneau",
                recipients=[to_email])
    if Alternant_id:
        msg.body = f"L'Alternant {nom_Alternant} a annulé sa réservation pour le {date} à {horaire}."
    else:
        msg.body = f"Le créneau pour le {date} à {horaire} a été annulé."
    mail.send(msg)

#--------------------------- CLASSES LIE A SQL ----------------------------------------

class LieuFormation:
    @staticmethod
    def get_lieux():
        conn = connect_db()
        conn =conn.cursor()
        conn.execute('SELECT * FROM Lieu_Formation')
        lieux = conn.fetchall()
        conn.close()
        return lieux

class Formation:
    @staticmethod
    def get_Formations():
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Formation')
        Formations = conn.fetchall()
        conn.close()
        return Formations

class Alternant:
    @staticmethod
    def get_Alternants():
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Alternants')
        Alternants = conn.fetchall()
        conn.close()
        return Alternants
    def get_Alternant_by_id(alt_id):
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Alternants WHERE id_Alternant = %s', (alt_id))
        Alternant = conn.fetchone()
        conn.close()
        return Alternant

class Formateur:
    @staticmethod
    def get_Formateurs():
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Formateurs')
        Formateurs = conn.fetchall()
        conn.close()
        return Formateurs
    def get_formateur_by_id(alt_id):
            conn = connect_db()
            conn = conn.cursor()
            conn.execute('SELECT * FROM Formateurs WHERE id_formateur = %s', (alt_id))
            Formateurs = conn.fetchone()
            conn.close()
            return Formateurs

class CreneauReservation:
    @staticmethod
    def get_creneaux_reserves(user_id):
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT Creneaux_Reservations.* , Formateurs.nom , Formateurs.prenom FROM Creneaux_Reservations INNER JOIN Formateurs ON Formateurs.id_formateur = Creneaux_Reservations.id_formateur WHERE Creneaux_Reservations.etat_reservation = 1')
        creneaux_reserves = conn.fetchall()
        conn.close()
        return creneaux_reserves

    @staticmethod
    def get_creneaux_reservables():
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Creneaux_Reservations WHERE etat_reservation = 0')
        creneaux_reservables = conn.fetchall()
        conn.close()
        return creneaux_reservables

#------------------------------------------- Routes -----------------------------------

@app.route('/')
def home():
    return render_template('home.jinja')  # Accueil




@app.route('/login', methods=['POST', 'GET'])
def login():
    id_false = 0
    if request.method == 'GET':
        return render_template('login.jinja')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password_MD5HASH = hashlib.md5(password.encode()).hexdigest()

        # Vérifier dans la table Alternants  ( pour login et redirect dashboard  )
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Alternants WHERE username=%s AND password=%s', (username, password_MD5HASH))
        Alternant = conn.fetchone()
        conn.close()

        if Alternant:
            session['user_id'] = Alternant[0]
            session['user_type'] = 'Alternant'
            return redirect(url_for('dashboard'))

        # Vérifier dans la table Formateurs ( pour login et redirect dashboard )
        conn = connect_db()
        conn = conn.cursor()
        conn.execute('SELECT * FROM Formateurs WHERE username=%s AND password=%s', (username, password_MD5HASH))
        formateur = conn.fetchone()
        conn.close()

        if formateur:
            session['user_id'] = formateur[0]
            session['user_type'] = 'Formateur'
            return redirect(url_for('dashboard'))

        id_false = 1
        return render_template('login.jinja', id_false=id_false)





@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    if user_id and user_type:
        if user_type == 'Alternant':
            #======Informations sur l'utilisateur connecté======
            infoFormateur = Formateur.get_Formateurs()
            infoUser = Alternant.get_Alternants()
            id_user = Alternant.get_Alternant_by_id(user_id)
            #===================================================
            creneaux_reserves = CreneauReservation.get_creneaux_reserves(user_id)
            creneaux_reservables = CreneauReservation.get_creneaux_reservables()

            return render_template('dashboard.jinja', formateurs=infoFormateur, id_user=id_user,creneau_reserve=creneaux_reserves, creneau_reservable=creneaux_reservables,user_type=user_type, infoUser=infoUser)

        elif user_type == 'Formateur':
            infoUser = Formateur.get_Formateurs()
            id_user = Formateur.get_formateur_by_id(user_id)
            infoUserAlternant = Alternant.get_Alternants()
            creneaux_proposes = CreneauReservation.get_creneaux_reservables()
            creneaux_reserves = CreneauReservation.get_creneaux_reserves(user_id)

            return render_template('dashboard.jinja',id_user=id_user,Alternant_info=infoUserAlternant, info_User=infoUser,creneau_propose=creneaux_proposes, creneau_reserve=creneaux_reserves,user_type=user_type)

    return redirect(url_for('login'))




@app.route('/ajouter_creneau', methods=['POST'])
def ajouter_creneau():
    conn = connect_db()
    if request.method == 'POST':
        date = request.form['date']
        horaire = request.form['horaire']
        formateur_id = int(session.get('user_id'))

        # Insert du créneau dans la BDD
        sql = "INSERT INTO Creneaux_Reservations (date_reservation, horaire_reservation, etat_reservation, id_formateur) VALUES (%s, %s,0, %s)"
        conn.cursor().execute(sql, (date, horaire, formateur_id))
        conn.commit()

    return redirect(url_for('dashboard'))




@app.route('/supprimer_creneau/<int:creneau_id>', methods=['POST'])
def supprimer_creneau(creneau_id):
    conn = connect_db()
    if request.method == 'POST':
            # Supprimer le créneau avec l'identifiant creneau_id de la table creneaux_reservables
            sql = "DELETE FROM Creneaux_Reservations WHERE id_reservation = %s"
            conn.cursor().execute(sql, (creneau_id,))
            conn.commit()

    return redirect(url_for('dashboard'))




@app.route('/annuler_creneau/<int:id_reservation>', methods=['POST'])
def annuler_creneau(id_reservation):
    conn = connect_db()
    try:
        cursor = conn.cursor()

        # Récupérer les détails de la réservation
        sql = "SELECT id_Alternant, id_formateur, date_reservation, horaire_reservation FROM Creneaux_Reservations WHERE id_reservation=%s"
        cursor.execute(sql, (id_reservation,))
        reservation = cursor.fetchone()

        if reservation:
            id_Alternant = reservation[0]
            id_formateur = reservation[1]
            date_reserved = reservation[2]
            horaire_reserved = reservation[3]

            # Mettre à jour ou annuler la réservation
            cursor.execute(
                'UPDATE Creneaux_Reservations SET id_Alternant=NULL, etat_reservation=0 WHERE id_reservation=%s',
                (id_reservation,)
            )
            conn.commit()

            # Récupérer les emails de l'Alternant et du formateur
            if id_Alternant:
                cursor.execute("SELECT nom FROM Alternants WHERE id_Alternant=%s",(id_Alternant,))
                nom_Alternant = cursor.fetchone()[0]
                cursor.execute("SELECT email FROM Alternants WHERE id_Alternant=%s", (id_Alternant,))
                Alternant_email = cursor.fetchone()[0]
                cursor.execute("SELECT email FROM Formateurs WHERE id_formateur=%s", (id_formateur,))
                formateur_email = cursor.fetchone()[0]


                # Envoyer les emails de confirmation et de notification
                send_cancellation_email(Alternant_email, date_reserved, horaire_reserved)
                send_cancellation_notification_email(formateur_email, date_reserved, horaire_reserved, id_Alternant, nom_Alternant)
            else:
                cursor.execute("SELECT email FROM Formateurs WHERE id_formateur=%s", (id_formateur,))
                formateur_email = cursor.fetchone()[0]

                # Envoyer l'email de notification uniquement au formateur
                send_cancellation_notification_email(formateur_email, date_reserved, horaire_reserved,nom_Alternant)

            flash('Réservation annulée avec succès.')
        else:
            flash('Réservation non trouvée.')
    finally:
        conn.close()

    return redirect(url_for('dashboard'))




@app.route('/get_reservations', methods=['GET'])
def get_reservations():
    formateur_id = request.args.get('formateur_id')
    if formateur_id:
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # SQL pour récupérer les dates de réservation disponibles d'un formateur choisi
            query = "SELECT DISTINCT DATE_FORMAT(date_reservation, '%%Y-%%m-%%d') FROM Creneaux_Reservations WHERE id_formateur = %s AND etat_reservation=%s AND date_reservation > NOW()"
            cursor.execute(query, (formateur_id,0))
            dates = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            return jsonify({'dates': dates}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Missing formateur_id parameter'}), 400



# Route pour récupérer les horaires disponibles pour un formateur et une date donné
@app.route('/get_horaires', methods=['GET'])
def get_horaires():
    formateur_id = request.args.get('formateur_id')
    date_selected = request.args.get('date')
    if formateur_id:
        try:
            # Connexion à la base de données
            conn = connect_db()
            cursor = conn.cursor()

            # Requête SQL pour récupérer les dates de réservation disponibles pour un formateur
            query = "SELECT DISTINCT horaire_reservation FROM Creneaux_Reservations WHERE id_formateur = %s AND date_reservation = %s AND etat_reservation =%s"
            cursor.execute(query, (formateur_id, date_selected,0))
            horaires = [row[0] for row in cursor.fetchall()]

            # Fermeture de la connexion et envoi des dates au client (JS par andré)
            cursor.close()
            conn.close()

            return jsonify({'horaires': horaires}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Missing formateur_id parameter'}), 400





@app.route('/prendre_RDV', methods=['POST', 'GET'])
def priserdv():
    user_id = session.get('user_id')
    date_reserved = request.form['date']
    horaire_reserved = request.form['horaire']
    formateur_reserved = request.form['formateur_id']
    conn = connect_db()

    # Récupérer les inFormations de l'Alternant et du formateur
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Alternants WHERE id_Alternant=%s", (user_id,))
    Alternant_email = cursor.fetchone()[0]
    cursor.execute("SELECT nom FROM Alternants WHERE id_Alternant=%s",(user_id,))
    nom_Alternant = cursor.fetchone()[0]
    
    cursor.execute("SELECT email FROM Formateurs WHERE id_formateur=%s", (formateur_reserved,))
    formateur_email = cursor.fetchone()[0]

    # Insérer la réservation dans la base de données
    sql = """
    SELECT id_reservation FROM Creneaux_Reservations 
    WHERE date_reservation=%s AND horaire_reservation=%s AND etat_reservation=%s AND id_formateur=%s
    """
    cursor.execute(sql, (date_reserved, horaire_reserved, 0, formateur_reserved))
    id_reservation = cursor.fetchone()[0]

    # Mettre à jour l'état de la réservation
    cursor.execute(
        'UPDATE Creneaux_Reservations SET id_Alternant=%s, etat_reservation=%s WHERE id_reservation=%s',
        (user_id, 1, id_reservation)
    )
    conn.commit()
    conn.close()

    # Envoi des emails
    send_confirmation_email(Alternant_email, date_reserved, horaire_reserved)
    send_notification_email(formateur_email, date_reserved, horaire_reserved, nom_Alternant)

    return redirect(url_for('dashboard'))



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
