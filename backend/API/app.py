from flask import Flask
from route.auth_routes import auth_bp
from route.tache_routes import task_bp
from route.categorie_routes import category_bp
from route.utilisateur_routes import user_bp
from route.historique_routes import history_bp


def creer_application():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(history_bp)

    return app