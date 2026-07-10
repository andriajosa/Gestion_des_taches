from functools import wraps
from flask import request, jsonify
from security.jwt_manager import decoder_token
import jwt as pyjwt


def token_requis(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        en_tete = request.headers.get("Authorization", "")
        if not en_tete.startswith("Bearer "):
            return jsonify({"erreur": "Token manquant"}), 401

        token = en_tete.split(" ")[1]
        try:
            donnees_token = decoder_token(token)
        except pyjwt.ExpiredSignatureError:
            return jsonify({"erreur": "Token expire"}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"erreur": "Token invalide"}), 401

        request.utilisateur_courant = donnees_token
        return fonction(*args, **kwargs)
    return enveloppe


def admin_requis(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        if request.utilisateur_courant.get("role") != "admin":
            return jsonify({"erreur": "Acces reserve aux administrateurs"}), 403
        return fonction(*args, **kwargs)
    return enveloppe