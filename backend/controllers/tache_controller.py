from database import taches_dao
from database.historique_dao import ajouter_entree
from security.encryption import chiffrer_texte, dechiffrer_texte


def creer_tache(titre, description, priority, due_date, categorie_id, created_by, assigned_to):
    description_chiffree = chiffrer_texte(description)
    id_tache = taches_dao.creer_tache(
        titre, description_chiffree, priority, due_date, categorie_id, created_by, assigned_to
    )
    ajouter_entree(created_by, f"Creation de la tache #{id_tache}")
    return id_tache


def lister_taches(utilisateur_courant):
    if utilisateur_courant["role"] == "admin":
        taches = taches_dao.lister_taches()
    else:
        taches = taches_dao.lister_taches(utilisateur_courant["id_utilisateur"])

    for tache in taches:
        tache["description"] = dechiffrer_texte(tache["description"])
    return taches


def modifier_tache(id_tache, champs, id_utilisateur):
    if "description" in champs:
        champs["description"] = chiffrer_texte(champs["description"])
    succes = taches_dao.modifier_tache(id_tache, champs)
    if succes:
        ajouter_entree(id_utilisateur, f"Modification de la tache #{id_tache}")
    return succes


def supprimer_tache(id_tache, id_utilisateur):
    succes = taches_dao.supprimer_tache(id_tache)
    if succes:
        ajouter_entree(id_utilisateur, f"Suppression de la tache #{id_tache}")
    return succes