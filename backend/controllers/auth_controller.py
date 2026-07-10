from database import utilisateur_dao
from security.password_manager import hacher_mot_de_passe, verifier_mot_de_passe
from security.jwt_manager import generer_token
from database.historique_dao import ajouter_entree


def inscrire(nom_utilisateur, email, mot_de_passe, role="utilisateur"):
    if utilisateur_dao.trouver_par_email(email):
        return None, "Un compte existe deja avec cet email"

    mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)
    id_utilisateur = utilisateur_dao.creer_utilisateur(nom_utilisateur, email, mot_de_passe_hache, role)
    ajouter_entree(id_utilisateur, "Creation du compte")
    return id_utilisateur, None


def connecter(email, mot_de_passe):
    utilisateur = utilisateur_dao.trouver_par_email(email)
    if not utilisateur:
        return None, "Email ou mot de passe incorrect"

    if not verifier_mot_de_passe(mot_de_passe, utilisateur["password_hash"]):
        return None, "Email ou mot de passe incorrect"

    token = generer_token(utilisateur["id_utilisateur"], utilisateur["role"])
    ajouter_entree(utilisateur["id_utilisateur"], "Connexion")

    infos_utilisateur = {
        "id_utilisateur": utilisateur["id_utilisateur"],
        "nom_utilisateur": utilisateur["nom_utilisateur"],
        "email": utilisateur["email"],
        "role": utilisateur["role"]
    }

    return {"token": token, "utilisateur": infos_utilisateur}, None