import tkinter as tk
from tkinter import ttk, messagebox

class TachesTable(ttk.Frame):
    # Ajout de la colonne "assigned_to" pour le mode collaboratif
    COLONNES = ("id_tache", "titre", "priority", "statut", "due_date", "assigned_to")

    def __init__(self, parent, api_client, est_admin=False, callback_action=None):
        """
        :param est_admin: True si l'utilisateur actuel est admin, ouvre les droits de suppression/réattribution
        :param callback_action: Fonction à appeler dans main_window pour rafraîchir l'affichage après une action
        """
        super().__init__(parent)
        self.api_client = api_client
        self.est_admin = est_admin
        self.callback_action = callback_action

        # --- CREATION DU TREEVIEW ---
        self.tree = ttk.Treeview(self, columns=self.COLONNES, show="headings", height=15)
        
        # Configuration des en-têtes et tailles
        titres = {
            "id_tache": "ID", "titre": "Titre de la tâche", 
            "priority": "Priorité", "statut": "Statut", 
            "due_date": "Échéance", "assigned_to": "Assigné à"
        }
        
        for colonne in self.COLONNES:
            self.tree.heading(colonne, text=titres[colonne])
            largeur = 60 if colonne == "id_tache" else 130
            self.tree.column(colonne, width=largeur, anchor="center" if colonne != "titre" else "w")

        # Configuration des couleurs pour les priorités (Tags)
        self.tree.tag_configure("Haute", background="#FFCDD2", foreground="#B71C1C")   # Rouge clair
        self.tree.tag_configure("Moyenne", background="#FFE0B2", foreground="#E65100") # Orange clair
        self.tree.tag_configure("Basse", background="#C8E6C9", foreground="#1B5E20")   # Vert clair

        # Barre de défilement (Scrollbar)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placement du tableau et de la scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- CREATION DU MENU CLIC DROIT (CONTEXTUEL) ---
        self.menu_contextuel = tk.Menu(self, tearoff=0)
        self.menu_contextuel.add_command(label="Changer le statut (Terminé/En cours)", command=self.basculer_statut)
        
        # Fonctionnalités restreintes aux administrateurs ou au mode collaboratif avancé
        if self.est_admin:
            self.menu_contextuel.add_separator()
            self.menu_contextuel.add_command(label="Supprimer la tâche ❌", command=self.supprimer_tache)
            self.menu_contextuel.add_command(label="Réassigner la tâche 👤", command=self.reassigner_tache)

        # Liaison du clic droit (Windows/Linux: <Button-3>, Mac: <Button-2>)
        self.tree.bind("<Button-3>", self.afficher_menu)

    def rafraichir(self, taches):
        """Remplit le tableau avec les données de l'API et applique les styles de priorité."""
        self.tree.delete(*self.tree.get_children())
        for tache in taches:
            priorite = tache.get("priority", "Basse")
            
            # Insertion avec le tag correspondant pour la couleur de ligne
            self.tree.insert("", tk.END, values=(
                tache.get("id_tache"), 
                tache.get("titre"), 
                priorite,
                tache.get("statut", "À faire"), 
                tache.get("due_date") or "Aucune", 
                tache.get("assigned_to") or "Non assigné"
            ), tags=(priorite,))

    def id_tache_selectionnee(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])["values"][0]

    def afficher_menu(self, event):
        """Affiche le menu clic droit là où se trouve la souris s'il y a une ligne sélectionnée."""
        item = self.tree.identify_row(event.y)
        if item:
            # Sélectionne automatiquement la ligne sous la souris
            self.tree.selection_set(item) 
            self.menu_contextuel.post(event.x_root, event.y_root)

    def basculer_statut(self):
        id_tache = self.id_tache_selectionnee()
        if not id_tache: return
        
        # Récupération de la ligne sélectionnée
        item = self.tree.item(self.tree.selection()[0])
        statut_actuel = item["values"][3]
        nouveau_statut = "Terminé" if statut_actuel != "Terminé" else "En cours"

        # Modification via l'API_Client
        succes = self.api_client.modifier_tache(id_tache, {"statut": nouveau_statut})
        if succes:
            if self.callback_action: self.callback_action()
        else:
            messagebox.showerror("Erreur", "Impossible de modifier le statut.")

    def supprimer_tache(self):
        if not self.est_admin:
            messagebox.showwarning("Droit insuffisant", "Seul un administrateur peut supprimer une tâche.")
            return

        id_tache = self.id_tache_selectionnee()
        if not id_tache: return

        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la tâche n°{id_tache} ?"):
            succes = self.api_client.supprimer_tache(id_tache)
            if succes:
                messagebox.showinfo("Succès", "Tâche supprimée avec succès.")
                if self.callback_action: self.callback_action()
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de la suppression.")

    def reassigner_tache(self):
        """Exemple d'ouverture vers une logique collaborative (Fenêtre popup de sélection de l'user)."""
        id_tache = self.id_tache_selectionnee()
        if not id_tache: return
        # Ici tu pourras coder une petite invite de saisie (SimpleDialog) 
        # pour taper le nom de l'utilisateur à qui attribuer le projet.
        pass