# agences.py

import random

AGENCES = [
    {"nom": "CIA", "pays": "USA", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["anglais"], "coop": False},
    {"nom": "NSA", "pays": "USA", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": False},
    {"nom": "MI6", "pays": "UK", "domaines": ["HUMINT", "SIGINT"], "langues": ["anglais"], "coop": True},
    {"nom": "FSB", "pays": "Russie", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["russe"], "coop": False},
    {"nom": "MSS", "pays": "Chine", "domaines": ["HUMINT", "CYBER"], "langues": ["chinois"], "coop": False},
    {"nom": "BND", "pays": "Allemagne", "domaines": ["HUMINT"], "langues": ["allemand"], "coop": True},
    # ... autres agences mondiales
]

def choisir_agence():
    return random.choice(AGENCES)

def lister_agences(pays=None):
    return [a for a in AGENCES if pays is None or a["pays"].lower() == pays.lower()]
