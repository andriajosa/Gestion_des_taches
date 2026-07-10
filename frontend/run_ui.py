import sys
import os

# Ajouter la racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from UI.api_client import ApiClient
from UI.login_window import LoginWindow
from UI.registration_window import RegisterWindow
from UI.main_window import MainWindow


class Application:
    """
    Gère la navigation entre les différentes fenêtres
    de l'application.
    """

    def __init__(self):
        self.api_client = ApiClient()

    # ------------------------------
    # Fenêtre principale
    # ------------------------------
    def ouvrir_fenetre_principale(self):
        fenetre = MainWindow(
            api_client=self.api_client,
            retour_connexion=self.ouvrir_connexion
        )
        fenetre.mainloop()

    # ------------------------------
    # Fenêtre d'inscription
    # ------------------------------
    def ouvrir_inscription(self):
        fenetre = RegisterWindow(
            api_client=self.api_client,
            sur_enregistrement_reussi=self.ouvrir_connexion,
            aller_a_connexion=self.ouvrir_connexion
        )
        fenetre.mainloop()

    # ------------------------------
    # Fenêtre de connexion
    # ------------------------------
    def ouvrir_connexion(self):
        fenetre = LoginWindow(
            api_client=self.api_client,
            sur_connexion_reussie=self.ouvrir_fenetre_principale,
            aller_a_inscription=self.ouvrir_inscription
        )
        fenetre.mainloop()


if __name__ == "__main__":
    Application().ouvrir_connexion()