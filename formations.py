# formations.py

import random
from datetime import timedelta

import budget
from recrutement import UNIVERSAL_AGENT_SKILLS

# Catalogue des formations disponibles (généré à partir des compétences universelles ET des prérequis d'actions)
# Chaque entrée définit: coût (€), durée (jours ingame), compétences gagnées (liste)

# Compétences utilisées dans les prérequis d'actions (noms canoniques)
_ACTION_PREREQ_SKILLS = {
    "Infiltration", "Combat rapproché", "Hacking", "Négociation", "Technique",
    "Analyse", "Sécurité", "Recherche", "Gestion", "Surveillance"
}

# Config coûts/durées par compétence
_SKILL_CONFIG = {
    "Infiltration": {"cout": 8000, "duree_jours": 5},
    "Surveillance": {"cout": 6000, "duree_jours": 4},
    "Hacking": {"cout": 12000, "duree_jours": 7},
    "Analyse": {"cout": 7000, "duree_jours": 4},
    "Sécurité": {"cout": 9000, "duree_jours": 6},
    "Combat rapproché": {"cout": 9500, "duree_jours": 6},
    "Gestion": {"cout": 8000, "duree_jours": 5},
    "Négociation": {"cout": 7000, "duree_jours": 4},
    "Technique": {"cout": 9000, "duree_jours": 6},
    "Recherche": {"cout": 6500, "duree_jours": 4},
}

# Import de la source unique des langues
from langues import obtenir_toutes_langues

# Configuration des coûts et difficultés par langue
# Génération automatique basée sur la source unique de vérité
def _generer_config_langue(langue):
    """Génère automatiquement la configuration pour une langue"""
    # Langues faciles (familles latines/germaniques proches)
    faciles = ["anglais", "espagnol", "italien", "portugais", "afrikaans", "néerlandais", "gallois"]
    
    # Langues moyennes (européennes, similitudes structurelles)
    moyennes = ["allemand", "français", "suédois", "norvégien", "danois", "polonais", "tchèque", 
               "bulgare", "roumain", "serbe", "croate", "slovaque", "slovène", "ukrainien",
               "hindi", "turc", "malais", "indonésien", "swahili", "wolof", "bambara", "kurde"]
    
    # Langues difficiles (systèmes d'écriture différents, grammaires complexes)
    difficiles = ["russe", "grec", "arabe", "hébreu", "hongrois", "finnois", "lituanien", 
                 "letton", "estonien", "maltais", "albanais", "géorgien", "arménien", "azéri",
                 "kazakh", "ouzbek", "kirghiz", "tadjik", "turkmène", "persan", "pashto", "dari",
                 "amharique", "bengali", "tamoul", "télougou", "marathi", "gujarati", "kannada",
                 "malayalam", "ourdou", "pendjabi", "sindhi", "népalais", "singhalais", "vietnamien",
                 "thaï", "birmane", "laotien", "khmer", "tagalog", "maori", "quechua", "aymara", "guarani"]
    
    # Langues très difficiles (tonales, logographiques, très éloignées)
    tres_difficiles = ["chinois", "japonais", "coréen", "islandais", "mongol", "divehi", "haoussa",
                      "yoruba", "igbo", "zoulou", "xhosa", "lingala", "cantonais", "mandarin"]
    
    langue_lower = langue.lower()
    
    if langue_lower in faciles:
        return {"cout": random.randint(5000, 7000), "duree_jours": random.randint(3, 4), "difficulte": "facile"}
    elif langue_lower in moyennes:
        return {"cout": random.randint(7000, 9000), "duree_jours": random.randint(4, 5), "difficulte": "moyenne"}
    elif langue_lower in difficiles:
        return {"cout": random.randint(8000, 11000), "duree_jours": random.randint(5, 6), "difficulte": "difficile"}
    elif langue_lower in tres_difficiles:
        return {"cout": random.randint(10000, 12000), "duree_jours": random.randint(6, 8), "difficulte": "très difficile"}
    else:
        # Par défaut : moyenne
        return {"cout": 8000, "duree_jours": 5, "difficulte": "moyenne"}

# Génération automatique du catalogue des formations linguistiques
def _generer_langues_formations():
    """Génère automatiquement le catalogue des formations linguistiques depuis langues.py"""
    import random
    catalogue = {}
    toutes_langues = obtenir_toutes_langues()
    
    for langue in toutes_langues:
        config = _generer_config_langue(langue)
        catalogue[langue] = config
    
    return catalogue

# Catalogue généré automatiquement
_LANGUES_FORMATIONS = _generer_langues_formations()

def _build_catalogue():
    allowed = sorted(set(UNIVERSAL_AGENT_SKILLS) & _ACTION_PREREQ_SKILLS)
    catalogue = {}
    for skill in allowed:
        cfg = _SKILL_CONFIG.get(skill, {"cout": 8000, "duree_jours": 5})
        # Un item = une seule compétence gagnée
        nom = skill
        catalogue[nom] = {
            "cout": int(cfg["cout"]),
            "duree_jours": int(cfg["duree_jours"]),
            "competences": [skill],
            "type": "competence"
        }
    return catalogue

def _build_catalogue_langues():
    """Construit le catalogue des formations linguistiques"""
    catalogue = {}
    for langue, config in _LANGUES_FORMATIONS.items():
        catalogue[f"Langue: {langue.title()}"] = {
            "cout": int(config["cout"]),
            "duree_jours": int(config["duree_jours"]),
            "langue": langue,
            "difficulte": config["difficulte"],
            "type": "langue"
        }
    return catalogue

FORMATIONS_CATALOGUE = _build_catalogue()
FORMATIONS_LANGUES_CATALOGUE = _build_catalogue_langues()

# Formations en cours: liste de dicts {agent, nom_formation, date_debut, date_fin, cout, statut}
FORMATIONS_EN_COURS = []

def lister_formations_catalogue():
    return FORMATIONS_CATALOGUE

def lister_formations_langues_catalogue():
    """Liste le catalogue des formations linguistiques"""
    return FORMATIONS_LANGUES_CATALOGUE

def lister_formations_en_cours():
    return list(FORMATIONS_EN_COURS)

def _ajouter_competences_agent(agent, competences):
    """Ajoute proprement des compétences à l'agent (sans doublons)."""
    actuelles_lower = {c.lower() for c in getattr(agent, "competences", [])}
    for c in competences:
        if c.lower() not in actuelles_lower:
            agent.competences.append(c)
            actuelles_lower.add(c.lower())

def _ajouter_langue_agent(agent, langue):
    """Ajoute une langue à l'agent (sans doublon et respecte la limite de 5 langues)"""
    if not hasattr(agent, 'langues'):
        agent.langues = []
    
    # Vérifier la limite de 5 langues
    if len(agent.langues) >= 5:
        return False, "L'agent a déjà atteint la limite de 5 langues"
    
    # Vérifier si la langue n'est pas déjà présente
    if langue.lower() not in [l.lower() for l in agent.langues]:
        agent.langues.append(langue)
        return True, f"Langue '{langue}' ajoutée avec succès"
    else:
        return False, f"L'agent maîtrise déjà la langue '{langue}'"

def planifier_formation(agent, nom_formation, current_game_time):
    """
    Planifie une formation pour un agent si budget suffisant et agent disponible.
    - Débite le budget
    - Place l'agent en statut "En formation"
    - Enregistre la formation dans FORMATIONS_EN_COURS
    """
    # Vérifier si c'est une formation de compétence ou de langue
    if nom_formation in FORMATIONS_CATALOGUE:
        # Formation de compétence
        if nom_formation not in FORMATIONS_CATALOGUE:
            return False, "Formation inconnue"

        if not getattr(agent, "est_disponible", None) or not agent.est_disponible():
            return False, "Agent non disponible"

        cfg = FORMATIONS_CATALOGUE[nom_formation]
        cout = int(cfg.get("cout", 0))
        duree_jours = int(cfg.get("duree_jours", 3))

        # Paiement
        if not budget.debiter(cout, f"Formation '{nom_formation}' pour {agent.nom} {agent.prenom}"):
            return False, f"Budget insuffisant. Coût: {cout}€"

        date_debut = current_game_time
        date_fin = current_game_time + timedelta(days=duree_jours)

        # Statut agent
        try:
            agent.changer_statut("En formation", f"Formation: {nom_formation}", date_debut=date_debut)
        except Exception:
            pass

        FORMATIONS_EN_COURS.append({
            "agent": agent,
            "nom_formation": nom_formation,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "cout": cout,
            "statut": "En cours",
            "type": "competence"
        })

        return True, f"Formation planifiée: {nom_formation} — Fin le {date_fin.strftime('%d/%m/%Y %H:%M')}"
    
    elif nom_formation in FORMATIONS_LANGUES_CATALOGUE:
        # Formation linguistique
        if not getattr(agent, "est_disponible", None) or not agent.est_disponible():
            return False, "Agent non disponible"

        cfg = FORMATIONS_LANGUES_CATALOGUE[nom_formation]
        cout = int(cfg.get("cout", 0))
        duree_jours = int(cfg.get("duree_jours", 3))
        langue = cfg.get("langue", "")

        # Vérifier la limite de langues
        if hasattr(agent, 'langues') and len(agent.langues) >= 5:
            return False, "L'agent a déjà atteint la limite de 5 langues"

        # Vérifier si l'agent maîtrise déjà cette langue
        if hasattr(agent, 'langues') and langue.lower() in [l.lower() for l in agent.langues]:
            return False, f"L'agent maîtrise déjà la langue '{langue}'"

        # Paiement
        if not budget.debiter(cout, f"Formation linguistique '{langue}' pour {agent.nom} {agent.prenom}"):
            return False, f"Budget insuffisant. Coût: {cout}€"

        date_debut = current_game_time
        date_fin = current_game_time + timedelta(days=duree_jours)

        # Statut agent
        try:
            agent.changer_statut("En formation", f"Formation linguistique: {langue}", date_debut=date_debut)
        except Exception:
            pass

        FORMATIONS_EN_COURS.append({
            "agent": agent,
            "nom_formation": nom_formation,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "cout": cout,
            "statut": "En cours",
            "type": "langue",
            "langue": langue
        })

        return True, f"Formation linguistique planifiée: {langue} — Fin le {date_fin.strftime('%d/%m/%Y %H:%M')}"
    
    else:
        return False, "Formation inconnue"


def finaliser_formations(current_time):
    """Vérifie les formations et finalise celles arrivées à échéance."""
    terminees = []
    for f in FORMATIONS_EN_COURS:
        if f.get("statut") != "En cours":
            continue
        if f.get("date_fin") and current_time >= f["date_fin"]:
            agent = f["agent"]
            nom_formation = f["nom_formation"]
            
            if f.get("type") == "langue":
                # Formation linguistique
                cfg = FORMATIONS_LANGUES_CATALOGUE.get(nom_formation, {})
                langue = cfg.get("langue", "")
                
                # Ajouter la langue à l'agent
                succes, message = _ajouter_langue_agent(agent, langue)
                if succes:
                    print(f"INFO: Formation linguistique terminée — {agent.nom} {agent.prenom} a acquis: {langue}")
                    # Mettre à jour la fiche agent si elle existe
                    try:
                        import fiches
                        fiche_id = f"{agent.nom}_{agent.prenom}_{agent.bureau}"
                        if fiches.get_fiche(fiche_id) is not None:
                            fiches.ajouter_info_fiche(fiche_id, "Langues", ", ".join(agent.langues))
                    except Exception:
                        pass
                else:
                    print(f"ERREUR: Impossible d'ajouter la langue {langue}: {message}")
                
                # Donner un peu d'XP
                try:
                    if hasattr(agent, "add_experience"):
                        agent.add_experience(random.randint(15, 25))
                except Exception:
                    pass
                
            else:
                # Formation de compétence (ancien système)
                cfg = FORMATIONS_CATALOGUE.get(nom_formation, {})
                competences = cfg.get("competences", [])
                _ajouter_competences_agent(agent, competences)

                # Donner un peu d'XP
                try:
                    if hasattr(agent, "add_experience"):
                        agent.add_experience(random.randint(20, 40))
                except Exception:
                    pass

                print(f"INFO: Formation terminée — {agent.nom} {agent.prenom} a acquis: {', '.join(competences)}")

            # Remettre l'agent disponible
            try:
                agent.changer_statut("Disponible", f"Formation terminée: {nom_formation}")
            except Exception:
                pass

            f["statut"] = "Terminée"
            terminees.append(f)

    # Nettoyage (laisser les terminées consultables si besoin, sinon retirer)
    # Ici, on les laisse dans la liste avec statut "Terminée" pour l'historique visuel
    return terminees


def annuler_formation(index):
    """Annule une formation en cours (remboursement partiel)."""
    if 0 <= index < len(FORMATIONS_EN_COURS):
        f = FORMATIONS_EN_COURS[index]
        if f.get("statut") == "En cours":
            # Remboursement 30%
            remboursement = int(f.get("cout", 0) * 0.3)
            budget.crediter(remboursement, f"Remboursement formation annulée: {f.get('nom_formation')}")
            try:
                ag = f.get("agent")
                if ag:
                    ag.changer_statut("Disponible", "Formation annulée")
            except Exception:
                pass
            f["statut"] = "Annulée"
            return True, f"Formation annulée. Remboursement: {remboursement}€"
    return False, "Aucune formation en cours à cet index"


