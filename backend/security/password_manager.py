from werkzeug.security import generate_password_hash, check_password_hash


def hacher_mot_de_passe(mot_de_passe_clair):
    #Transforme un mot de passe en clair en une empreinte irreversible
    #On ne stocke jamais un mot de passe en clair dans la base de donnees
    return generate_password_hash(mot_de_passe_clair)


def verifier_mot_de_passe(mot_de_passe_clair, mot_de_passe_hache):
    return check_password_hash(mot_de_passe_hache, mot_de_passe_clair)