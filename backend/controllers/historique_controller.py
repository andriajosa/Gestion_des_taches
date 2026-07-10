from database import historique_dao


def lister_historique(utilisateur_courant):
    if utilisateur_courant["role"] == "admin":
        return historique_dao.lister_historique()
    return historique_dao.lister_historique(utilisateur_courant["id_utilisateur"])