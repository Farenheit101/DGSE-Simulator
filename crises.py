import random
from datetime import datetime, timedelta

NOMS_OPERATION = [
    "Aigle Noir", "Tempête Blanche", "Lynx Gris", "Phénix Rouge",
    "Opale", "Quasar", "Icebreaker", "Spectre", "Jade", "Mamba", "Sahara", "Bison", "Saturne"
]

def generer_nom_operation():
    return random.choice(NOMS_OPERATION) + "-" + str(random.randint(10, 99))

CRISES = []

class Crise:
    def __init__(self, nom=None, statut="En cours", origine=None, gravite=None, etapes=None, suspects=None, dossier=None, lat=48.85, lon=2.35, date_debut=None, date_fin=None):
        self.nom = nom if nom else generer_nom_operation()
        self.statut = statut
        self.origine = origine
        self.gravite = gravite
        self.etapes = etapes or []
        self.suspects = suspects or []
        self.dossier = dossier or {}
        self.lat = lat
        self.lon = lon
        self.date_debut = date_debut
        self.date_fin = date_fin

    def ajouter_etape(self, texte):
        self.etapes.append(texte)

    def ajouter_suspect(self, personne):
        self.suspects.append(personne)

    def clore(self, resultat):
        self.statut = "Clôturée"
        self.dossier["resultat"] = resultat

    def demarrer(self, now, duree_minutes):
        self.date_debut = now
        self.date_fin = now + timedelta(minutes=duree_minutes)
        self.statut = "En cours"

    def maj_etat(self, now):
        if self.statut == "En cours" and self.date_fin and now >= self.date_fin:
            self.statut = "Clôturée"
            self.dossier["resultat"] = "Clôturée automatiquement par le temps"

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        c = Crise(
            d.get('nom'), d.get('statut', 'En cours'), d.get('origine'), d.get('gravite'),
            d.get('etapes', []), d.get('suspects', []), d.get('dossier', {}), d.get('lat', 48.85), d.get('lon', 2.35),
            d.get('date_debut', None), d.get('date_fin', None)
        )
        return c

def ajouter_crise(crise):
    CRISES.append(crise)

def supprimer_crise(idx):
    if 0 <= idx < len(CRISES):
        CRISES.pop(idx)

def modifier_crise(idx, **kwargs):
    if 0 <= idx < len(CRISES):
        crise = CRISES[idx]
        for k, v in kwargs.items():
            setattr(crise, k, v)

def lister_crises(etat=None):
    return [c for c in CRISES if (etat is None or c.statut == etat)]

def get_crises():
    return CRISES
