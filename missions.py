# missions.py — version complète et corrigée

import random
from datetime import datetime, timedelta
from geographie import VILLES_PAR_PAYS

MISSIONS = []

TYPES_MISSIONS = [
    "Opération d'infiltration", "Surveillance prolongée", "Protection rapprochée",
    "Exfiltration d'agent", "Neutralisation d'objectif", "Récupération d'informations",
    "Sabotage opérationnel", "Déstabilisation de réseaux", "Mise en place de planques",
    "Déploiement de moyens de surveillance", "Rencontre clandestine", "Test de sécurité d'un site",
    "Découverte de taupes", "Analyse de communications", "Cyber-intrusion",
    "Gestion de sources humaines", "Protection d'un transfuge", "Contre-espionnage",
    "Appui à une cellule locale", "Enrôlement de nouvel agent"
]

class Mission:
    def __init__(self, description, statut="En attente", bureau=None, lat=48.85, lon=2.35,
                 assigned_agent=None, rapport=None, progression=0, id=None, date_debut=None,
                 date_fin=None, type_mission="simple", embranchements=None):
        self.id = id or f"MISSION-{random.randint(100000, 999999)}"
        self.description = description
        self.statut = statut
        self.bureau = bureau
        self.lat = lat
        self.lon = lon
        self.assigned_agent = assigned_agent
        self.rapport = rapport or []
        self.progression = progression
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.type_mission = type_mission  # simple ou complexe
        self.embranchements = embranchements or []

    def demarrer(self, now, duree_minutes):
        self.date_debut = now
        self.date_fin = now + timedelta(minutes=duree_minutes)
        self.statut = "En cours"

    def maj_etat(self, now):
        if self.statut == "En cours" and self.date_fin and now >= self.date_fin:
            if self.type_mission == "complexe" and self.embranchements:
                self.embranchements.pop(0)
                if self.embranchements:
                    self.date_fin = now + timedelta(minutes=random.randint(300, 5760))
                    return
            self.statut = "Terminée"

    def attribuer_agent(self, agent):
        self.assigned_agent = agent
        if hasattr(agent, 'ajouter_mission'):
            agent.ajouter_mission(self.id)

    def ajouter_rapport(self, texte):
        self.rapport.append(texte)

    def avancer(self, points):
        self.progression = min(100, self.progression + points)
        if self.progression >= 100:
            self.statut = "Terminée"

    def echec(self):
        self.statut = "Echec"
        self.progression = 0

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Mission(
            d['description'], d.get('statut', 'En attente'), d.get('bureau'), d.get('lat', 48.85),
            d.get('lon', 2.35), d.get('assigned_agent'), d.get('rapport', []), d.get('progression', 0),
            d.get('id'), d.get('date_debut'), d.get('date_fin'), d.get('type_mission', 'simple'),
            d.get('embranchements', [])
        )

def ajouter_mission(mission):
    MISSIONS.append(mission)

def supprimer_mission(idx):
    if 0 <= idx < len(MISSIONS):
        MISSIONS.pop(idx)

def modifier_mission(idx, **kwargs):
    if 0 <= idx < len(MISSIONS):
        mission = MISSIONS[idx]
        for k, v in kwargs.items():
            setattr(mission, k, v)

def lister_missions(etat=None):
    return [m for m in MISSIONS if (etat is None or m.statut == etat)]

def get_missions():
    return MISSIONS

def generer_mission_automatique():
    pays = random.choice(list(VILLES_PAR_PAYS.keys()))
    ville = random.choice(VILLES_PAR_PAYS[pays])
    description = random.choice(TYPES_MISSIONS) + f" à {ville['ville']} ({pays.title()})"

    type_mission = "complexe" if random.random() < 0.1 else "simple"
    embranchements = []
    if type_mission == "complexe":
        embranchements = ["Succès" if random.random() < 0.7 else "Échec"
                          for _ in range(random.randint(2, 4))]

    duree_minutes = random.randint(600, 2880) if type_mission == "simple" else random.randint(300, 5760)

    m = Mission(
        description=description,
        statut="En attente",
        lat=ville['lat'],
        lon=ville['lon'],
        type_mission=type_mission,
        embranchements=embranchements
    )
    ajouter_mission(m)
    return m
