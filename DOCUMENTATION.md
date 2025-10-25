# Documentation du Projet Santé Admin

## Vue d'ensemble

Le projet **Santé Admin** est une application web développée avec Flask pour la gestion administrative d'un système de santé. Elle permet de gérer les médecins, les patients et les rendez-vous médicaux de manière centralisée et sécurisée.

## Fonctionnalités principales

### Gestion des médecins
- Ajout, modification et suppression de médecins
- Gestion des spécialités médicales
- Attribution de cabinets médicaux
- Configuration des disponibilités hebdomadaires

### Gestion des patients
- Enregistrement des informations personnelles des patients
- Historique des rendez-vous par patient
- Modification des données patient

### Gestion des rendez-vous
- Planification de rendez-vous médicaux
- Association patient-médecin
- Suivi du statut des rendez-vous (à venir/effectué)
- Ajout de notes médicales

### Système d'authentification
- Connexion sécurisée avec nom d'utilisateur et mot de passe
- Session utilisateur persistante
- Accès protégé aux fonctionnalités administratives

### Tableau de bord
- Statistiques générales (nombre de médecins, patients, rendez-vous)
- Affichage des derniers rendez-vous
- Navigation intuitive vers toutes les fonctionnalités

## Technologies utilisées

- **Backend :** Python Flask
- **Base de données :** SQLite avec SQLAlchemy
- **Frontend :** HTML5, CSS3, Jinja2 templates
- **Sécurité :** Werkzeug (hachage des mots de passe)
- **Interface :** Bootstrap (via CSS personnalisé)

## Structure du projet

```
projet_santé_admin/
├── app.py                      # Application principale Flask
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation de base
├── DOCUMENTATION.md            # Cette documentation
├── .gitignore                  # Fichiers à ignorer par Git
├── instance/                   # Base de données SQLite
├── static/                     # Fichiers statiques
│   └── css/
│       └── style.css          # Styles CSS personnalisés
└── templates/                  # Templates HTML
    ├── base.html              # Template de base
    ├── login.html             # Page de connexion
    ├── dashboard.html         # Tableau de bord
    ├── medecins.html          # Liste des médecins
    ├── patients.html          # Liste des patients
    ├── ajouter_medecin.html   # Formulaire ajout médecin
    ├── ajouter_patient.html   # Formulaire ajout patient
    ├── ajouter_rendez_vous.html # Formulaire ajout RDV
    ├── modifier_medecin.html  # Formulaire modification médecin
    ├── modifier_patient.html  # Formulaire modification patient
    ├── modifier_rendez_vous.html # Formulaire modification RDV
    └── disponibilite.html     # Gestion disponibilités médecin
```

## Installation et configuration

### Prérequis
- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <url-du-repo>
   cd projet_santé_admin
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Sur Windows
   # ou
   source venv/bin/activate  # Sur Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   python app.py
   ```

5. **Accéder à l'application**
   Ouvrir un navigateur web et aller à l'adresse : `http://127.0.0.1:5000`

### Configuration de la base de données

L'application utilise SQLite comme base de données. Le fichier de base de données `sante_ci.db` sera automatiquement créé dans le dossier `instance/` lors du premier lancement.

**Utilisateur par défaut :**
- Nom d'utilisateur : `admin`
- Mot de passe : `sante123`

## Modèles de données

### Utilisateur
- `id` : Identifiant unique
- `username` : Nom d'utilisateur (unique)
- `password_hash` : Mot de passe haché

### Médecin
- `id` : Identifiant unique
- `nom` : Nom du médecin
- `prenom` : Prénom du médecin
- `specialite` : Spécialité médicale
- `cabinet` : Adresse du cabinet
- `disponibilites` : Jours de disponibilité (stockés en chaîne séparée par des virgules)

### Patient
- `id` : Identifiant unique
- `nom` : Nom du patient
- `prenom` : Prénom du patient
- `age` : Âge du patient
- `telephone` : Numéro de téléphone
- `email` : Adresse email

### RendezVous
- `id` : Identifiant unique
- `patient_id` : Référence vers le patient
- `medecin_id` : Référence vers le médecin
- `date` : Date et heure du rendez-vous
- `effectue` : Statut du rendez-vous (booléen)
- `notes` : Notes médicales

## Routes et fonctionnalités

### Routes d'authentification
- `GET/POST /login` : Connexion utilisateur
- `GET /logout` : Déconnexion

### Routes principales
- `GET /` : Redirection vers le dashboard (si connecté) ou login
- `GET /dashboard` : Tableau de bord avec statistiques

### Gestion des médecins
- `GET /medecins` : Liste des médecins
- `GET /ajouter_medecin` : Formulaire d'ajout de médecin
- `POST /ajouter_medecin` : Traitement de l'ajout
- `GET /modifier_medecin/<id>` : Formulaire de modification
- `POST /modifier_medecin/<id>` : Traitement de la modification
- `GET /supprimer_medecin/<id>` : Suppression d'un médecin
- `GET/POST /disponibilite/<id>` : Gestion des disponibilités

### Gestion des patients
- `GET /patients` : Liste des patients
- `GET /patient/<id>` : Détails d'un patient et ses RDV
- `GET /ajouter_patient` : Formulaire d'ajout de patient
- `POST /ajouter_patient` : Traitement de l'ajout
- `GET /modifier_patient/<id>` : Formulaire de modification
- `POST /modifier_patient/<id>` : Traitement de la modification
- `GET /supprimer_patient/<id>` : Suppression d'un patient

### Gestion des rendez-vous
- `GET /ajouter_rendez_vous` : Formulaire d'ajout de RDV
- `POST /ajouter_rendez_vous` : Traitement de l'ajout
- `GET /modifier_rendez_vous/<id>` : Formulaire de modification
- `POST /modifier_rendez_vous/<id>` : Traitement de la modification
- `GET /supprimer_rendez_vous/<id>` : Suppression d'un RDV

## Utilisation de l'application

### Première connexion
1. Accéder à `http://127.0.0.1:5000`
2. Se connecter avec les identifiants par défaut :
   - Utilisateur : `admin`
   - Mot de passe : `sante123`

### Navigation
- Utiliser la barre de navigation pour accéder aux différentes sections
- Le tableau de bord affiche un aperçu général
- Les boutons d'action permettent d'ajouter, modifier ou supprimer des éléments

### Gestion des données
- **Médecins :** Commencer par ajouter des médecins avec leurs spécialités
- **Patients :** Enregistrer les patients avec leurs informations de contact
- **Rendez-vous :** Planifier des RDV en associant patients et médecins

## Sécurité

- Les mots de passe sont hachés avec Werkzeug
- L'accès aux fonctionnalités nécessite une authentification
- Les sessions utilisateur sont gérées automatiquement
- Protection CSRF basique via les formulaires Flask

## Personnalisation

### Styles CSS
Les styles sont définis dans `static/css/style.css`. Vous pouvez les modifier pour personnaliser l'apparence.

### Configuration
La configuration de l'application se trouve dans `app.py` :
- Clé secrète pour les sessions
- Configuration de la base de données
- Paramètres Flask

## Dépannage

### Problèmes courants

1. **Erreur de base de données**
   - Supprimer le fichier `instance/sante_ci.db`
   - Relancer l'application pour recréer la base

2. **Erreur de dépendances**
   - Vérifier que toutes les dépendances sont installées : `pip install -r requirements.txt`

3. **Port déjà utilisé**
   - Changer le port dans `app.run(debug=True, port=5001)`

### Logs
Les logs de l'application sont affichés dans la console lors de l'exécution en mode debug.

## Contribution

Pour contribuer au projet :
1. Forker le repository
2. Créer une branche pour vos modifications
3. Commiter vos changements
4. Pousser vers votre fork
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Support

Pour toute question ou problème, veuillez contacter l'équipe de développement ou créer une issue sur le repository GitHub.

---

**Version :** 1.0
**Dernière mise à jour :** Octobre 2024
**Auteur :** Équipe de développement Santé Admin
