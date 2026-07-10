# backend/controllers/user_controller.py
from database import utilisateur_dao


def lister_utilisateurs():
    return utilisateur_dao.lister_utilisateurs()