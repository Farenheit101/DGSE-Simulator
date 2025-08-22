# sources.py

import random

SOURCES = []

class Source:
    def __init__(self, nom, prenom, metier, lat=48.85, lon=2.35, rattachement=None, dossier=None):
        self.nom = nom
        self.prenom = prenom
        self.metier = metier
        self.lat = lat
        self.lon = lon
        self.rattachement = rattachement  # nom du réseau/cellule
        self.dossier = dossier or {}      # historique infos recueillies

    def ajouter_info(self, cle, valeur):
        self.dossier[cle] = valeur

    def rattacher_cellule(self, cellule):
        self.rattachement = cellule

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        s = Source(
            d['nom'], d['prenom'], d['metier'], d.get('lat', 48.85), d.get('lon', 2.35), d.get('rattachement'), d.get('dossier', {})
        )
        return s

def ajouter_source(source):
    SOURCES.append(source)

def supprimer_source(idx):
    if 0 <= idx < len(SOURCES):
        SOURCES.pop(idx)

def modifier_source(idx, **kwargs):
    if 0 <= idx < len(SOURCES):
        source = SOURCES[idx]
        for k, v in kwargs.items():
            setattr(source, k, v)

def lister_sources(cellule=None, secteur=None):
    return [
        s for s in SOURCES
        if (cellule is None or s.rattachement == cellule)
        and (secteur is None or getattr(s, "secteur", None) == secteur)
    ]

def get_sources():
    return SOURCES
