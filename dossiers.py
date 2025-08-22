# dossiers.py

class DossierSource:
    def __init__(self, nom, pays, ville, infos, agent_recruteur, rattachement=None):
        self.nom = nom
        self.pays = pays
        self.ville = ville
        self.infos = infos
        self.agent_recruteur = agent_recruteur
        self.rattachement = rattachement  # nom du réseau

    def to_dict(self):
        return {
            "nom": self.nom,
            "pays": self.pays,
            "ville": self.ville,
            "infos": self.infos,
            "agent_recruteur": self.agent_recruteur,
            "rattachement": self.rattachement
        }
    @staticmethod
    def from_dict(data):
        return DossierSource(
            data["nom"], data["pays"], data["ville"], data["infos"],
            data["agent_recruteur"], data.get("rattachement")
        )
