import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow(tk.Tk):

    def __init__(self, api_client, sur_connexion_reussie, aller_a_inscription=None):

        super().__init__()

        self.api_client = api_client
        self.sur_connexion_reussie = sur_connexion_reussie
        self.aller_a_inscription = aller_a_inscription

        self.title("Gestion des Tâches - Connexion")
        self.geometry("520x430")
        self.resizable(False, False)

        self.configure(bg="#F4F6F8")

        self.creer_interface()


    def creer_interface(self):

        titre = tk.Label(
            self,
            text="Gestion des Tâches",
            font=("Segoe UI", 22, "bold"),
            bg="#F4F6F8",
            fg="#1F4E79"
        )

        titre.pack(pady=(25, 5))

        cadre = ttk.LabelFrame(
            self,
            text="Connexion"
        )

        cadre.pack(
            padx=35,
            pady=30,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Adresse email"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.champ_email = ttk.Entry(
            cadre,
            width=45
        )

        self.champ_email.pack(
            padx=15,
            fill="x"
        )

        ttk.Label(
            cadre,
            text="Mot de passe"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.champ_mot_de_passe = ttk.Entry(
            cadre,
            show="*",
            width=45
        )

        self.champ_mot_de_passe.pack(
            padx=15,
            fill="x"
        )

        ttk.Button(
            cadre,
            text="Se connecter",
            command=self.se_connecter
        ).pack(
            pady=20,
            padx=15,
            fill="x"
        )

        if self.aller_a_inscription:

            ttk.Separator(self).pack(
                fill="x",
                padx=25,
                pady=10
            )

            lien = tk.Label(
                self,
                text="Créer un nouveau compte",
                fg="#0066CC",
                cursor="hand2",
                bg="#F4F6F8",
                font=("Segoe UI", 10, "underline")
            )

            lien.pack()

            lien.bind(
                "<Button-1>",
                lambda e: self.ouvrir_inscription()
            )

    def se_connecter(self):

        email = self.champ_email.get().strip()

        mot_de_passe = self.champ_mot_de_passe.get()

        if email == "":
            messagebox.showwarning(
                "Information",
                "Veuillez saisir votre adresse email."
            )
            return

        if mot_de_passe == "":
            messagebox.showwarning(
                "Information",
                "Veuillez saisir votre mot de passe."
            )
            return

        succes, erreur = self.api_client.connexion(
            email,
            mot_de_passe
        )

        if succes:

            self.destroy()

            self.sur_connexion_reussie()

        else:

            messagebox.showerror(
                "Connexion",
                erreur
            )


    def ouvrir_inscription(self):

        self.destroy()

        self.aller_a_inscription()