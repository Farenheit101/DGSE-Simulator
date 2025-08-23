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
            "competences": [skill]
        }
    return catalogue

FORMATIONS_CATALOGUE = _build_catalogue()


# Formations en cours: liste de dicts {agent, nom_formation, date_debut, date_fin, cout, statut}
FORMATIONS_EN_COURS = []


def lister_formations_catalogue():
    return FORMATIONS_CATALOGUE


def lister_formations_en_cours():
    return list(FORMATIONS_EN_COURS)


def _ajouter_competences_agent(agent, competences):
    """Ajoute proprement des compétences à l'agent (sans doublons)."""
    actuelles_lower = {c.lower() for c in getattr(agent, "competences", [])}
    for c in competences:
        if c.lower() not in actuelles_lower:
            agent.competences.append(c)
            actuelles_lower.add(c.lower())


def planifier_formation(agent, nom_formation, current_game_time):
    """
    Planifie une formation pour un agent si budget suffisant et agent disponible.
    - Débite le budget
    - Place l'agent en statut "En formation"
    - Enregistre la formation dans FORMATIONS_EN_COURS
    """
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
        "statut": "En cours"
    })

    return True, f"Formation planifiée: {nom_formation} — Fin le {date_fin.strftime('%d/%m/%Y %H:%M')}"


def finaliser_formations(current_time):
    """Vérifie les formations et finalise celles arrivées à échéance."""
    terminees = []
    for f in FORMATIONS_EN_COURS:
        if f.get("statut") != "En cours":
            continue
        if f.get("date_fin") and current_time >= f["date_fin"]:
            agent = f["agent"]
            nom_formation = f["nom_formation"]
            cfg = FORMATIONS_CATALOGUE.get(nom_formation, {})
            competences = cfg.get("competences", [])
            _ajouter_competences_agent(agent, competences)

            # Donner un peu d'XP
            try:
                if hasattr(agent, "add_experience"):
                    agent.add_experience(random.randint(20, 40))
            except Exception:
                pass

            # Remettre l'agent disponible
            try:
                agent.changer_statut("Disponible", f"Formation terminée: {nom_formation}")
            except Exception:
                pass

            f["statut"] = "Terminée"
            terminees.append(f)
            print(f"INFO: Formation terminée — {agent.nom} {agent.prenom} a acquis: {', '.join(competences)}")

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


