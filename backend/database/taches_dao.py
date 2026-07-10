# backend/database/tache_dao.py
from database.connexion import obtenir_connexion


def creer_tache(titre, description, priority, due_date, categorie_id, created_by, assigned_to):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    requete = """INSERT INTO taches
                 (titre, description, priority, statut, due_date, categorie_id, created_by, assigned_to)
                 VALUES (%s, %s, %s, 'a_faire', %s, %s, %s, %s)"""
    curseur.execute(requete, (titre, description, priority, due_date, categorie_id, created_by, assigned_to))
    connexion.commit()
    id_cree = curseur.lastrowid
    curseur.close()
    connexion.close()
    return id_cree


def lister_taches(id_utilisateur=None):
    """Si id_utilisateur est fourni, ne retourne que les taches liees a cet utilisateur
    (creees par lui ou qui lui sont assignees). Sinon, retourne toutes les taches (admin)."""
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    if id_utilisateur:
        curseur.execute(
            "SELECT * FROM taches WHERE created_by = %s OR assigned_to = %s",
            (id_utilisateur, id_utilisateur)
        )
    else:
        curseur.execute("SELECT * FROM taches")
    resultats = curseur.fetchall()
    curseur.close()
    connexion.close()
    return resultats


def trouver_tache_par_id(id_tache):
    connexion = obtenir_connexion()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT * FROM taches WHERE id_tache = %s", (id_tache,))
    resultat = curseur.fetchone()
    curseur.close()
    connexion.close()
    return resultat


def modifier_tache(id_tache, champs):
    """champs est un dictionnaire {nom_colonne: nouvelle_valeur}.
    On construit dynamiquement la requete UPDATE pour ne modifier que les champs fournis."""
    if not champs:
        return False
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    colonnes = ", ".join(f"{cle} = %s" for cle in champs.keys())
    valeurs = list(champs.values()) + [id_tache]
    curseur.execute(f"UPDATE taches SET {colonnes} WHERE id_tache = %s", valeurs)
    connexion.commit()
    lignes_affectees = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes_affectees > 0


def supprimer_tache(id_tache):
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM taches WHERE id_tache = %s", (id_tache,))
    connexion.commit()
    lignes_affectees = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes_affectees > 0