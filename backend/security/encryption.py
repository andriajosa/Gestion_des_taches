from cryptography.fernet import Fernet
from config.settings import FERNET_KEY

_moteur_chiffrement = Fernet(FERNET_KEY)


def chiffrer_texte(texte_clair):
    if not texte_clair:
        return texte_clair
    return _moteur_chiffrement.encrypt(texte_clair.encode()).decode()


def dechiffrer_texte(texte_chiffre):
    if not texte_chiffre:
        return texte_chiffre
    return _moteur_chiffrement.decrypt(texte_chiffre.encode()).decode()