import tkinter as tk
from tkinter import ttk, messagebox

from backend.utils.validators import (
    email_valide,
    mot_de_passe_valide
)


class RegisterWindow(tk.Tk):

    def __init__(
            self,
            api_client,
            sur_enregistrement_reussi,
            aller_a_connexion=None):

        super().__init__()

        self.api_client = api_client
        self.sur_enregistrement_reussi = sur_enregistrement_reussi
        self.aller_a_connexion = aller_a_connexion

        self.title("Création d'un compte")
        self.geometry("550x680")
        self.resizable(False, False)

        self.configure(bg="#F4F6F8")

        self.role = tk.StringVar(value="utilisateur")

        self.creer_interface()

    def creer_interface(self):

        titre = tk.Label(
            self,
            text="Créer un compte",
            font=("Segoe UI", 22, "bold"),
            bg="#F4F6F8",
            fg="#1F4E79"
        )

        titre.pack(pady=20)

        cadre = ttk.LabelFrame(
            self,
            text="Informations"
        )

        cadre.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Nom d'utilisateur"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.champ_username = ttk.Entry(cadre)

        self.champ_username.pack(
            padx=15,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Adresse email"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.champ_email = ttk.Entry(cadre)

        self.champ_email.pack(
            padx=15,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Mot de passe (au moins 6 caractères)"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.champ_password = ttk.Entry(
            cadre,
            show="*"
        )

        self.champ_password.pack(
            padx=15,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Confirmer le mot de passe"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.confirmation = ttk.Entry(
            cadre,
            show="*"
        )

        self.confirmation.pack(
            padx=15,
            fill="x",
            pady=(0, 15)
        )

        cadre_role = ttk.LabelFrame(
            self,
            text="Type de compte"
        )

        cadre_role.pack(
            padx=30,
            pady=15,
            fill="x"
        )

        ttk.Radiobutton(
            cadre_role,
            text="Utilisateur",
            value="utilisateur",
            variable=self.role
        ).pack(anchor="w", padx=15, pady=5)

        ttk.Radiobutton(
            cadre_role,
            text="Administrateur",
            value="admin",
            variable=self.role
        ).pack(anchor="w", padx=15, pady=(0, 10))

        ttk.Button(
            self,
            text="Créer le compte",
            command=self.s_inscrire
        ).pack(
            fill="x",
            padx=40,
            pady=20
        )

        lien = tk.Label(
            self,
            text="Déjà inscrit ? Se connecter",
            fg="#0066CC",
            cursor="hand2",
            bg="#F4F6F8",
            font=("Segoe UI", 10, "underline")
        )

        lien.pack()

        lien.bind(
            "<Button-1>",
            lambda e: self.ouvrir_connexion()
        )

    # ----------------------------------------------------

    def s_inscrire(self):

        username = self.champ_username.get().strip()
        email = self.champ_email.get().strip()
        password = self.champ_password.get()
        confirmation = self.confirmation.get()

        if username == "":
            messagebox.showerror(
                "Erreur",
                "Nom d'utilisateur obligatoire."
            )
            return

        if not email_valide(email):
            messagebox.showerror(
                "Erreur",
                "Adresse email invalide."
            )
            return

        if not mot_de_passe_valide(password):
            messagebox.showerror(
                "Erreur",
                "Le mot de passe doit contenir au moins 6 caractères."
            )
            return

        if password != confirmation:
            messagebox.showerror(
                "Erreur",
                "Les deux mots de passe sont différents."
            )
            return

        succes, erreur = self.api_client.inscription(
            username,
            email,
            password,
            self.role.get()
        )

        if succes:

            messagebox.showinfo(
                "Succès",
                "Compte créé avec succès."
            )

            self.destroy()

            self.sur_enregistrement_reussi()

        else:

            messagebox.showerror(
                "Erreur",
                erreur
            )

    # ----------------------------------------------------

    def ouvrir_connexion(self):

        self.destroy()

        self.aller_a_connexion()