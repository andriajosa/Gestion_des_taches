import requests
from config import API_BASE_URL


class ApiClient:
    def __init__(self):
        self.token = None
        self.utilisateur = None
    #en tête HTTP
    def _headers(self):
        headers = {
            "Content-Type": "application/json"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    #authentification
    def connexion(self, email, mot_de_passe):
        corps = {
            "email": email,
            "mot_de_passe": mot_de_passe
        }

        try:
            reponse = requests.post(
                f"{API_BASE_URL}/auth/connexion",
                json=corps
            )

            if reponse.status_code == 200:
                donnees = reponse.json()

                self.token = donnees.get("token")
                self.utilisateur = donnees.get("utilisateur")

                return True, None

            return False, reponse.json().get(
                "erreur",
                "Email ou mot de passe incorrect."
            )

        except requests.exceptions.ConnectionError:
            return False, "Impossible de joindre le serveur."

    #inscription
    def inscription(
            self,
            nom_utilisateur,
            email,
            mot_de_passe,
            role):

        corps = {
            "nom_utilisateur": nom_utilisateur,
            "email": email,
            "mot_de_passe": mot_de_passe,
            "role": role
        }

        try:

            reponse = requests.post(
                f"{API_BASE_URL}/auth/inscription",
                json=corps
            )

            if reponse.status_code == 201:
                return True, None

            return False, reponse.json().get(
                "erreur",
                "Erreur lors de l'inscription."
            )

        except requests.exceptions.ConnectionError:
            return False, "Serveur inaccessible."

    #deconnexion
    def deconnexion(self):
        self.token = None
        self.utilisateur = None

    #utilisateur connecté
    def utilisateur_connecte(self):
        return self.utilisateur

    #taches
    def obtenir_taches(self):

        try:

            reponse = requests.get(
                f"{API_BASE_URL}/taches",
                headers=self._headers()
            )

            if reponse.status_code == 200:
                return reponse.json()

            return []

        except:
            return []

    #creer tache
    def creer_tache(
            self,
            titre,
            description,
            priority,
            due_date,
            categorie_id,
            assigned_to):

        corps = {

            "titre": titre,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "categorie_id": categorie_id,
            "assigned_to": assigned_to

        }

        reponse = requests.post(

            f"{API_BASE_URL}/taches",

            json=corps,

            headers=self._headers()

        )

        return reponse.status_code == 201

    #modifier_tache
    def modifier_tache(self, id_tache, champs):

        reponse = requests.put(

            f"{API_BASE_URL}/taches/{id_tache}",

            json=champs,

            headers=self._headers()

        )

        return reponse.status_code == 200

    #supprimer tache
    def supprimer_tache(self, id_tache):

        reponse = requests.delete(

            f"{API_BASE_URL}/taches/{id_tache}",

            headers=self._headers()

        )

        return reponse.status_code == 200

    #categorie
    def obtenir_categories(self):

        try:

            reponse = requests.get(

                f"{API_BASE_URL}/categories",

                headers=self._headers()

            )

            if reponse.status_code == 200:
                return reponse.json()

            return []

        except:
            return []
    
    #creer_categorie
    def creer_categorie(self, nom_categorie):

        corps = {
            "nom_categorie": nom_categorie
        }

        try:
            reponse = requests.post(
                f"{API_BASE_URL}/categories",
                json=corps,
                headers=self._headers()
            )

            if reponse.status_code == 201:
                return reponse.json().get("id_categories")

            return None

        except:
            return None

    #utilisateur
    def obtenir_utilisateurs(self):

        try:

            reponse = requests.get(

                f"{API_BASE_URL}/utilisateurs",

                headers=self._headers()

            )

            if reponse.status_code == 200:
                return reponse.json()

            return []

        except:
            return []

    #historique
    def obtenir_historique(self):

        try:

            reponse = requests.get(

                f"{API_BASE_URL}/historique",

                headers=self._headers()

            )

            if reponse.status_code == 200:
                return reponse.json()

            return []

        except:
            return []

    #attribuer tacher
    def attribuer_tache(
            self,
            id_tache,
            utilisateur_id):

        corps = {

            "assigned_to": utilisateur_id

        }

        reponse = requests.put(

            f"{API_BASE_URL}/taches/{id_tache}",

            json=corps,

            headers=self._headers()

        )

        return reponse.status_code == 200