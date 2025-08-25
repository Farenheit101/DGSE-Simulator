import random
from agents import Agent, ajouter_agent, generer_langues
from noms import generer_nom_prenom
from metiers import METIERS, choisir_metier_competence, generer_metier_aleatoire
from budget import debiter
import budget
from langues import LANGUES_PAR_PAYS
from bureaux import lister_bureaux
from datetime import datetime, timedelta

UNIVERSAL_AGENT_SKILLS = [
    "Infiltration", "Surveillance", "Hacking", "Langues étrangères",
    "Négociation", "Combat rapproché", "Crypto", "Conduite",
    "Déguisement", "Tir", "Protection", "Renseignement",
    "Analyse", "Technique", "Sécurité", "Gestion", "Recherche"
]
METIER_SKILLS = set()
for metier in METIERS.values():
    METIER_SKILLS.update(metier["competences"])

def generer_competences_agent():
    agent_skills = set(random.sample(UNIVERSAL_AGENT_SKILLS, 3))
    metier_extras = list(METIER_SKILLS - agent_skills)
    if metier_extras:
        agent_skills.update(random.sample(metier_extras, 1))
    return list(agent_skills)

def extraire_competences_metier(agent_competences):
    return sorted(set(agent_competences) & METIER_SKILLS)

def extraire_competences_universelles(agent_competences):
    return sorted(set(agent_competences) & set(UNIVERSAL_AGENT_SKILLS))

def generer_profils(nb, ciblage=None):
    profils = []
    
    # Pour le recrutement ciblé par compétences, s'assurer qu'au moins le premier profil ait la compétence
    competences_requises = None
    if ciblage and "competences" in ciblage:
        competences_requises = ciblage["competences"]
        if not isinstance(competences_requises, list):
            competences_requises = [competences_requises]
    
    for i in range(nb):
        # Déterminer d'abord le pays (priorité au ciblage)
        if ciblage and "pays" in ciblage:
            pays = ciblage["pays"]
        else:
            # Pays par défaut si pas de ciblage
            pays = "france"
        
        # Génération du profil de base (maintenant que pays est défini)
        nom, prenom = generer_nom_prenom(pays)
        bureau = determiner_bureau_ideal([])
        
        # Application du ciblage
        if ciblage:
            if "bureau" in ciblage:
                bureau = ciblage["bureau"]
            if "langue" in ciblage:
                # Ciblage par langue : forcer l'inclusion de cette langue
                langue_cible = ciblage["langue"]
                langues_poss = [langue_cible]  # Commencer par la langue ciblée
                # Ajouter 1-2 langues supplémentaires aléatoirement
                autres_langues = [l for l in LANGUES_PAR_PAYS.get(pays.lower(), ["français"]) if l != langue_cible]
                if autres_langues:
                    nb_autres = random.randint(1, min(2, len(autres_langues)))
                    langues_poss.extend(random.sample(autres_langues, nb_autres))
            else:
                # Génération normale des langues
                langues_poss = generer_langues(pays, random.randint(2, 4))
        else:
            langues_poss = generer_langues(pays, random.randint(2, 4))
        
        # Génération des compétences
        competences = generer_competences_agent()
        
        # Pour le premier profil en cas de ciblage par compétences, garantir la présence de la compétence
        if i == 0 and competences_requises:
            # S'assurer que le premier profil a AU MOINS une des compétences requises
            a_competence_requise = any(comp in competences for comp in competences_requises)
            if not a_competence_requise:
                # Remplacer une compétence aléatoire par la première compétence requise
                if competences:
                    competences[random.randint(0, len(competences)-1)] = competences_requises[0]
                else:
                    competences.append(competences_requises[0])
        
        # Application du ciblage des compétences
        if ciblage and "competences" in ciblage:
            comp_ciblees = ciblage["competences"]
            if isinstance(comp_ciblees, list):
                # Ajouter les compétences ciblées si pas déjà présentes
                for comp in comp_ciblees:
                    if comp not in competences:
                        competences.append(comp)
            else:
                # Compétence unique
                if comp_ciblees not in competences:
                    competences.append(comp_ciblees)
        
        # Génération du métier
        metier_info = generer_metier_aleatoire()
        metier_nom = metier_info["metier"]
        entreprise = metier_info["entreprise"]
        
        # Calcul du coût
        statut_legende = False
        legende_nom = None
        cout = 30000 if statut_legende else 15000 if bureau == "BDL" else 10000
        bonus_comp = sum(1 for c in competences if c in ["Hacking", "Crypto", "Déguisement"])
        bonus_langue = max(0, len(langues_poss) - 1)
        cout += bonus_comp * 2500 + bonus_langue * 2000

        comp_metier = extraire_competences_metier(competences)
        comp_univ = extraire_competences_universelles(competences)

        profil = {
            "nom": nom,
            "prenom": prenom,
            "pays": pays,
            "bureau_ideal": bureau,
            "competences": competences,
            "langues": langues_poss,
            "statut_legende": statut_legende,
            "legende_nom": legende_nom,
            "cout": cout,
            "comp_univ": comp_univ,
            "comp_metier": comp_metier,
            "metier": metier_nom,
            "entreprise": entreprise,
        }
        # Nouveau système: harmonise l'affichage du coût si activé
        if budget.is_new_budget_enabled():
            type_recrutement = "classique" if not ciblage else "cible"
            profil["cout"] = budget.cout_recrutement_mode(type_recrutement)
        profils.append(profil)
    return profils

def generer_profils_apres_delai(nb, cible, callback, delay=7):
    def tache():
        import time
        time.sleep(delay)
        profils = generer_profils(nb, cible)
        callback(profils)
    import threading
    thread = threading.Thread(target=tache)
    thread.start()

def generer_profils_blocant(nb, ciblage=None, delay=7):
    import time
    time.sleep(delay)
    return generer_profils(nb, ciblage)

def valider_recrutement(profil, bureau_choisi, legende_nom_choisi=None, forcer=False, type_recrutement=None):
    # Détermine le coût en fonction du système actif
    if budget.is_new_budget_enabled():
        # Nouveau modèle: coût fixe selon le type
        t = type_recrutement or ("classique" if profil is None else ("classique" if profil and profil.get("bureau_ideal") else "classique"))
        cout = budget.cout_recrutement_mode(t)
        risque = 1 if (forcer and bureau_choisi != profil.get("bureau_ideal")) else 0
    else:
        # Ancien modèle conservé tant que le flag est désactivé
        cout = profil["cout"]
        risque = 0
        if forcer and bureau_choisi != profil["bureau_ideal"]:
            cout += 5000
            risque = 1
    if not debiter(cout, f"Recrutement agent ({profil['nom']} {profil['prenom']})"):
        return None, "Fonds insuffisants"
    agent = Agent(
        profil["nom"], profil["prenom"], profil["pays"], bureau_choisi,
        profil["competences"], profil["langues"], niveau=1,
        statut_legende=(bureau_choisi == "BDL"),
        legende_nom=None
    )
    ajouter_agent(agent)
    return agent, risque

def preparer_ciblage(bureau=None, competences=None, pays=None, langue=None):
    ciblage = {}
    if bureau: ciblage["bureau"] = bureau
    if competences: ciblage["competences"] = competences
    if pays: ciblage["pays"] = pays
    if langue: ciblage["langue"] = langue
    return ciblage
    
def determiner_bureau_ideal(competences):
    competence_map = {
        "infiltration": "DO",
        "négociation": "DR",
        "renseignement": "DR",
        "hacking": "DT",
        "crypto": "DT",
        "conduite": "DO",
        "déguisement": "BDL",
        "surveillance": "DR",
        "tir": "DO",
        "protection": "DO",
        "langues étrangères": "DR",
        "combat rapproché": "DO"
    }
    for comp in competences:
        b = competence_map.get(comp.lower())
        if b:
            return b
    return random.choice(lister_bureaux())

