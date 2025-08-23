# agences.py

import random

AGENCES = [
    {"nom": "CIA", "pays": "USA", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["anglais"], "coop": False},
    {"nom": "NSA", "pays": "USA", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": False},
    {"nom": "MI6", "pays": "UK", "domaines": ["HUMINT", "SIGINT"], "langues": ["anglais"], "coop": True},
    {"nom": "FSB", "pays": "Russie", "domaines": ["SIGINT", "HUMINT", "TECH"], "langues": ["russe"], "coop": False},
    {"nom": "MSS", "pays": "Chine", "domaines": ["HUMINT", "CYBER"], "langues": ["chinois"], "coop": False},
    {"nom": "BND", "pays": "Allemagne", "domaines": ["HUMINT"], "langues": ["allemand"], "coop": True},
    {"nom": "Mossad", "pays": "Israël", "domaines": ["HUMINT", "SIGINT"], "langues": ["hébreu", "anglais"], "coop": False},
    {"nom": "RAW", "pays": "Inde", "domaines": ["HUMINT", "SIGINT"], "langues": ["hindi", "anglais"], "coop": False},
    {"nom": "ISI", "pays": "Pakistan", "domaines": ["HUMINT", "SIGINT"], "langues": ["ourdou", "anglais"], "coop": False},
    {"nom": "MIT", "pays": "Turquie", "domaines": ["HUMINT", "CYBER"], "langues": ["turc"], "coop": False},
    {"nom": "MOIS", "pays": "Iran", "domaines": ["HUMINT", "SIGINT"], "langues": ["persan"], "coop": False},
    {"nom": "PSIA", "pays": "Japon", "domaines": ["HUMINT", "CYBER"], "langues": ["japonais"], "coop": True},
    {"nom": "NIS", "pays": "Corée du Sud", "domaines": ["HUMINT", "CYBER"], "langues": ["coréen"], "coop": True},
    {"nom": "RGB", "pays": "Corée du Nord", "domaines": ["HUMINT", "SIGINT"], "langues": ["coréen"], "coop": False},
    {"nom": "ASIS", "pays": "Australie", "domaines": ["HUMINT"], "langues": ["anglais"], "coop": True},
    {"nom": "ASD", "pays": "Australie", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais"], "coop": True},
    {"nom": "CSIS", "pays": "Canada", "domaines": ["HUMINT"], "langues": ["anglais", "français"], "coop": True},
    {"nom": "CSE", "pays": "Canada", "domaines": ["SIGINT", "CYBER"], "langues": ["anglais", "français"], "coop": True},
    {"nom": "CNI", "pays": "Espagne", "domaines": ["HUMINT", "SIGINT"], "langues": ["espagnol"], "coop": True},
    {"nom": "AISE", "pays": "Italie", "domaines": ["HUMINT"], "langues": ["italien"], "coop": True},
    {"nom": "AIVD", "pays": "Pays-Bas", "domaines": ["HUMINT", "CYBER"], "langues": ["néerlandais"], "coop": True},
    {"nom": "SÄPO", "pays": "Suède", "domaines": ["HUMINT"], "langues": ["suédois"], "coop": True},
    {"nom": "ABW", "pays": "Pologne", "domaines": ["HUMINT"], "langues": ["polonais"], "coop": True},
    {"nom": "PST", "pays": "Norvège", "domaines": ["HUMINT"], "langues": ["norvégien"], "coop": True},
    {"nom": "PET", "pays": "Danemark", "domaines": ["HUMINT"], "langues": ["danois"], "coop": True},
    {"nom": "VSSE", "pays": "Belgique", "domaines": ["HUMINT"], "langues": ["français", "néerlandais"], "coop": True},
    {"nom": "NDB", "pays": "Suisse", "domaines": ["HUMINT", "SIGINT"], "langues": ["allemand", "français", "italien"], "coop": True},
    {"nom": "ABIN", "pays": "Brésil", "domaines": ["HUMINT", "SIGINT"], "langues": ["portugais"], "coop": False},
    {"nom": "GID", "pays": "Égypte", "domaines": ["HUMINT"], "langues": ["arabe"], "coop": False},
    {"nom": "SBU", "pays": "Ukraine", "domaines": ["HUMINT", "CYBER"], "langues": ["ukrainien"], "coop": True},
    # ... autres agences mondiales
]

def choisir_agence():
    return random.choice(AGENCES)

def lister_agences(pays=None):
    return [a for a in AGENCES if pays is None or a["pays"].lower() == pays.lower()]
