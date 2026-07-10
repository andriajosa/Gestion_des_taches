import jwt
import datetime
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS


def generer_token(id_utilisateur, role):
    charge_utile = {
        "id_utilisateur": id_utilisateur,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(charge_utile, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decoder_token(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])