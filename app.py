from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_tres_securisee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sante_ci.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèles de base de données
class Medecin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)
    cabinet = db.Column(db.String(100), nullable=False)
    disponibilites = db.Column(db.String(200))  # Stocké comme string séparé par des virgules
    rendez_vous = db.relationship('RendezVous', backref='medecin', lazy=True)

    def get_disponibilites_list(self):
        if self.disponibilites:
            return self.disponibilites.split(',')
        return []

    def set_disponibilites_list(self, jours_list):
        self.disponibilites = ','.join(jours_list)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    effectue = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Initialiser la base de données et créer des données de test
def init_db():
    with app.app_context():
        db.create_all()

        # Vérifier si des données existent déjà
        if Utilisateur.query.filter_by(username='admin').first() is None:
            # Créer un utilisateur admin
            admin = Utilisateur(username='admin')
            admin.set_password('sante123')
            db.session.add(admin)
            db.session.commit()

# Routes
@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Utilisateur.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    stats = {
        'nb_medecins': Medecin.query.count(),
        'nb_patients': Patient.query.count(),
        'nb_rendez_vous': RendezVous.query.count()
    }

    # Récupérer les 5 derniers rendez-vous
    recent_rv = RendezVous.query.order_by(RendezVous.date.desc()).limit(5).all()

    # Préparer les données pour l'affichage
    rv_display = []
    for rv in recent_rv:
        rv_display.append({
            'id': rv.id,
            'medecin_nom': f"{rv.medecin.prenom} {rv.medecin.nom}",
            'patient_nom': f"{rv.patient.prenom} {rv.patient.nom}",
            'date_formatted': rv.date.strftime("%d/%m/%Y %H:%M"),
            'effectue': rv.effectue
        })

    return render_template('dashboard.html', stats=stats, recent_rv=rv_display)

@app.route('/medecins')
def liste_medecins():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    medecins = Medecin.query.all()

    # Préparer les données pour l'affichage
    medecins_display = []
    for m in medecins:
        medecins_display.append({
            'id': m.id,
            'nom': m.nom,
            'prenom': m.prenom,
            'specialite': m.specialite,
            'cabinet': m.cabinet,
            'disponibilites': m.get_disponibilites_list()
        })

    return render_template('medecins.html', medecins=medecins_display)

@app.route('/disponibilite/<int:id>', methods=['GET', 'POST'])
def disponibilite(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    medecin = Medecin.query.get_or_404(id)

    if request.method == 'POST':
        jours = request.form.getlist('jours')
        medecin.set_disponibilites_list(jours)
        db.session.commit()
        flash('Disponibilités mises à jour avec succès', 'success')
        return redirect(url_for('disponibilite', id=id))

    medecin_data = {
        'id': medecin.id,
        'nom': medecin.nom,
        'prenom': medecin.prenom,
        'specialite': medecin.specialite,
        'cabinet': medecin.cabinet,
        'disponibilites': medecin.get_disponibilites_list()
    }

    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    return render_template('disponibilite.html', medecin=medecin_data, jours_semaine=jours_semaine)

@app.route('/patients')
def liste_patients():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/patient/<int:id>')
def patient(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)

    # Récupérer les rendez-vous du patient
    rv_patient = RendezVous.query.filter_by(patient_id=id).order_by(RendezVous.date.desc()).all()

    # Préparer les données pour l'affichage
    rv_display = []
    for rv in rv_patient:
        rv_display.append({
            'id': rv.id,
            'medecin_nom': f"{rv.medecin.prenom} {rv.medecin.nom}",
            'date_formatted': rv.date.strftime("%d/%m/%Y %H:%M"),
            'effectue': rv.effectue
        })

    return render_template('patient.html', patient=patient, rendez_vous=rv_display)

@app.route('/ajouter_medecin', methods=['GET', 'POST'])
def ajouter_medecin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        specialite = request.form.get('specialite')
        cabinet = request.form.get('cabinet')

        medecin = Medecin(nom=nom, prenom=prenom, specialite=specialite, cabinet=cabinet)
        db.session.add(medecin)
        db.session.commit()

        flash('Médecin ajouté avec succès', 'success')
        return redirect(url_for('liste_medecins'))

    return render_template('ajouter_medecin.html')

@app.route('/ajouter_patient', methods=['GET', 'POST'])
def ajouter_patient():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        age = request.form.get('age')
        telephone = request.form.get('telephone')
        email = request.form.get('email')

        patient = Patient(nom=nom, prenom=prenom, age=age, telephone=telephone, email=email)
        db.session.add(patient)
        db.session.commit()

        flash('Patient ajouté avec succès', 'success')
        return redirect(url_for('liste_patients'))

    return render_template('ajouter_patient.html')

@app.route('/ajouter_rendez_vous', methods=['GET', 'POST'])
def ajouter_rendez_vous():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        medecin_id = request.form.get('medecin_id')
        date_str = request.form.get('date')
        notes = request.form.get('notes')

        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        rv = RendezVous(patient_id=patient_id, medecin_id=medecin_id, date=date, notes=notes)
        db.session.add(rv)
        db.session.commit()

        flash('Rendez-vous ajouté avec succès', 'success')
        return redirect(url_for('dashboard'))

    patients = Patient.query.all()
    medecins = Medecin.query.all()
    return render_template('ajouter_rendez_vous.html', patients=patients, medecins=medecins)

@app.route('/supprimer_medecin/<int:id>')
def supprimer_medecin(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    medecin = Medecin.query.get_or_404(id)
    # Supprimer les rendez-vous associés d'abord
    RendezVous.query.filter_by(medecin_id=id).delete()
    db.session.delete(medecin)
    db.session.commit()

    flash('Médecin supprimé avec succès', 'success')
    return redirect(url_for('liste_medecins'))

@app.route('/supprimer_patient/<int:id>')
def supprimer_patient(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)
    # Supprimer les rendez-vous associés d'abord
    RendezVous.query.filter_by(patient_id=id).delete()
    db.session.delete(patient)
    db.session.commit()

    flash('Patient supprimé avec succès', 'success')
    return redirect(url_for('liste_patients'))

@app.route('/supprimer_rendez_vous/<int:id>')
def supprimer_rendez_vous(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    rv = RendezVous.query.get_or_404(id)
    db.session.delete(rv)
    db.session.commit()

    flash('Rendez-vous supprimé avec succès', 'success')
    return redirect(url_for('dashboard'))

@app.route('/modifier_medecin/<int:id>', methods=['GET', 'POST'])
def modifier_medecin(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    medecin = Medecin.query.get_or_404(id)

    if request.method == 'POST':
        medecin.nom = request.form.get('nom')
        medecin.prenom = request.form.get('prenom')
        medecin.specialite = request.form.get('specialite')
        medecin.cabinet = request.form.get('cabinet')
        db.session.commit()

        flash('Médecin modifié avec succès', 'success')
        return redirect(url_for('liste_medecins'))

    return render_template('modifier_medecin.html', medecin=medecin)

@app.route('/modifier_patient/<int:id>', methods=['GET', 'POST'])
def modifier_patient(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.nom = request.form.get('nom')
        patient.prenom = request.form.get('prenom')
        patient.age = request.form.get('age')
        patient.telephone = request.form.get('telephone')
        patient.email = request.form.get('email')
        db.session.commit()

        flash('Patient modifié avec succès', 'success')
        return redirect(url_for('liste_patients'))

    return render_template('modifier_patient.html', patient=patient)

@app.route('/modifier_rendez_vous/<int:id>', methods=['GET', 'POST'])
def modifier_rendez_vous(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    rv = RendezVous.query.get_or_404(id)

    if request.method == 'POST':
        rv.patient_id = request.form.get('patient_id')
        rv.medecin_id = request.form.get('medecin_id')
        date_str = request.form.get('date')
        rv.date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        rv.notes = request.form.get('notes')
        rv.effectue = 'effectue' in request.form
        db.session.commit()

        flash('Rendez-vous modifié avec succès', 'success')
        return redirect(url_for('dashboard'))

    patients = Patient.query.all()
    medecins = Medecin.query.all()
    return render_template('modifier_rendez_vous.html', rv=rv, patients=patients, medecins=medecins)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
