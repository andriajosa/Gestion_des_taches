
class Utilisateur:
    """Represente un utilisateur de l'application.
    Cette classe ne contient aucune logique SQL : elle sert juste
    a manipuler les donnees d'un utilisateur de facon structuree."""

    def __init__(self, id_utilisateur, nom_utilisateur, email, role):
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.email = email
        self.role = role

    def est_admin(self):
        return self.role == "admin"

    @staticmethod
    def depuis_ligne_sql(ligne):
        return Utilisateur(
            id_utilisateur=ligne["id_utilisateur"],
            nom_utilisateur=ligne["nom_utilisateur"],
            email=ligne["email"],
            role=ligne["role"]
        )