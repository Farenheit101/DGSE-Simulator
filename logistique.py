# logistique.py

from datetime import datetime, timedelta

LOGISTIQUE = {
    "materiel": [],
    "plans": [],
    "exfiltrations": [],
    "moyens": []
}

def ajouter_materiel(nom, quantite=1, affectation=None):
    LOGISTIQUE["materiel"].append({"nom": nom, "quantite": quantite, "affectation": affectation})

def lister_materiel():
    return list(LOGISTIQUE["materiel"])

def ajouter_plan(nom, description):
    LOGISTIQUE["plans"].append({"nom": nom, "description": description})

def lister_plans():
    return list(LOGISTIQUE["plans"])

def ajouter_exfiltration(agent, lieu, statut="En attente", date_debut=None, date_fin=None):
    # Ajout gestion temps (date_debut/date_fin) si souhaité
    exf = {"agent": agent, "lieu": lieu, "statut": statut, "date_debut": date_debut, "date_fin": date_fin}
    LOGISTIQUE["exfiltrations"].append(exf)
    return exf

def lister_exfiltrations():
    return list(LOGISTIQUE["exfiltrations"])

def ajouter_moyen(type_moyen, details):
    LOGISTIQUE["moyens"].append({"type": type_moyen, "details": details})

def lister_moyens():
    return list(LOGISTIQUE["moyens"])
