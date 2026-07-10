class Tache:
    def __init__(self, id_tache, titre, description, priority, statut,
                 due_date, categorie_id, created_by, assigned_to):
        self.id_tache = id_tache
        self.titre = titre
        self.description = description
        self.priority = priority
        self.statut = statut
        self.due_date = due_date
        self.categorie_id = categorie_id
        self.created_by = created_by
        self.assigned_to = assigned_to

    @staticmethod
    def depuis_ligne_sql(ligne):
        return Tache(
            id_tache=ligne["id_tache"],
            titre=ligne["titre"],
            description=ligne["description"],
            priority=ligne["priority"],
            statut=ligne["statut"],
            due_date=ligne["due_date"],
            categorie_id=ligne["categorie_id"],
            created_by=ligne["created_by"],
            assigned_to=ligne["assigned_to"]
        )