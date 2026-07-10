from database.connexion import obtenir_connexion


def creer_categorie(nom_categorie, created_by):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO categories (nom_categorie, created_by) VALUES (%s, %s)",
        (nom_categorie, created_by)
    )
    connexion.commit()
    id_cree = curseur.lastrowid
    curseur.close()
    connexion.close()
    return id_cree


def lister_categories():
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT * FROM categories")
    resultats = curseur.fetchall()
    curseur.close()
    connexion.close()
    return resultats


def supprimer_categorie(id_categories):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM categories WHERE id_categories = %s", (id_categories,))
    connexion.commit()
    lignes_affectees = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes_affectees > 0