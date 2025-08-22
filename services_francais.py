# services_francais.py

import random

ALERTES = [
    {
        "emetteur": "DGSI",
        "logo": "assets/logos/dgsi.png",  # Peut être une URL ou un chemin
        "message": "Alerte sur la présence d'un individu surveillé à Lyon."
    },
    {
        "emetteur": "Police",
        "logo": "assets/logos/police.png",
        "message": "Signalement de mouvements suspects à proximité d'une ambassade étrangère à Paris."
    },
    {
        "emetteur": "Gendarmerie",
        "logo": "assets/logos/gendarmerie.png",
        "message": "Découverte d'une cache d'armes dans le sud-ouest."
    },
    # ... autres modèles d'alertes
]

def generer_alerte():
    return random.choice(ALERTES)

def prochain_delai_alerte():
    # Entre 5 et 10 minutes
    return random.randint(300, 600)
