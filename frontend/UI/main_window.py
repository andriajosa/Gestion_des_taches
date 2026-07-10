# frontend/UI/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from UI.widgets.taches_table import TachesTable


class MainWindow(tk.Tk):
    STATUTS_AFFICHAGE = {"a_faire": "À faire", "en_cours": "En cours", "termine": "Terminé"}
    STATUTS_REVERSE = {v: k for k, v in STATUTS_AFFICHAGE.items()}

    def __init__(self, api_client, retour_connexion=None):
        super().__init__()
        self.api_client = api_client
        self.retour_connexion = retour_connexion
        self.title("Gestion des tâches")
        self.geometry("1200x700")
        self.taches_initiales = []
        
        infos_user = self.api_client.utilisateur_connecte() or {}
        self.nom_user = infos_user.get("nom_utilisateur", "Utilisateur")
        self.role_user = infos_user.get("role", "user")
        
        self.creer_interface()
        self.charger_taches()

    def creer_interface(self):
        self.barre_superieure = tk.Frame(self, bg="#2C3E50", height=50)
        self.barre_superieure.pack(fill=tk.X, side=tk.TOP)
        self.barre_superieure.pack_propagate(False)

        lbl_titre = tk.Label(self.barre_superieure, text="Gestion des tâches", fg="white", bg="#2C3E50", font=("Arial", 14, "bold"))
        lbl_titre.pack(side=tk.LEFT, padx=15)

        btn_deco = tk.Button(self.barre_superieure, text="Déconnexion", command=self.deconnexion, bg="#C0392B", fg="white", bd=0, padx=10, pady=5)
        btn_deco.pack(side=tk.RIGHT, padx=15, pady=10)

        lbl_info = tk.Label(self.barre_superieure, text=f"Session : {self.nom_user} ({self.role_user})", fg="white", bg="#2C3E50")
        lbl_info.pack(side=tk.RIGHT, padx=10)

        self.barre_recherche = tk.LabelFrame(self, text="Recherche et Filtres", padx=10, pady=10)
        self.barre_recherche.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(self.barre_recherche, text="Texte :").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.entree_recherche = tk.Entry(self.barre_recherche, width=25)
        self.entree_recherche.grid(row=0, column=1, padx=5)

        tk.Label(self.barre_recherche, text="Catégorie :").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.combo_cat = ttk.Combobox(self.barre_recherche, width=15, state="readonly")
        self.combo_cat.grid(row=0, column=3, padx=5)

        tk.Label(self.barre_recherche, text="Priorité :").grid(row=0, column=4, padx=5, sticky=tk.W)
        self.combo_prio = ttk.Combobox(self.barre_recherche, values=["Toutes", "Basse", "Moyenne", "Haute"], width=12, state="readonly")
        self.combo_prio.set("Toutes")
        self.combo_prio.grid(row=0, column=5, padx=5)

        tk.Label(self.barre_recherche, text="Statut :").grid(row=0, column=6, padx=5, sticky=tk.W)
        self.combo_statut = ttk.Combobox(self.barre_recherche, values=["Tous", "À faire", "En cours", "Terminé"], width=12, state="readonly")
        self.combo_statut.set("Tous")
        self.combo_statut.grid(row=0, column=7, padx=5)

        btn_chercher = tk.Button(self.barre_recherche, text="Rechercher", command=self.filtrer, bg="#34495E", fg="white")
        btn_chercher.grid(row=0, column=8, padx=5)

        btn_raz = tk.Button(self.barre_recherche, text="Réinitialiser", command=self.rafraichir, bg="#7F8C8D", fg="white")
        btn_raz.grid(row=0, column=9, padx=5)

        self.barre_actions = tk.Frame(self, padx=5, pady=5)
        self.barre_actions.pack(fill=tk.X, padx=15, pady=5)

        tk.Button(self.barre_actions, text="Ajouter", command=self.ajouter_tache, bg="#27AE60", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Modifier", command=self.modifier_tache, bg="#2980B9", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Supprimer", command=self.supprimer_tache, bg="#C0392B", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Attribuer", command=self.attribuer_tache, bg="#8E44AD", fg="white", width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Actualiser", command=self.charger_taches, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Historique", command=self.ouvrir_historique, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(self.barre_actions, text="Exporter CSV", command=self.exporter_csv, bg="#F39C12", fg="white", width=12).pack(side=tk.RIGHT, padx=2)

        self.cadre_tableau = tk.Frame(self)
        self.cadre_tableau.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.tableau = TachesTable(
            self.cadre_tableau,
            api_client=self.api_client,
            est_admin=(self.role_user == "admin"),
            callback_action=self.charger_taches
        )
        self.tableau.pack(fill=tk.BOTH, expand=True)

        self.barre_inferieure = tk.Frame(self, height=25, bg="#BDC3C7")
        self.barre_inferieure.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_total = tk.Label(self.barre_inferieure, text="Total: 0", bg="#BDC3C7")
        self.lbl_total.pack(side=tk.LEFT, padx=15)

        self.lbl_encours = tk.Label(self.barre_inferieure, text="En cours: 0", bg="#BDC3C7")
        self.lbl_encours.pack(side=tk.LEFT, padx=15)

        self.lbl_termines = tk.Label(self.barre_inferieure, text="Terminées: 0", bg="#BDC3C7")
        self.lbl_termines.pack(side=tk.LEFT, padx=15)

    def charger_taches(self):
        try:
            self.taches_initiales = self.api_client.obtenir_taches() or []

            # Résolution des ID "assigned_to" en noms d'utilisateur pour l'affichage
            utilisateurs = self.api_client.obtenir_utilisateurs() or []
            mappage_users = {u.get("id_utilisateur"): u.get("nom_utilisateur") for u in utilisateurs}

            categories = self.api_client.obtenir_categories() or []
            mappage_categories = {c.get("id_categories"): c.get("nom_categorie") for c in categories if c.get("id_categories")}

            for tache in self.taches_initiales:
                id_assigne = tache.get("assigned_to")
                tache["assigned_to"] = mappage_users.get(id_assigne, "Non assigné") if id_assigne else "Non assigné"
                tache["categorie"] = mappage_categories.get(tache.get("categorie_id"), "Aucune")
                tache["statut_affichage"] = self.STATUTS_AFFICHAGE.get(str(tache.get("statut", "")).lower(), tache.get("statut", ""))

            self.tableau.rafraichir(self.taches_initiales)
            self.mettre_a_jour_statistiques(self.taches_initiales)

            liste_cat = ["Toutes"] + [c.get("nom_categorie") for c in categories if c.get("nom_categorie")]
            self.combo_cat["values"] = list(set(liste_cat))
            self.combo_cat.set("Toutes")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {str(e)}")
    
    def rafraichir(self):
        self.entree_recherche.delete(0, tk.END)
        self.combo_cat.set("Toutes")
        self.combo_prio.set("Toutes")
        self.combo_statut.set("Tous")
        self.tableau.rafraichir(self.taches_initiales)
        self.mettre_a_jour_statistiques(self.taches_initiales)

    def filtrer(self):
        texte = self.entree_recherche.get().strip().lower()
        categorie = self.combo_cat.get()
        priorite = self.combo_prio.get()
        statut = self.combo_statut.get()

        resultats = []
        for t in self.taches_initiales:
            match_texte = (not texte or 
                           texte in str(t.get("titre", "")).lower() or 
                           texte in str(t.get("description", "")).lower() or 
                           texte in str(t.get("categorie", "")).lower())
            
            match_cat = (categorie == "Toutes" or str(t.get("categorie", "")) == categorie)
            match_prio = (priorite == "Toutes" or str(t.get("priority", "")).capitalize() == priorite.capitalize())
            statut_tache = self.STATUTS_AFFICHAGE.get(str(t.get("statut", "")).lower(), str(t.get("statut", "")))
            match_statut = (statut == "Tous" or statut_tache.lower() == statut.lower())

            if match_texte and match_cat and match_prio and match_statut:
                resultats.append(t)

        self.tableau.rafraichir(resultats)
        self.mettre_a_jour_statistiques(resultats)

    def ajouter_tache(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Nouvelle tâche")
        fenetre.geometry("350x450")
        fenetre.grab_set()

        tk.Label(fenetre, text="Titre *").pack(pady=(10,0))
        entree_titre = tk.Entry(fenetre, width=35)
        entree_titre.pack()

        tk.Label(fenetre, text="Description").pack(pady=(10,0))
        texte_desc = tk.Text(fenetre, width=35, height=4)
        texte_desc.pack()

        tk.Label(fenetre, text="Catégorie (laisser vide si aucune)").pack(pady=(10,0))
        entree_categorie = tk.Entry(fenetre, width=35)
        entree_categorie.pack()

        tk.Label(fenetre, text="Priorité").pack(pady=(10,0))
        combo_p = ttk.Combobox(fenetre, values=["Basse", "Moyenne", "Haute"], width=32, state="readonly")
        combo_p.set("Moyenne")
        combo_p.pack()

        tk.Label(fenetre, text="Échéance (AAAA-MM-JJ)").pack(pady=(10,0))
        entree_date = tk.Entry(fenetre, width=35)
        entree_date.pack()

        tk.Label(fenetre, text="Assigner à").pack(pady=(10,0))
        combo_u = ttk.Combobox(fenetre, width=32, state="readonly")
        users = self.api_client.obtenir_utilisateurs() or []
        mappage_users = {u.get("nom_utilisateur"): u.get("id_utilisateur") for u in users if u.get("nom_utilisateur")}
        combo_u["values"] = list(mappage_users.keys())
        combo_u.pack()

        def enregistrer():
            titre = entree_titre.get().strip()
            if not titre:
                messagebox.showwarning("Champs requis", "Le titre est obligatoire.")
                return

            nom_categorie_saisi = entree_categorie.get().strip()
            id_cat = None

            if nom_categorie_saisi:
                categories_actuelles = self.api_client.obtenir_categories() or []
                categorie_existante = next(
                    (c for c in categories_actuelles
                     if c.get("nom_categorie", "").lower() == nom_categorie_saisi.lower()),
                    None
                )

                if categorie_existante:
                    id_cat = categorie_existante.get("id_categories")
                else:
                    id_cat = self.api_client.creer_categorie(nom_categorie_saisi)
                    if id_cat is None:
                        messagebox.showerror("Erreur", "Impossible de créer la catégorie.")
                        return

            id_user_assigne = mappage_users.get(combo_u.get())

            succes = self.api_client.creer_tache(
                titre=titre,
                description=texte_desc.get("1.0", tk.END).strip(),
                priority=combo_p.get().lower(),
                due_date=entree_date.get().strip() or None,
                categorie_id=id_cat,
                assigned_to=id_user_assigne
            )

            if succes:
                messagebox.showinfo("Succès", "Tâche créée avec succès.")
                fenetre.destroy()
                self.charger_taches()
            else:
                messagebox.showerror("Erreur", "Impossible de créer la tâche.")

        tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="#27AE60", fg="white", width=15).pack(pady=20)

    def modifier_tache(self):
        id_sel = self.tableau.id_tache_selectionnee()
        if not id_sel:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une tâche à modifier.")
            return

        tache_actuelle = next((t for t in self.taches_initiales if t.get("id_tache") == id_sel), None)
        if not tache_actuelle:
            return

        fenetre = tk.Toplevel(self)
        fenetre.title("Modifier la tâche")
        fenetre.geometry("350x480")
        fenetre.grab_set()

        tk.Label(fenetre, text="Titre *").pack(pady=(10,0))
        entree_titre = tk.Entry(fenetre, width=35)
        entree_titre.insert(0, tache_actuelle.get("titre", ""))
        entree_titre.pack()

        tk.Label(fenetre, text="Description").pack(pady=(10,0))
        texte_desc = tk.Text(fenetre, width=35, height=4)
        texte_desc.insert("1.0", tache_actuelle.get("description", ""))
        texte_desc.pack()

        tk.Label(fenetre, text="Statut").pack(pady=(10,0))
        combo_s = ttk.Combobox(fenetre, values=["À faire", "En cours", "Terminé"], width=32, state="readonly")
        combo_s.set(self.STATUTS_AFFICHAGE.get(str(tache_actuelle.get("statut", "")).lower(), "À faire"))
        combo_s.pack()

        tk.Label(fenetre, text="Priorité").pack(pady=(10,0))
        combo_p = ttk.Combobox(fenetre, values=["Basse", "Moyenne", "Haute"], width=32, state="readonly")
        combo_p.set(str(tache_actuelle.get("priority", "Moyenne")).capitalize())
        combo_p.pack()

        tk.Label(fenetre, text="Échéance (AAAA-MM-JJ)").pack(pady=(10,0))
        entree_date = tk.Entry(fenetre, width=35)
        entree_date.insert(0, tache_actuelle.get("due_date", "") or "")
        entree_date.pack()

        def sauvegarder():
            titre = entree_titre.get().strip()
            if not titre:
                messagebox.showwarning("Champs requis", "Le titre ne peut pas être vide.")
                return

            champs = {
                "titre": titre,
                "description": texte_desc.get("1.0", tk.END).strip(),
                "statut": self.STATUTS_REVERSE.get(combo_s.get(), combo_s.get()),
                "priority": combo_p.get().lower(),
                "due_date": entree_date.get().strip() or None
            }

            if self.api_client.modifier_tache(id_sel, champs):
                messagebox.showinfo("Succès", "Tâche mise à jour.")
                fenetre.destroy()
                self.charger_taches()
            else:
                messagebox.showerror("Erreur", "Échec de la modification.")

        tk.Button(fenetre, text="Sauvegarder", command=sauvegarder, bg="#2980B9", fg="white", width=15).pack(pady=20)

    def supprimer_tache(self):
        id_sel = self.tableau.id_tache_selectionnee()
        if not id_sel:
            messagebox.showwarning("Sélection requise", "Sélectionnez la tâche à supprimer.")
            return

        if messagebox.askyesno("Confirmation", f"Voulez-vous supprimer la tâche ID {id_sel} ?"):
            if self.api_client.supprimer_tache(id_sel):
                messagebox.showinfo("Succès", "Tâche supprimée.")
                self.charger_taches()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer cette tâche.")

    def attrs_attribuer_tache(self, id_tache, id_user):
        if hasattr(self.api_client, 'attribuer_tache'):
            return self.api_client.attribuer_tache(id_tache, id_user)
        return self.api_client.modifier_tache(id_tache, {"assigned_to": id_user})

    def attribuer_tache(self):
        id_sel = self.tableau.id_tache_selectionnee()
        if not id_sel:
            messagebox.showwarning("Sélection requise", "Sélectionnez une tâche à attribuer.")
            return

        fenetre = tk.Toplevel(self)
        fenetre.title("Attribuer la tâche")
        fenetre.geometry("300x150")
        fenetre.grab_set()

        tk.Label(fenetre, text="Sélectionner l'utilisateur :").pack(pady=15)
        combo_u = ttk.Combobox(fenetre, width=30, state="readonly")
        users = self.api_client.obtenir_utilisateurs() or []
        mappage_users = {u.get("nom_utilisateur"): u.get("id_utilisateur") for u in users if u.get("nom_utilisateur")}
        combo_u["values"] = list(mappage_users.keys())
        combo_u.pack()

        def valider():
            nom_sel = combo_u.get()
            if not nom_sel:
                messagebox.showwarning("Champs requis", "Sélectionnez un utilisateur.")
                return
            
            id_user = mappage_users.get(nom_sel)
            
            if self.attrs_attribuer_tache(id_sel, id_user):
                messagebox.showinfo("Succès", f"Tâche attribuée à {nom_sel}.")
                fenetre.destroy()
                self.charger_taches()
            else:
                messagebox.showerror("Erreur", "Impossible d'attribuer la tâche.")

        tk.Button(fenetre, text="Valider", command=valider, bg="#8E44AD", fg="white", width=12).pack(pady=15)

    def ouvrir_historique(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Historique des activités")
        fenetre.geometry("700x400")
        fenetre.grab_set()

        colonnes = ("id", "user", "action", "date")
        table_hist = ttk.Treeview(fenetre, columns=colonnes, show="headings")
        table_hist.heading("id", text="ID")
        table_hist.heading("user", text="Utilisateur")
        table_hist.heading("action", text="Action")
        table_hist.heading("date", text="Date")

        table_hist.column("id", width=50, anchor="center")
        table_hist.column("user", width=120)
        table_hist.column("action", width=350)
        table_hist.column("date", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=table_hist.yview)
        table_hist.configure(yscrollcommand=scrollbar.set)
        
        table_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        try:
            logs = self.api_client.obtenir_historique() or []
            for item in logs:
                table_hist.insert("", tk.END, values=(
                    item.get("id_historique") or item.get("id"),
                    item.get("nom_utilisateur") or item.get("utilisateur"),
                    item.get("action"),
                    item.get("date_action") or item.get("date")
                ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'historique : {str(e)}")

    def exporter_csv(self):
        if not self.taches_initiales:
            messagebox.showwarning("Export impossible", "Aucune donnée à exporter.")
            return

        fichier = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")],
            title="Exporter les tâches"
        )
        if not fichier:
            return

        try:
            df = pd.DataFrame(self.taches_initiales)
            
            mappage_colonnes = {
                "id_tache": "ID",
                "titre": "Titre",
                "description": "Description",
                "categorie": "Catégorie",
                "priority": "Priorité",
                "statut": "Statut",
                "due_date": "Échéance",
                "cree_par": "Créée par",
                "assigned_to": "Assignée à",
                "date_creation": "Date création"
            }
            
            df = df.rename(columns=mappage_colonnes)
            colonnes_finales = [c for c in mappage_colonnes.values() if c in df.columns]
            df = df[colonnes_finales]
            
            df.to_csv(fichier, index=False, encoding="utf-8-sig")
            messagebox.showinfo("Export réussi", "Les données ont été exportées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Une erreur est survenue lors de l'exportation : {str(e)}")

    def deconnexion(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vous déconnecter ?"):
            try:
                self.api_client.deconnexion()
            except:
                pass
            self.destroy()
            if self.retour_connexion:
                self.retour_connexion()

    def mettre_a_jour_statistiques(self, liste_taches):
        total = len(liste_taches)
        en_cours = sum(1 for t in liste_taches if str(t.get("statut", "")).lower() in ["en cours", "en_cours"])
        termines = sum(1 for t in liste_taches if str(t.get("statut", "")).lower() in ["terminé", "termine"])

        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_encours.config(text=f"En cours: {en_cours}")
        self.lbl_termines.config(text=f"Terminées: {termines}")