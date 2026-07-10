from database.connexion import obtenir_connexion


def ajouter_entree(user_id, action):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO historique (user_id, action) VALUES (%s, %s)",
        (user_id, action)
    )
    connexion.commit()
    curseur.close()
    connexion.close()


def lister_historique(user_id=None):
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)

    requete_base = """
        SELECT h.id_historique, h.user_id, u.nom_utilisateur,
               h.action, h.timestamp AS date_action
        FROM historique h
        LEFT JOIN utilisateur u ON h.user_id = u.id_utilisateur
    """

    if user_id:
        curseur.execute(requete_base + " WHERE h.user_id = %s ORDER BY h.timestamp DESC", (user_id,))
    else:
        curseur.execute(requete_base + " ORDER BY h.timestamp DESC")

    resultats = curseur.fetchall()
    curseur.close()
    connexion.close()
    return resultats