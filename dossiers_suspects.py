# dossiers_suspects.py

import random
from datetime import datetime
from metiers import METIERS, generer_metier_aleatoire
from geographie import generer_nom_prenom

DOSSIERS_SUSPECTS = {}

class DossierSuspect:
    def __init__(self, nom, prenom, pays, crise_id, metier=None, entreprise=None, age=None, 
                 nationalite=None, adresse=None, telephone=None, email=None, 
                 antecedents=None, liens=None, notes=None):
        self.id = f"{nom}_{prenom}_{crise_id}"
        self.nom = nom
        self.prenom = prenom
        self.pays = pays
        self.crise_id = crise_id  # ID de la crise associée
        self.metier = metier or "Inconnu"
        self.entreprise = entreprise or "Inconnue"
        self.age = age or random.randint(25, 65)
        self.nationalite = nationalite or pays
        self.adresse = adresse or "Adresse inconnue"
        self.telephone = telephone or "Téléphone inconnu"
        self.email = email or "Email inconnu"
        self.antecedents = antecedents or []
        self.liens = liens or []  # Liens avec d'autres suspects
        self.notes = notes or []
        self.date_creation = datetime.now()
        self.derniere_mise_a_jour = datetime.now()
        
        # Informations glanées au cours des actions (à développer)
        self.informations_recueillies = []
        self.surveillances = []
        self.interceptions = []
        self.sources_humaines = []
        
    def ajouter_note(self, note, source="Agent"):
        """Ajoute une note au dossier"""
        timestamp = datetime.now()
        self.notes.append({
            "texte": note,
            "source": source,
            "date": timestamp
        })
        self.derniere_mise_a_jour = timestamp
        
    def ajouter_information(self, info, type_info="Général", source="Agent"):
        """Ajoute une information recueillie"""
        timestamp = datetime.now()
        self.informations_recueillies.append({
            "information": info,
            "type": type_info,
            "source": source,
            "date": timestamp
        })
        self.derniere_mise_a_jour = timestamp
        
    def ajouter_surveillance(self, lieu, duree, agent, resultat):
        """Ajoute une surveillance effectuée"""
        timestamp = datetime.now()
        self.surveillances.append({
            "lieu": lieu,
            "duree": duree,
            "agent": agent,
            "resultat": resultat,
            "date": timestamp
        })
        self.derniere_mise_a_jour = timestamp
        
    def ajouter_interception(self, type_interception, contenu, source):
        """Ajoute une interception de communication"""
        timestamp = datetime.now()
        self.interceptions.append({
            "type": type_interception,
            "contenu": contenu,
            "source": source,
            "date": timestamp
        })
        self.derniere_mise_a_jour = timestamp
        
    def ajouter_source_humaine(self, nom_source, information, fiabilite):
        """Ajoute une source humaine"""
        timestamp = datetime.now()
        self.sources_humaines.append({
            "nom": nom_source,
            "information": information,
            "fiabilite": fiabilite,
            "date": timestamp
        })
        self.derniere_mise_a_jour = timestamp
        
    def to_dict(self):
        """Convertit le dossier en dictionnaire pour la sauvegarde"""
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "pays": self.pays,
            "crise_id": self.crise_id,
            "metier": self.metier,
            "entreprise": self.entreprise,
            "age": self.age,
            "nationalite": self.nationalite,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "email": self.email,
            "antecedents": self.antecedents,
            "liens": self.liens,
            "notes": self.notes,
            "date_creation": self.date_creation,
            "derniere_mise_a_jour": self.derniere_mise_a_jour,
            "informations_recueillies": self.informations_recueillies,
            "surveillances": self.surveillances,
            "interceptions": self.interceptions,
            "sources_humaines": self.sources_humaines
        }
        
    @staticmethod
    def from_dict(data):
        """Crée un dossier suspect à partir d'un dictionnaire"""
        dossier = DossierSuspect(
            data["nom"], data["prenom"], data["pays"], data["crise_id"],
            data.get("metier"), data.get("entreprise"), data.get("age"),
            data.get("nationalite"), data.get("adresse"), data.get("telephone"),
            data.get("email"), data.get("antecedents"), data.get("liens"),
            data.get("notes")
        )
        
        # Restaurer les informations supplémentaires
        dossier.informations_recueillies = data.get("informations_recueillies", [])
        dossier.surveillances = data.get("surveillances", [])
        dossier.interceptions = data.get("interceptions", [])
        dossier.sources_humaines = data.get("sources_humaines", [])
        dossier.date_creation = data.get("date_creation", datetime.now())
        dossier.derniere_mise_a_jour = data.get("derniere_mise_a_jour", datetime.now())
        
        return dossier

def creer_dossier_suspect(nom, prenom, pays, crise_id, metier=None, entreprise=None):
    """Crée un nouveau dossier suspect"""
    if not metier:
        # Générer un métier aléatoire si aucun n'est fourni
        metier_info = generer_metier_aleatoire()
        metier = metier_info["metier"]
        entreprise = metier_info["entreprise"]
    
    dossier = DossierSuspect(nom, prenom, pays, crise_id, metier, entreprise)
    DOSSIERS_SUSPECTS[dossier.id] = dossier
    return dossier

def get_dossier_suspect(suspect_id):
    """Récupère un dossier suspect par son ID"""
    return DOSSIERS_SUSPECTS.get(suspect_id)

def lister_dossiers_crise(crise_id):
    """Liste tous les dossiers suspects d'une crise"""
    return [d for d in DOSSIERS_SUSPECTS.values() if d.crise_id == crise_id]

def supprimer_dossiers_crise(crise_id):
    """Supprime tous les dossiers suspects d'une crise (quand elle est terminée/supprimée)"""
    dossiers_a_supprimer = [d.id for d in DOSSIERS_SUSPECTS.values() if d.crise_id == crise_id]
    for dossier_id in dossiers_a_supprimer:
        if dossier_id in DOSSIERS_SUSPECTS:
            del DOSSIERS_SUSPECTS[dossier_id]
    return len(dossiers_a_supprimer)

def lister_tous_dossiers():
    """Liste tous les dossiers suspects"""
    return list(DOSSIERS_SUSPECTS.values())

def rechercher_suspects(nom=None, prenom=None, pays=None, metier=None):
    """Recherche des suspects selon différents critères"""
    resultats = []
    for dossier in DOSSIERS_SUSPECTS.values():
        if nom and nom.lower() not in dossier.nom.lower():
            continue
        if prenom and prenom.lower() not in dossier.prenom.lower():
            continue
        if pays and pays.lower() != dossier.pays.lower():
            continue
        if metier and metier.lower() not in dossier.metier.lower():
            continue
        resultats.append(dossier)
    return resultats
