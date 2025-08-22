import random
from langues import LANGUES_PAR_PAYS

class Agent:
    def __init__(self, nom, prenom, pays, bureau, competences, langues, niveau=1, exp=0,
                 statut_legende=False, legende_nom=None, legende_temp=None, cout_base=10000, historique_legendes=None, nom_code=None):
        self.nom = nom
        self.prenom = prenom
        self.pays = pays
        self.bureau = bureau  # ex : "DO", "DR", "BDL", etc.
        self.competences = competences  # ["Infiltration", "Hacking", ...]
        self.langues = langues  # ["français", "anglais", ...]
        self.niveau = niveau
        self.exp = exp
        self.missions = []   # missions attribuées (id ou objet mission)
        self.history = []    # historique des déplacements ou affectations
        self.statut_legende = statut_legende
        self.legende_nom = legende_nom
        self.legende_temp = legende_temp
        self.cout_base = cout_base
        self.historique_legendes = historique_legendes if historique_legendes is not None else []
        self.nom_code = nom_code  # <= NOUVEAU

    def add_experience(self, points):
        self.exp += points
        if self.exp >= 100:
            self.niveau += 1
            self.exp -= 100

    def affecter_legende_temp(self, legende):
        if self.legende_temp is not None:
            self.archiver_legende(self.legende_temp)
        self.legende_temp = legende
        self.statut_legende = True
        self.legende_nom = legende.get("nom")

    def supprimer_legende_temp(self):
        if self.legende_temp is not None:
            self.archiver_legende(self.legende_temp)
        self.legende_temp = None
        self.statut_legende = False
        self.legende_nom = None

    def archiver_legende(self, legende_dict):
        self.historique_legendes.insert(0, legende_dict)
        self.historique_legendes = self.historique_legendes[:5]

    def reprendre_legende(self, idx):
        if 0 <= idx < len(self.historique_legendes):
            legende_dict = self.historique_legendes.pop(idx)
            if self.legende_temp is not None:
                self.archiver_legende(self.legende_temp)
            self.legende_temp = legende_dict
            self.statut_legende = True
            self.legende_nom = legende_dict.get("nom")

    def ajouter_mission(self, mission_id):
        self.missions.append(mission_id)

    def retirer_mission(self, mission_id):
        if mission_id in self.missions:
            self.missions.remove(mission_id)

    def ajouter_historique(self, lieu):
        self.history.append(lieu)

    def en_mission(self):
        return any(m for m in self.missions)

    def update_position(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.ajouter_historique((lat, lon))

    def __repr__(self):
        nc = f" (Code: {self.nom_code})" if self.nom_code else ""
        return f"<Agent {self.nom} {self.prenom}{nc} ({self.bureau}) | {'Légende' if self.statut_legende else 'Classique'}>"

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "pays": self.pays,
            "bureau": self.bureau,
            "competences": self.competences,
            "langues": self.langues,
            "niveau": self.niveau,
            "exp": self.exp,
            "missions": self.missions,
            "history": self.history,
            "statut_legende": self.statut_legende,
            "legende_nom": self.legende_nom,
            "legende_temp": self.legende_temp,
            "cout_base": self.cout_base,
            "lat": getattr(self, "lat", 48.85),
            "lon": getattr(self, "lon", 2.35),
            "historique_legendes": self.historique_legendes,
            "nom_code": self.nom_code
        }

    @staticmethod
    def from_dict(data):
        a = Agent(
            data["nom"],
            data["prenom"],
            data["pays"],
            data["bureau"],
            data["competences"],
            data["langues"],
            data.get("niveau", 1),
            data.get("exp", 0),
            data.get("statut_legende", False),
            data.get("legende_nom", None),
            data.get("legende_temp", None),
            data.get("cout_base", 10000),
            data.get("historique_legendes", []),
            data.get("nom_code", None)
        )
        a.missions = data.get("missions", [])
        a.history = data.get("history", [])
        a.lat = data.get("lat", 48.85)
        a.lon = data.get("lon", 2.35)
        return a

# ---------- Fonctions utiles agents -----------

def generer_langues(pays, n=2):
    langues_possibles = LANGUES_PAR_PAYS.get(pays, ["français"])
    langues = [langues_possibles[0]]
    autres = [l for l in langues_possibles[1:] if l not in langues]
    while len(langues) < n and autres:
        langues.append(random.choice(autres))
        autres = [l for l in autres if l not in langues]
    return langues

AGENTS = []

def ajouter_agent(agent):
    AGENTS.append(agent)

def supprimer_agent(idx):
    if 0 <= idx < len(AGENTS):
        AGENTS.pop(idx)

def modifier_agent(idx, **kwargs):
    if 0 <= idx < len(AGENTS):
        agent = AGENTS[idx]
        for k, v in kwargs.items():
            setattr(agent, k, v)

def lister_agents(bureau=None, legende=None):
    return [a for a in AGENTS
            if (bureau is None or a.bureau == bureau)
            and (legende is None or a.statut_legende == legende)]

def get_agent_by_nom(nom, prenom):
    for a in AGENTS:
        if a.nom == nom and a.prenom == prenom:
            return a
    return None

def est_disponible(agent):
    if getattr(agent, "statut", "").lower() in ["repos", "blessé", "mort"]:
        return False
    return True

def get_agents():
    return AGENTS

def refresh_agents(): pass
