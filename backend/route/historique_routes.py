from flask import Blueprint, request, jsonify
from controllers import historique_controller
from security.decorators import token_requis

history_bp = Blueprint("historique", __name__, url_prefix="/api/historique")


@history_bp.route("", methods=["GET"])
@token_requis
def obtenir_historique():
    return jsonify(historique_controller.lister_historique(request.utilisateur_courant)), 200