# bureaux.py

BUREAUX = [
    {
        "code": "DR",
        "nom": "Direction du Renseignement",
        "type": "Direction",
        "description": "Collecte, analyse et synthèse du renseignement extérieur.",
        "bureaux_fils": [
            {"code": "AFRIQUE", "nom": "Bureau Afrique", "type": "Bureau géographique"},
            {"code": "MO", "nom": "Bureau Moyen-Orient", "type": "Bureau géographique"},
            {"code": "RUSSIE", "nom": "Bureau Russie & CEI", "type": "Bureau géographique"},
        ],
        "bureaux_thematiques": [
            {"code": "TERRORISME", "nom": "Cellule Terrorisme", "type": "Thématique"},
            {"code": "CYBER", "nom": "Cellule Cyber", "type": "Thématique"},
        ]
    },
    {
        "code": "DO",
        "nom": "Direction des Opérations",
        "type": "Direction",
        "description": "Planification/exécution d'opérations clandestines et action.",
    },
    {
        "code": "DT",
        "nom": "Direction Technique",
        "type": "Direction",
        "description": "SIGINT, hacking, innovation, appui technique.",
    },
    {
        "code": "DS",
        "nom": "Direction de la Stratégie",
        "type": "Direction",
        "description": "Analyse stratégique, veille multi-domaines.",
    },
    {
        "code": "DA",
        "nom": "Direction de l’Administration",
        "type": "Direction",
        "description": "Gestion RH, finances, sécurité interne.",
    },
    {
        "code": "BDL",
        "nom": "Bureau des Légendes",
        "type": "Cellule spéciale",
        "description": "Gestion agents sous légende, opérations clandestines longue durée.",
    }
]

def lister_bureaux():
    return [b["code"] for b in BUREAUX]

def get_bureau(code):
    for b in BUREAUX:
        if b["code"] == code:
            return b
    return None
