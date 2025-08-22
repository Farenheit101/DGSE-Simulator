import random
from agents import Agent, ajouter_agent
from noms import generer_nom_prenom
from metiers import METIERS, choisir_metier_competence, generer_metier_aleatoire
from budget import debiter
from langues import LANGUES_PAR_PAYS
from bureaux import lister_bureaux
from datetime import datetime, timedelta
from bureaux import lister_bureaux

UNIVERSAL_AGENT_SKILLS = [
    "Infiltration", "Surveillance", "Hacking", "Langues étrangères",
    "Négociation", "Combat rapproché", "Crypto", "Conduite",
    "Déguisement", "Tir", "Protection", "Renseignement"
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
    for _ in range(nb):
        if ciblage and "pays" in ciblage:
            pays = ciblage["pays"]
        else:
            pays = random.choice(list(LANGUES_PAR_PAYS.keys()))
        from bureaux import lister_bureaux


        if ciblage and "bureau" in ciblage:
            bureau = ciblage["bureau"]
        elif ciblage and "competences" in ciblage:
            bureau = determiner_bureau_ideal(ciblage["competences"])
        else:
            bureau = determiner_bureau_ideal([])
        if ciblage and "competences" in ciblage:
            competences = list(ciblage["competences"])
            metier_infos = choisir_metier_competence(competences)
            if metier_infos:
                competences = metier_infos.get("competences", competences)
                universelles = [c for c in UNIVERSAL_AGENT_SKILLS if c not in competences]
                competences += random.sample(universelles, k=min(3, len(universelles)))
                metier_nom = metier_infos["metier"]
                entreprise = metier_infos["entreprise"]
            else:
                metier_infos = generer_metier_aleatoire()
                competences = list(metier_infos["competences"])  # Copie pour ne pas modifier l'original
                metier_nom = metier_infos["metier"]
                entreprise = metier_infos["entreprise"]

                # Ajoute 3 compétences universelles aléatoires non redondantes
                universelles = [c for c in UNIVERSAL_AGENT_SKILLS if c not in competences]
                competences += random.sample(universelles, k=min(3, len(universelles)))
        else:
            metier_infos = generer_metier_aleatoire()
            competences = metier_infos["competences"]
            universelles = [c for c in UNIVERSAL_AGENT_SKILLS if c not in competences]
            competences += random.sample(universelles, k=min(3, len(universelles)))
            metier_nom = metier_infos["metier"]
            entreprise = metier_infos["entreprise"]
        langues_poss = LANGUES_PAR_PAYS.get(pays, ["français"])
        nom, prenom = generer_nom_prenom(pays)
        statut_legende = (bureau == "BDL")
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

def valider_recrutement(profil, bureau_choisi, legende_nom_choisi=None, forcer=False):
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

def preparer_ciblage(bureau=None, competences=None, pays=None):
    ciblage = {}
    if bureau: ciblage["bureau"] = bureau
    if competences: ciblage["competences"] = competences
    if pays: ciblage["pays"] = pays
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

