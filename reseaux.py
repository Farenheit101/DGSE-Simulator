# reseaux.py

RESEAUX = {}
from datetime import datetime

def ajouter_reseau(nom, pays, ville, lat=48.85, lon=2.35):
    if nom not in RESEAUX:
        RESEAUX[nom] = {
            "pays": pays,
            "ville": ville,
            "lat": lat,
            "lon": lon,
            "agents": [],
            "sources": [],
            "missions": [],
            "responsable": None,
            "evenements": [],  # 🆕 historique interne du réseau
            "date_creation": datetime.now().strftime("%d/%m/%Y")
        }

def supprimer_reseau(nom):
    if nom in RESEAUX:
        del RESEAUX[nom]

def modifier_reseau(nom, **kwargs):
    if nom in RESEAUX:
        for k, v in kwargs.items():
            RESEAUX[nom][k] = v

def rattacher_agent_reseau(reseau, agent):
    if reseau in RESEAUX and agent not in RESEAUX[reseau]["agents"]:
        RESEAUX[reseau]["agents"].append(agent)

def rattacher_source_reseau(reseau, source):
    if reseau in RESEAUX and source not in RESEAUX[reseau]["sources"]:
        RESEAUX[reseau]["sources"].append(source)

def lister_reseaux(pays=None):
    return [
        (k, v) for k, v in RESEAUX.items()
        if (pays is None or v["pays"] == pays)
    ]

def get_reseaux():
    return RESEAUX
    
def definir_responsable(reseau, agent):
    if reseau in RESEAUX:
        RESEAUX[reseau]["responsable"] = agent

def supprimer_responsable(reseau):
    if reseau in RESEAUX:
        RESEAUX[reseau]["responsable"] = None

def ajouter_evenement(reseau, texte):
    if reseau in RESEAUX:
        RESEAUX[reseau]["evenements"].insert(0, texte)
        RESEAUX[reseau]["evenements"] = RESEAUX[reseau]["evenements"][:10]
