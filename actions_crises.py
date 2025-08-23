# actions_crises.py

import random
from datetime import datetime, timedelta
from enum import Enum

class TypeAction(Enum):
    SURVEILLANCE = "Surveillance"
    INFILTRATION = "Infiltration"
    INTERCEPTION = "Interception"
    ARRESTATION = "Arrestation"
    NEUTRALISATION = "Neutralisation"
    RECUPERATION = "Récupération d'informations"
    SABOTAGE = "Sabotage"
    INFILTRATION_NUMERIQUE = "Infiltration numérique"
    ANALYSE_FORENSIQUE = "Analyse forensique"
    SURVEILLANCE_ELECTRONIQUE = "Surveillance électronique"
    OPERATION_COVERTE = "Opération covert"

class StatutAction(Enum):
    EN_ATTENTE = "En attente"
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    ECHEC = "Échec"
    ANNULEE = "Annulée"

class ActionCrise:
    def __init__(self, type_action, crise_id, agent_id=None, cible=None, 
                 cout=0, duree_minutes=60, description="", prerequis=None):
        self.id = f"ACTION_{random.randint(100000, 999999)}"
        self.type_action = type_action
        self.crise_id = crise_id
        self.agent_id = agent_id
        self.cible = cible  # Suspect ciblé ou lieu
        self.cout = cout
        self.duree_minutes = duree_minutes
        self.description = description
        self.prerequis = prerequis or []
        
        # État de l'action
        self.statut = StatutAction.EN_ATTENTE
        self.date_debut = None
        self.date_fin = None
        self.date_creation = datetime.now()
        
        # Résultats
        self.resultat = None
        self.informations_recueillies = []
        self.risques_encourus = []
        self.impact_crise = 0  # -100 à +100
        
        # Progression
        self.progression = 0
        self.etapes = []
        
    def demarrer(self, agent_nom, now):
        """Démarre l'action avec un agent"""
        if self.statut != StatutAction.EN_ATTENTE:
            return False, "Action déjà en cours ou terminée"
        
        self.agent_id = agent_nom  # Maintenant c'est le nom de l'agent
        self.date_debut = now
        self.date_fin = now + timedelta(minutes=self.duree_minutes)
        self.statut = StatutAction.EN_COURS
        self.progression = 0  # Commence à 0%
        
        return True, "Action démarrée"
    
    def avancer(self, points, etape_description=""):
        """Fait avancer l'action"""
        if self.statut != StatutAction.EN_COURS:
            return False, "Action non en cours"
        
        self.progression += points
        if etape_description:
            self.etapes.append({
                "description": etape_description,
                "date": datetime.now(),
                "progression": self.progression
            })
        
        # Vérifier si l'action est terminée
        if self.progression >= 100:
            self.terminer()
        
        return True, f"Progression: {self.progression}%"
    
    def terminer(self, resultat="Succès", informations=None):
        """Termine l'action avec un résultat"""
        self.statut = StatutAction.TERMINEE
        self.resultat = resultat
        self.progression = 100
        
        if informations:
            self.informations_recueillies.extend(informations)
        
        # Calculer l'impact sur la crise
        self._calculer_impact()
        
        return True, "Action terminée"
    
    def echouer(self, raison="Échec de l'opération"):
        """Marque l'action comme échouée"""
        self.statut = StatutAction.ECHEC
        self.resultat = raison
        self.progression = 100  # Marquer comme terminée
        
        # Calculer l'impact négatif sur la crise
        self._calculer_impact()
        
        return True, "Action échouée"
    
    def annuler(self, raison="Action annulée"):
        """Annule l'action"""
        self.statut = StatutAction.ANNULEE
        self.resultat = raison
        
        return True, "Action annulée"
    
    def _calculer_impact(self):
        """Calcule l'impact de l'action sur la crise"""
        base_impact = {
            TypeAction.SURVEILLANCE: 5,
            TypeAction.INFILTRATION: 15,
            TypeAction.INTERCEPTION: 10,
            TypeAction.ARRESTATION: 25,
            TypeAction.NEUTRALISATION: 30,
            TypeAction.RECUPERATION: 20,
            TypeAction.SABOTAGE: 35,
            TypeAction.INFILTRATION_NUMERIQUE: 12,
            TypeAction.ANALYSE_FORENSIQUE: 8,
            TypeAction.SURVEILLANCE_ELECTRONIQUE: 6,
            TypeAction.OPERATION_COVERTE: 40
        }
        
        impact_base = base_impact.get(self.type_action, 10)
        
        # Modificateurs selon le résultat
        if self.resultat == "Succès":
            self.impact_crise = impact_base + random.randint(0, 20)
        elif self.resultat == "Succès partiel":
            self.impact_crise = impact_base // 2 + random.randint(-5, 10)
        elif self.resultat == "Échec de l'opération":
            # Impact négatif plus important pour les échecs
            self.impact_crise = -(impact_base + random.randint(5, 25))
        else:
            self.impact_crise = -random.randint(5, 15)
    
    def to_dict(self):
        """Convertit l'action en dictionnaire"""
        return {
            "id": self.id,
            "type_action": self.type_action.value,
            "crise_id": self.crise_id,
            "agent_id": self.agent_id,
            "cible": self.cible,
            "cout": self.cout,
            "duree_minutes": self.duree_minutes,
            "description": self.description,
            "prerequis": self.prerequis,
            "statut": self.statut.value,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "date_creation": self.date_creation,
            "resultat": self.resultat,
            "informations_recueillies": self.informations_recueillies,
            "risques_encourus": self.risques_encourus,
            "impact_crise": self.impact_crise,
            "progression": self.progression,
            "etapes": self.etapes
        }

# Configuration des actions disponibles
ACTIONS_DISPONIBLES = {
    TypeAction.SURVEILLANCE: {
        "cout": 5000,
        "duree_minutes": 120,
        "description": "Surveillance discrète d'un suspect ou d'un lieu",
        "prerequis": ["agent_disponible"],
        "risques": ["Détection", "Échec de la surveillance"],
        "recompenses": ["Informations sur les mouvements", "Identification de contacts"]
    },
    
    TypeAction.INFILTRATION: {
        "cout": 15000,
        "duree_minutes": 240,
        "description": "Infiltration d'un lieu ou d'une organisation",
        "prerequis": ["agent_disponible", "competence_infiltration"],
        "risques": ["Détection", "Arrestation", "Compromission"],
        "recompenses": ["Accès aux informations", "Placement d'écoutes"]
    },
    
    TypeAction.INTERCEPTION: {
        "cout": 8000,
        "duree_minutes": 90,
        "description": "Interception de communications",
        "prerequis": ["agent_disponible", "equipement_interception"],
        "risques": ["Détection du matériel", "Échec technique"],
        "recompenses": ["Contenu des communications", "Identification des interlocuteurs"]
    },
    
    TypeAction.ARRESTATION: {
        "cout": 25000,
        "duree_minutes": 180,
        "description": "Arrestation d'un suspect",
        "prerequis": ["agent_disponible", "competence_combat", "competence_securite", "support_local"],
        "risques": ["Résistance armée", "Évasion", "Compromission"],
        "recompenses": ["Suspect en détention", "Interrogatoire possible"]
    },
    
    TypeAction.NEUTRALISATION: {
        "cout": 35000,
        "duree_minutes": 120,
        "description": "Neutralisation d'une menace",
        "prerequis": ["agent_disponible", "competence_combat", "competence_securite", "autorisation"],
        "risques": ["Échec de la neutralisation", "Victimes collatérales", "Compromission"],
        "recompenses": ["Menace éliminée", "Récupération d'équipements"]
    },
    
    TypeAction.RECUPERATION: {
        "cout": 12000,
        "duree_minutes": 150,
        "description": "Récupération d'informations ou d'objets",
        "prerequis": ["agent_disponible", "competence_infiltration", "competence_analyse"],
        "risques": ["Détection", "Échec de la récupération"],
        "recompenses": ["Informations sensibles", "Preuves matérielles"]
    },
    
    TypeAction.SABOTAGE: {
        "cout": 20000,
        "duree_minutes": 200,
        "description": "Sabotage d'équipements ou d'installations",
        "prerequis": ["agent_disponible", "competence_technique", "competence_securite"],
        "risques": ["Détection", "Échec du sabotage", "Compromission"],
        "recompenses": ["Capacités ennemies réduites", "Délais imposés"]
    },
    
    TypeAction.INFILTRATION_NUMERIQUE: {
        "cout": 10000,
        "duree_minutes": 180,
        "description": "Infiltration numérique d'un système",
        "prerequis": ["agent_disponible", "competence_hacking"],
        "risques": ["Détection", "Contre-attaque", "Traçage"],
        "recompenses": ["Accès aux données", "Surveillance continue"]
    },
    

    
    TypeAction.ANALYSE_FORENSIQUE: {
        "cout": 6000,
        "duree_minutes": 240,
        "description": "Analyse forensique d'éléments récupérés",
        "prerequis": ["agent_disponible", "competence_technique", "competence_analyse", "laboratoire"],
        "risques": ["Échec de l'analyse", "Contamination des preuves"],
        "recompenses": ["Informations détaillées", "Preuves exploitables"]
    },
    
    TypeAction.SURVEILLANCE_ELECTRONIQUE: {
        "cout": 7000,
        "duree_minutes": 120,
        "description": "Surveillance électronique et SIGINT",
        "prerequis": ["agent_disponible", "equipement_sigint"],
        "risques": ["Détection", "Brouillage", "Échec technique"],
        "recompenses": ["Communications interceptées", "Données techniques"]
    },
    
    TypeAction.OPERATION_COVERTE: {
        "cout": 50000,
        "duree_minutes": 360,
        "description": "Opération covert complexe multi-phases",
        "prerequis": ["agent_disponible", "competence_infiltration", "competence_gestion", "support_equipe"],
        "risques": ["Détection", "Compromission majeure", "Échec total"],
        "recompenses": ["Objectif principal atteint", "Informations critiques"]
    }
}

def creer_action(type_action, crise_id, agent_nom=None, cible=None):
    """Crée une nouvelle action pour une crise"""
    if type_action not in ACTIONS_DISPONIBLES:
        return None, "Type d'action non reconnu"
    
    config = ACTIONS_DISPONIBLES[type_action]
    
    action = ActionCrise(
        type_action=type_action,
        crise_id=crise_id,
        agent_id=agent_nom,  # Maintenant c'est le nom de l'agent
        cible=cible,
        cout=config["cout"],
        duree_minutes=config["duree_minutes"],
        description=config["description"],
        prerequis=config["prerequis"]
    )
    
    return action, "Action créée"

def lister_actions_disponibles():
    """Liste toutes les actions disponibles avec leurs détails"""
    return ACTIONS_DISPONIBLES

def verifier_prerequis(action, agent, equipements_disponibles=None):
    """Vérifie si les prérequis d'une action sont satisfaits"""
    if not agent:
        return False, "Aucun agent spécifié"
    
    prerequis = action.prerequis
    equipements_disponibles = equipements_disponibles or []
    
    # 1) Vérifier les prérequis non liés aux compétences (équipements, autorisations, disponibilité)
    for p in prerequis:
        if p == "agent_disponible":
            # Utiliser le nouveau système de statut si disponible
            if hasattr(agent, 'est_disponible'):
                if not agent.est_disponible():
                    return False, "Agent non disponible"
            else:
                if not hasattr(agent, 'en_mission') or agent.en_mission():
                    return False, "Agent non disponible"
        
        elif p == "equipement_interception":
            if "Équipement d'interception" not in equipements_disponibles:
                return False, "Équipement d'interception non disponible"
        
        elif p == "equipement_sigint":
            if "Équipement SIGINT" not in equipements_disponibles:
                return False, "Équipement SIGINT non disponible"
        
        elif p == "laboratoire":
            if "Laboratoire forensique" not in equipements_disponibles:
                return False, "Laboratoire forensique non disponible"
        
        elif p == "support_local":
            if "Support local" not in equipements_disponibles:
                return False, "Support local non disponible"
        
        elif p == "autorisation":
            if "Autorisation spéciale" not in equipements_disponibles:
                return False, "Autorisation spéciale requise"
        
        elif p == "support_equipe":
            if "Support d'équipe" not in equipements_disponibles:
                return False, "Support d'équipe non disponible"
    
    # 2) Gérer les prérequis de compétences avec logique "AU MOINS 1" + comptage pour bonus
    competences_requises = [p for p in prerequis if p.startswith("competence_")]
    if competences_requises:
        agent_comps_lower = [c.lower() for c in getattr(agent, 'competences', [])]
        
        def match_comp(pr):
            key = pr.replace("competence_", "")
            if key == "infiltration":
                return "infiltration" in agent_comps_lower
            if key == "combat":
                return any(x in agent_comps_lower for x in ["combat rapproché", "combat"])
            if key == "hacking":
                return "hacking" in agent_comps_lower
            if key == "negociation":
                return "négociation" in agent_comps_lower or "negociation" in agent_comps_lower
            if key == "technique":
                return any(x in agent_comps_lower for x in ["hacking", "crypto", "infiltration", "technique"])
            if key == "analyse":
                return "analyse" in agent_comps_lower
            if key == "securite":
                return "sécurité" in agent_comps_lower or "securité" in agent_comps_lower or "securite" in agent_comps_lower
            if key == "recherche":
                return "recherche" in agent_comps_lower
            if key == "gestion":
                return "gestion" in agent_comps_lower
            if key == "surveillance":
                return "surveillance" in agent_comps_lower
            # Par défaut, tenter une correspondance directe
            return key in agent_comps_lower
        
        nb_ok = sum(1 for pr in competences_requises if match_comp(pr))
        if nb_ok == 0:
            return False, "Agent ne possède aucune des compétences requises"
        # NB: le bonus de vitesse sera appliqué au lancement (gestionnaire_actions)
    
    return True, "Tous les prérequis sont satisfaits"

def calculer_cout_action(type_action, modificateurs=None):
    """Calcule le coût d'une action avec modificateurs"""
    if type_action not in ACTIONS_DISPONIBLES:
        return 0
    
    cout_base = ACTIONS_DISPONIBLES[type_action]["cout"]
    modificateurs = modificateurs or {}
    
    # Modificateurs de coût
    if modificateurs.get("urgence"):
        cout_base *= 1.5  # +50% pour urgence
    
    if modificateurs.get("risque_eleve"):
        cout_base *= 1.3  # +30% pour risque élevé
    
    if modificateurs.get("zone_difficile"):
        cout_base *= 1.2  # +20% pour zone difficile
    
    if modificateurs.get("discount_relation"):
        cout_base *= 0.8  # -20% pour relations locales
    
    return int(cout_base)
