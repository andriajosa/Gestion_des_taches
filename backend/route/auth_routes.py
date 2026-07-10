from flask import Blueprint, request, jsonify
from controllers import auth_controller

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/inscription", methods=["POST"])
def inscription():
    donnees = request.get_json()
    id_utilisateur, erreur = auth_controller.inscrire(
        donnees.get("nom_utilisateur"),
        donnees.get("email"),
        donnees.get("mot_de_passe"),
        donnees.get("role")
    )
    if erreur:
        return jsonify({"erreur": erreur}), 400
    return jsonify({"message": "Compte cree", "id_utilisateur": id_utilisateur}), 201


@auth_bp.route("/connexion", methods=["POST"])
def connexion():
    donnees = request.get_json()
    resultat, erreur = auth_controller.connecter(donnees.get("email"), donnees.get("mot_de_passe"))
    if erreur:
        return jsonify({"erreur": erreur}), 401
    return jsonify(resultat), 200