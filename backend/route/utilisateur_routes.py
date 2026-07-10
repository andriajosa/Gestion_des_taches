from flask import Blueprint, jsonify
from controllers import utilisateur_controller
from security.decorators import token_requis, admin_requis

user_bp = Blueprint("utilisateurs", __name__, url_prefix="/api/utilisateurs")


@user_bp.route("", methods=["GET"])
@token_requis
@admin_requis
def obtenir_utilisateurs():
    return jsonify(utilisateur_controller.lister_utilisateurs()), 200