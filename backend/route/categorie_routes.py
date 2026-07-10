from flask import Blueprint, request, jsonify
from controllers import categorie_controller
from security.decorators import token_requis

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@category_bp.route("", methods=["GET"])
@token_requis
def obtenir_categories():
    return jsonify(categorie_controller.lister_categories()), 200


@category_bp.route("", methods=["POST"])
@token_requis
def ajouter_categorie():
    donnees = request.get_json()
    id_utilisateur = request.utilisateur_courant["id_utilisateur"]
    id_categorie = categorie_controller.creer_categorie(donnees.get("nom_categorie"), id_utilisateur)
    return jsonify({"message": "Categorie creee", "id_categories": id_categorie}), 201


@category_bp.route("/<int:id_categories>", methods=["DELETE"])
@token_requis
def retirer_categorie(id_categories):
    succes = categorie_controller.supprimer_categorie(id_categories)
    if not succes:
        return jsonify({"erreur": "Categorie introuvable"}), 404
    return jsonify({"message": "Categorie supprimee"}), 200