import re

EMAIL_REGEX = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")


def email_valide(email):
    return bool(EMAIL_REGEX.match(email or ""))


def mot_de_passe_valide(mot_de_passe):
    return bool(mot_de_passe) and len(mot_de_passe) >= 6


def titre_tache_valide(titre):
    return bool(titre) and len(titre.strip()) > 0