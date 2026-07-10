from database import categorie_dao


def creer_categorie(nom_categorie, created_by):
    return categorie_dao.creer_categorie(nom_categorie, created_by)


def lister_categories():
    return categorie_dao.lister_categories()


def supprimer_categorie(id_categories):
    return categorie_dao.supprimer_categorie(id_categories)