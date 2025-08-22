# metiers.py

import random

METIERS = {
    "technicien radioprotection": {
    "secteur": "Nucléaire",
    "entreprises": ["EDF", "Orano", "CEA", "Framatome"],
    "competences": ["sécurité", "nucléaire", "radioprotection"]
},
"inspecteur ASN": {
    "secteur": "Nucléaire",
    "entreprises": ["ASN", "IRSN"],
    "competences": ["réglementation", "nucléaire", "contrôle"]
},
"ingénieur sûreté nucléaire": {
    "secteur": "Nucléaire",
    "entreprises": ["EDF", "CEA", "Framatome", "Rosatom"],
    "competences": ["nucléaire", "sûreté", "ingénierie"]
},
"agent de maintenance nucléaire": {
    "secteur": "Nucléaire",
    "entreprises": ["EDF", "Orano", "Westinghouse"],
    "competences": ["technique", "nucléaire", "maintenance"]
},
"physicien nucléaire": {
    "secteur": "Recherche nucléaire",
    "entreprises": ["CEA", "CNRS", "IN2P3", "ITER"],
    "competences": ["physique", "recherche", "nucléaire"]
},
"consultant déconstruction nucléaire": {
    "secteur": "Nucléaire",
    "entreprises": ["Orano", "EDF", "Veolia"],
    "competences": ["projet", "nucléaire", "environnement"]
},
"spécialiste transport matières radioactives": {
    "secteur": "Nucléaire / Transport",
    "entreprises": ["Orano", "Transnucleaire", "SNCF"],
    "competences": ["logistique", "sécurité", "nucléaire"]
},
    "ingénieur balistique": {
    "secteur": "Armement",
    "entreprises": ["MBDA", "Nexter", "Safran", "Thales"],
    "competences": ["balistique", "recherche", "défense"]
},
"chef de projet armement": {
    "secteur": "Armement",
    "entreprises": ["MBDA", "Safran", "Airbus Defence", "Thales"],
    "competences": ["gestion", "défense", "ingénierie"]
},
"testeur d’armes": {
    "secteur": "Armement",
    "entreprises": ["DGA", "Nexter", "Thales"],
    "competences": ["tests", "sécurité", "technique"]
},
"responsable export d’armement": {
    "secteur": "Commerce/Armement",
    "entreprises": ["MBDA", "Safran", "Dassault"],
    "competences": ["export", "réglementation", "défense"]
},
"expert réglementation ITAR": {
    "secteur": "Armement / Légal",
    "entreprises": ["MBDA", "Ministère des Armées", "Thales"],
    "competences": ["réglementation", "défense", "international"]
},
"analyste intelligence économique défense": {
    "secteur": "Armement / Veille",
    "entreprises": ["Safran", "Dassault", "Ministère des Armées"],
    "competences": ["veille", "défense", "analyse"]
},
"opérateur de fabrication de munitions": {
    "secteur": "Armement",
    "entreprises": ["Nexter", "Eurenco", "MBDA"],
    "competences": ["fabrication", "sécurité", "technique"]
},
"expert déminage": {
    "secteur": "Défense / Sécurité",
    "entreprises": ["Armée de Terre", "Sécurité Civile", "ONU"],
    "competences": ["explosifs", "sécurité", "terrain"]
},

    "chimiste": {
        "secteur": "Pétrolier",
        "entreprises": ["Total", "Petronas", "NIOC", "BP"],
        "competences": ["sciences", "analyse", "sécurité"]
    },
    "commercial": {
        "secteur": "Pétrolier",
        "entreprises": ["Total", "Shell", "Exxon"],
        "competences": ["commerce", "langues", "réseautage"]
    },
    "analyste cyber": {
        "secteur": "Cybersécurité",
        "entreprises": ["Orange Cyberdefense", "Kaspersky", "FireEye", "ANSSI", "Thales"],
        "competences": ["cyber", "analyse", "sécurité"]
    },
    "soudeur nucléaire": {
        "secteur": "Nucléaire",
        "entreprises": ["EDF", "Framatome", "Rosatom"],
        "competences": ["nucléaire", "technique"]
    },
    "opérateur SIGINT": {
        "secteur": "Renseignement",
        "entreprises": ["DGSE", "NSA", "GCHQ"],
        "competences": ["écoute", "analyse", "langues"]
    },
    "analyste OSINT": {
        "secteur": "Renseignement",
        "entreprises": ["DGSE", "BND", "CIA", "MI6"],
        "competences": ["veille", "recherche", "synthèse"]
    },
    "diplomate": {
        "secteur": "Affaires étrangères",
        "entreprises": ["Ministère des Affaires étrangères", "ONU", "Ambassade"],
        "competences": ["langues", "diplomatie", "analyse"]
    },
    "journaliste": {
        "secteur": "Médias",
        "entreprises": ["AFP", "Reuters", "Le Monde", "BBC"],
        "competences": ["rédaction", "recherche", "langues"]
    },
    "informaticien": {
        "secteur": "Technologies",
        "entreprises": ["Microsoft", "Apple", "Google", "Thales", "Palantir"],
        "competences": ["programmation", "cyber", "réseau"]
    },
    "chef de projet IT": {
        "secteur": "Technologies",
        "entreprises": ["Capgemini", "Accenture", "Atos"],
        "competences": ["gestion", "organisation", "cyber"]
    },
    "agent de sécurité": {
        "secteur": "Sécurité privée",
        "entreprises": ["Securitas", "Prosegur", "G4S"],
        "competences": ["surveillance", "sécurité"]
    },
    "traducteur": {
        "secteur": "Langues & Interprétariat",
        "entreprises": ["ONU", "Union Européenne", "Cabinets de traduction"],
        "competences": ["langues", "analyse", "discrétion"]
    },
    "ingénieur télécom": {
        "secteur": "Télécommunications",
        "entreprises": ["Orange", "Huawei", "Ericsson", "Nokia"],
        "competences": ["réseau", "technique", "sécurité"]
    },
    "expert blockchain": {
        "secteur": "Finance / Technologie",
        "entreprises": ["Binance", "Ledger", "Chainalysis"],
        "competences": ["cryptographie", "finance", "analyse"]
    },
    "pilote de drone": {
        "secteur": "Aéronautique",
        "entreprises": ["Armée de l'air", "Parrot", "DJI"],
        "competences": ["pilotage", "technique", "vidéo"]
    },
    "biologiste": {
        "secteur": "Recherche / Santé",
        "entreprises": ["Institut Pasteur", "INSERM", "Pfizer"],
        "competences": ["analyse", "sciences", "biologie"]
    },
    "agent de liaison": {
        "secteur": "Diplomatie",
        "entreprises": ["Ambassade", "Services de renseignement"],
        "competences": ["relationnel", "discrétion", "langues"]
    },
    "banquier": {
        "secteur": "Finance",
        "entreprises": ["BNP Paribas", "HSBC", "Deutsche Bank"],
        "competences": ["finance", "analyse", "réseau"]
    },
    "chauffeur poids-lourd": {
        "secteur": "Logistique",
        "entreprises": ["DHL", "Schenker", "Transdev"],
        "competences": ["transport", "itinéraire", "logistique"]
    },
    "ingénieur en armement": {
        "secteur": "Défense",
        "entreprises": ["MBDA", "Thales", "Dassault", "Safran"],
        "competences": ["défense", "ingénierie", "sécurité"]
    },
    "spécialiste cryptographie": {
        "secteur": "Cybersécurité",
        "entreprises": ["ANSSI", "DGSE", "GCHQ"],
        "competences": ["cryptographie", "analyse", "mathématiques"]
    },
    "douanier": {
        "secteur": "Contrôle / Douanes",
        "entreprises": ["Douanes françaises", "US Customs"],
        "competences": ["contrôle", "lois", "analyse"]
    },
    "expert OSINT": {
        "secteur": "Veille stratégique",
        "entreprises": ["Sekoia", "Risk&Co", "DGSE"],
        "competences": ["veille", "internet", "analyse"]
    },
    "officier de marine": {
        "secteur": "Défense",
        "entreprises": ["Marine nationale", "US Navy"],
        "competences": ["commandement", "navigation", "stratégie"]
    },
    "consultant export": {
        "secteur": "Commerce international",
        "entreprises": ["Business France", "CCI", "Cabinets privés"],
        "competences": ["export", "réglementation", "langues"]
    },
    "médecin urgentiste": {
        "secteur": "Santé",
        "entreprises": ["SAMU", "Hôpitaux", "ONG"],
        "competences": ["médecine", "urgence", "réactivité"]
    },
    "urbaniste": {
        "secteur": "Géopolitique/Aménagement",
        "entreprises": ["Mairies", "Cabinets d'études"],
        "competences": ["analyse", "cartographie", "projet"]
    },
    "géologue": {
        "secteur": "Énergie",
        "entreprises": ["Total", "Exxon", "Chevron"],
        "competences": ["analyse", "terrain", "cartographie"]
    },
    "analyste financier": {
        "secteur": "Finance",
        "entreprises": ["Goldman Sachs", "Banque de France", "Crédit Suisse"],
        "competences": ["finance", "analyse", "économie"]
    },
    "spécialiste logistique": {
        "secteur": "Transport & Logistique",
        "entreprises": ["DHL", "Amazon", "FedEx"],
        "competences": ["logistique", "gestion", "organisation"]
    },
    "analyste de risques": {
        "secteur": "Sécurité",
        "entreprises": ["Allianz", "Axa", "Risk&Co"],
        "competences": ["sécurité", "évaluation", "analyse"]
    },
    "avocat international": {
        "secteur": "Juridique",
        "entreprises": ["Cabinets d'avocats", "Cour pénale internationale"],
        "competences": ["droit", "international", "analyse"]
    },
    "gestionnaire de crise": {
        "secteur": "Sécurité civile",
        "entreprises": ["Protection civile", "Préfecture", "Armée"],
        "competences": ["gestion", "décision", "communication"]
    },
    "cartographe SIG": {
        "secteur": "Géomatique",
        "entreprises": ["ESRI", "IGN", "Armée"],
        "competences": ["cartographie", "SIG", "analyse"]
    },
    # Ajoute d'autres métiers si tu veux encore plus de diversité !
}

def get_metier_infos(metier):
    return METIERS.get(metier, {})

def choisir_metier_competence(competences_agent):
    """
    Retourne un métier et une entreprise selon les compétences de l'agent uniquement (pas le pays).
    """
    pool = [k for k, v in METIERS.items() if any(c in v["competences"] for c in competences_agent)]
    if not pool:
        return {}
    metier = random.choice(pool)
    infos = METIERS[metier]
    entreprise = random.choice(infos["entreprises"])
    return {"metier": metier, "entreprise": entreprise}
    
def generer_metier_aleatoire():
    nom_metier = random.choice(list(METIERS.keys()))
    infos = METIERS[nom_metier]
    entreprise = random.choice(infos["entreprises"])
    return {
        "metier": nom_metier,
        "entreprise": entreprise,
        "competences": infos["competences"]
    }
    
def choisir_metier_secteur(secteur):
    candidats = [k for k, v in METIERS.items() if v["secteur"].lower() == secteur.lower()]
    if not candidats:
        return {"metier": "Inconnu", "competences": [], "entreprises": ["N/A"]}
    metier = random.choice(candidats)
    infos = METIERS[metier]
    return {
        "metier": metier,
        "competences": infos["competences"],
        "entreprise": random.choice(infos["entreprises"])
    }

