# backend/database/utilisateur_dao.py
from database.connexion import obtenir_connexion


def creer_utilisateur(nom_utilisateur, email, password_hash, role="utilisateur"):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    requete = """INSERT INTO utilisateur (nom_utilisateur, email, password_hash, role) VALUES (%s, %s, %s, %s)"""
    curseur.execute(requete, (nom_utilisateur, email, password_hash, role))
    connexion.commit()
    id_cree = curseur.lastrowid
    curseur.close()
    connexion.close()
    return id_cree


def trouver_par_email(email):
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
    resultat = curseur.fetchone()
    curseur.close()
    connexion.close()
    return resultat


def trouver_par_id(id_utilisateur):
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT * FROM utilisateur WHERE id_utilisateur = %s", (id_utilisateur,))
    resultat = curseur.fetchone()
    curseur.close()
    connexion.close()
    return resultat


def lister_utilisateurs():
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT id_utilisateur, nom_utilisateur, email, role FROM utilisateur")
    resultats = curseur.fetchall()
    curseur.close()
    connexion.close()
    return resultats