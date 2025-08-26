# reseaux.py

RESEAUX = {}
from datetime import datetime

def calculer_bonus_langue_agent(agent, pays_cible):
    """
    Calcule les bonus de création de réseau basés sur les langues de l'agent
    Retourne un dictionnaire avec les différents bonus
    """
    try:
        from geographie import LANGUES_PAR_PAYS
        
        # Récupérer les langues du pays cible
        langues_pays = LANGUES_PAR_PAYS.get(pays_cible.lower(), [])
        if not langues_pays:
            return {
                "chance_succes": 0,
                "reduction_cout": 0,
                "reduction_duree": 0,
                "bonus_qualite": 0,
                "langues_maitrisees": [],
                "langues_pays": []
            }
        
        # Récupérer les langues de l'agent
        langues_agent = getattr(agent, 'langues', [])
        if not langues_agent:
            return {
                "chance_succes": 0,
                "reduction_cout": 0,
                "reduction_duree": 0,
                "bonus_qualite": 0,
                "langues_maitrisees": [],
                "langues_pays": langues_pays
            }
        
        # Normaliser les langues pour la comparaison
        langues_pays_norm = [l.lower() for l in langues_pays]
        langues_agent_norm = [l.lower() for l in langues_agent]
        
        # Trouver les langues communes
        langues_communes = [l for l in langues_agent_norm if l in langues_pays_norm]
        
        # Calculer les bonus
        bonus = {
            "chance_succes": 0,
            "reduction_cout": 0,
            "reduction_duree": 0,
            "bonus_qualite": 0,
            "langues_maitrisees": langues_communes,
            "langues_pays": langues_pays
        }
        
        if langues_communes:
            # Langue principale du pays (première dans la liste)
            langue_principale = langues_pays_norm[0]
            parle_langue_principale = langue_principale in langues_communes
            
            # Bonus de chance de succès
            if parle_langue_principale:
                bonus["chance_succes"] = 15  # +15% si parle la langue principale
            elif len(langues_communes) >= 2:
                bonus["chance_succes"] = 10  # +10% si parle au moins 2 langues du pays
            else:
                bonus["chance_succes"] = 5   # +5% si parle au moins 1 langue du pays
            
            # Réduction de coût
            if parle_langue_principale:
                bonus["reduction_cout"] = 20  # -20% si parle la langue principale
            elif len(langues_communes) >= 2:
                bonus["reduction_cout"] = 15  # -15% si parle au moins 2 langues
            else:
                bonus["reduction_cout"] = 10  # -10% si parle au moins 1 langue
            
            # Réduction de durée
            if parle_langue_principale:
                bonus["reduction_duree"] = 30  # -30% si parle la langue principale
            elif len(langues_communes) >= 2:
                bonus["reduction_duree"] = 20  # -20% si parle au moins 2 langues
            else:
                bonus["reduction_duree"] = 10  # -10% si parle au moins 1 langue
            
            # Bonus de qualité
            if parle_langue_principale:
                bonus["bonus_qualite"] = 25  # +25% de qualité si parle la langue principale
            elif len(langues_communes) >= 2:
                bonus["bonus_qualite"] = 15  # +15% de qualité si parle au moins 2 langues
            else:
                bonus["bonus_qualite"] = 10  # +10% de qualité si parle au moins 1 langue
        
        return bonus
        
    except ImportError:
        # Fallback si le module langues n'est pas disponible
        return {
            "chance_succes": 0,
            "reduction_cout": 0,
            "reduction_duree": 0,
            "bonus_qualite": 0,
            "langues_maitrisees": [],
            "langues_pays": []
        }

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
    
def mettre_a_jour_qualite_reseau(nom_reseau):
    """
    Met à jour la qualité du réseau en fonction du responsable et des agents
    """
    if nom_reseau not in RESEAUX:
        return False, "Réseau non trouvé"
    
    reseau = RESEAUX[nom_reseau]
    pays = reseau.get("pays", "")
    responsable = reseau.get("responsable")
    
    # Calculer la qualité de base selon l'agent de création
    qualite_base = reseau.get("bonus_qualite", 0)
    
    # Bonus/malus selon le responsable
    bonus_responsable = 0
    if responsable and pays:
        bonus_resp = calculer_bonus_langue_agent(responsable, pays)
        if bonus_resp['langues_maitrisees']:
            # Le responsable parle au moins une langue du pays
            if bonus_resp['bonus_qualite'] >= 25:
                bonus_responsable = 15  # +15% si le responsable parle la langue principale
            elif bonus_resp['bonus_qualite'] >= 15:
                bonus_responsable = 10  # +10% si le responsable parle 2+ langues
            else:
                bonus_responsable = 5   # +5% si le responsable parle 1 langue
        else:
            # Le responsable ne parle aucune langue du pays
            bonus_responsable = -10  # -10% de malus
    
    # Qualité finale
    qualite_finale = qualite_base + bonus_responsable
    
    # Déterminer le niveau de qualité
    if qualite_finale >= 35:
        niveau_qualite = "Excellente"
    elif qualite_finale >= 25:
        niveau_qualite = "Bonne"
    elif qualite_finale >= 15:
        niveau_qualite = "Améliorée"
    elif qualite_finale >= 5:
        niveau_qualite = "Standard"
    else:
        niveau_qualite = "Faible"
    
    # Mettre à jour le réseau
    reseau["qualite"] = niveau_qualite
    reseau["bonus_qualite"] = qualite_finale
    reseau["bonus_responsable"] = bonus_responsable
    
    # Ajouter un événement si la qualité a changé
    ancienne_qualite = reseau.get("qualite_precedente", "Standard")
    if ancienne_qualite != niveau_qualite:
        if bonus_responsable > 0:
            reseau["evenements"].append(f"Qualité du réseau améliorée à '{niveau_qualite}' grâce au responsable linguistiquement compétent")
        elif bonus_responsable < 0:
            reseau["evenements"].append(f"Qualité du réseau dégradée à '{niveau_qualite}' - le responsable ne parle pas les langues locales")
        else:
            reseau["evenements"].append(f"Qualité du réseau maintenue à '{niveau_qualite}'")
    
    reseau["qualite_precedente"] = niveau_qualite
    
    return True, f"Qualité mise à jour: {niveau_qualite} ({qualite_finale:+d}%)"

def definir_responsable(reseau, agent):
    if reseau in RESEAUX:
        RESEAUX[reseau]["responsable"] = agent
        
        # Mettre à jour la qualité du réseau
        mettre_a_jour_qualite_reseau(reseau)
        
        # Ajouter un événement
        ajouter_evenement(reseau, f"Responsable assigné: {agent.nom} {agent.prenom}")
        
        return True, "Responsable assigné et qualité mise à jour"
    return False, "Réseau non trouvé"

def supprimer_responsable(reseau):
    if reseau in RESEAUX:
        RESEAUX[reseau]["responsable"] = None

def ajouter_evenement(reseau, texte):
    if reseau in RESEAUX:
        RESEAUX[reseau]["evenements"].insert(0, texte)
        RESEAUX[reseau]["evenements"] = RESEAUX[reseau]["evenements"][:10]

def ajouter_reseau_avec_bonus(nom, pays, ville, agent_createur, lat=48.85, lon=2.35):
    """
    Crée un réseau avec des bonus de qualité basés sur les compétences linguistiques de l'agent créateur
    """
    # Calculer les bonus de langue
    bonus = calculer_bonus_langue_agent(agent_createur, pays)
    
    # Créer le réseau de base
    ajouter_reseau(nom, pays, ville, lat, lon)
    
    # Ajouter des informations supplémentaires basées sur les bonus
    if nom in RESEAUX:
        reseau = RESEAUX[nom]
        
        # Ajouter l'agent créateur comme premier membre
        reseau["agents"].append(agent_createur)
        
        # Ajouter des informations sur la qualité du réseau
        if bonus['bonus_qualite'] > 0:
            # Améliorer la qualité du réseau selon les bonus linguistiques
            qualite_base = "Standard"
            if bonus['bonus_qualite'] >= 25:
                qualite_base = "Excellente"
            elif bonus['bonus_qualite'] >= 15:
                qualite_base = "Bonne"
            elif bonus['bonus_qualite'] >= 10:
                qualite_base = "Améliorée"
            
            reseau["qualite"] = qualite_base
            reseau["bonus_qualite"] = bonus['bonus_qualite']
            
            # Ajouter des événements spéciaux selon la qualité
            if bonus['langues_maitrisees']:
                langues_communes = ', '.join(bonus['langues_maitrisees'])
                if bonus['bonus_qualite'] >= 25:
                    reseau["evenements"].append(f"Réseau créé avec une intégration locale excellente grâce à la maîtrise de {langues_communes}")
                elif bonus['bonus_qualite'] >= 15:
                    reseau["evenements"].append(f"Réseau créé avec une bonne intégration locale grâce à la maîtrise de {langues_communes}")
                else:
                    reseau["evenements"].append(f"Réseau créé avec une intégration locale améliorée grâce à la maîtrise de {langues_communes}")
        
        # Ajouter des informations sur l'agent créateur
        reseau["agent_creation"] = {
            "nom": f"{agent_createur.nom} {agent_createur.prenom}",
            "bureau": agent_createur.bureau,
            "langues": agent_createur.langues,
            "bonus_appliques": bonus
        }
        
        # Ajouter des informations sur la localisation
        reseau["localisation"] = {
            "pays": pays,
            "ville": ville,
            "coordonnees": {"lat": lat, "lon": lon},
            "langues_locales": bonus['langues_pays']
        }
        
        return True, f"Réseau créé avec succès. Qualité: {reseau.get('qualite', 'Standard')}"
    
    return False, "Erreur lors de la création du réseau"
