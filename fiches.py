# fiches.py

FICHES = {}

def creer_fiche(personne_id, type_pers, base_infos):
    FICHES[personne_id] = {
        "type": type_pers,  # "agent", "source", "suspect"
        "infos": base_infos,
        "historique": []
    }

def ajouter_info_fiche(personne_id, cle, valeur):
    if personne_id in FICHES:
        FICHES[personne_id]["infos"][cle] = valeur

def ajouter_historique_fiche(personne_id, evenement):
    if personne_id in FICHES:
        FICHES[personne_id]["historique"].append(evenement)

def get_fiche(personne_id):
    return FICHES.get(personne_id, None)

def lister_fiches(type_pers=None):
    return [
        (k, v) for k, v in FICHES.items()
        if (type_pers is None or v["type"] == type_pers)
    ]
