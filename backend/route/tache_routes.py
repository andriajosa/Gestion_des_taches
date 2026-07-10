from flask import Blueprint, request, jsonify
from controllers import tache_controller
from security.decorators import token_requis

task_bp = Blueprint("taches", __name__, url_prefix="/api/taches")


@task_bp.route("", methods=["GET"])
@token_requis
def obtenir_taches():
    taches = tache_controller.lister_taches(request.utilisateur_courant)
    return jsonify(taches), 200


@task_bp.route("", methods=["POST"])
@token_requis
def ajouter_tache():
    donnees = request.get_json()
    id_utilisateur = request.utilisateur_courant["id_utilisateur"]
    id_tache = tache_controller.creer_tache(
        donnees.get("titre"),
        donnees.get("description"),
        donnees.get("priority", "moyenne"),
        donnees.get("due_date"),
        donnees.get("categorie_id"),
        id_utilisateur,
        donnees.get("assigned_to")
    )
    return jsonify({"message": "Tache creee", "id_tache": id_tache}), 201


@task_bp.route("/<int:id_tache>", methods=["PUT"])
@token_requis
def mettre_a_jour_tache(id_tache):
    donnees = request.get_json()
    id_utilisateur = request.utilisateur_courant["id_utilisateur"]
    succes = tache_controller.modifier_tache(id_tache, donnees, id_utilisateur)
    if not succes:
        return jsonify({"erreur": "Tache introuvable"}), 404
    return jsonify({"message": "Tache modifiee"}), 200


@task_bp.route("/<int:id_tache>", methods=["DELETE"])
@token_requis
def retirer_tache(id_tache):
    id_utilisateur = request.utilisateur_courant["id_utilisateur"]
    succes = tache_controller.supprimer_tache(id_tache, id_utilisateur)
    if not succes:
        return jsonify({"erreur": "Tache introuvable"}), 404
    return jsonify({"message": "Tache supprimee"}), 200