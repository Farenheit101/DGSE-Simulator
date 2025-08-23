# gestionnaire_actions.py

import random
from datetime import datetime, timedelta
from actions_crises import ActionCrise, TypeAction, StatutAction, creer_action, verifier_prerequis
import dossiers_suspects
import budget

class GestionnaireActions:
    def __init__(self):
        self.actions_en_cours = {}  # id_action -> ActionCrise
        self.actions_terminees = {}  # id_action -> ActionCrise
        self.historique_actions = []
        
    def _verifier_bonus_reseau(self, agent_nom, pays_crise):
        """
        Vérifie si un agent est rattaché à un réseau dans le pays de la crise
        Retourne le nom du réseau et le bonus appliqué
        """
        try:
            from reseaux import RESEAUX
            from agents import get_agent_by_nom
            
            # Extraire nom et prénom de l'agent
            if ' ' in agent_nom:
                nom, prenom = agent_nom.split(' ', 1)
            else:
                nom, prenom = agent_nom, ""
            
            agent = get_agent_by_nom(nom, prenom)
            if not agent:
                return None, 0
            
            # Chercher dans tous les réseaux
            for nom_reseau, reseau in RESEAUX.items():
                if reseau["pays"].lower() == pays_crise.lower():
                    # Vérifier si l'agent est dans ce réseau
                    if agent in reseau["agents"]:
                        return nom_reseau, 15  # Bonus de 15% pour les actions réussies
                    # Vérifier si l'agent est le responsable du réseau
                    elif reseau["responsable"] == agent:
                        return nom_reseau, 20  # Bonus de 20% si l'agent est responsable
            
            return None, 0
            
        except ImportError:
            return None, 0
    
    def lancer_action(self, type_action, crise_id, agent_nom, cible=None, equipements=None, current_game_time=None):
        """Lance une nouvelle action sur une crise"""
        # Créer l'action
        action, message = creer_action(type_action, crise_id, agent_nom, cible)
        if not action:
            return False, message
        
        # Vérifier les prérequis
        from agents import get_agent_by_nom
        # Extraire nom et prénom de l'agent
        if ' ' in agent_nom:
            nom, prenom = agent_nom.split(' ', 1)
        else:
            nom, prenom = agent_nom, ""
        
        agent = get_agent_by_nom(nom, prenom)
        prerequis_ok, message_prerequis = verifier_prerequis(action, agent, equipements)
        if not prerequis_ok:
            return False, f"Prérequis non satisfaits: {message_prerequis}"
        
        # Vérifier le budget
        if not budget.debiter(action.cout, f"Action {action.type_action.value} sur crise {crise_id}"):
            return False, f"Budget insuffisant. Coût: {action.cout}€"
        
        # Appliquer un bonus de vitesse si l'agent possède des compétences requises
        try:
            competences_requises = [p for p in action.prerequis if p.startswith("competence_")]
            if competences_requises:
                comps_agent = [c.lower() for c in getattr(agent, 'competences', [])]
                def _match(pr):
                    key = pr.replace("competence_", "")
                    if key == "infiltration":
                        return "infiltration" in comps_agent
                    if key == "combat":
                        return any(x in comps_agent for x in ["combat rapproché", "combat"])
                    if key == "hacking":
                        return "hacking" in comps_agent
                    if key == "negociation":
                        return "négociation" in comps_agent or "negociation" in comps_agent
                    if key == "technique":
                        return any(x in comps_agent for x in ["hacking", "crypto", "infiltration", "technique"])
                    if key == "analyse":
                        return "analyse" in comps_agent
                    if key == "securite":
                        return "sécurité" in comps_agent or "securité" in comps_agent or "securite" in comps_agent
                    if key == "recherche":
                        return "recherche" in comps_agent
                    if key == "gestion":
                        return "gestion" in comps_agent
                    if key == "surveillance":
                        return "surveillance" in comps_agent
                    return key in comps_agent
                
                nb_ok = sum(1 for pr in competences_requises if _match(pr))
                
                # Bonus de vitesse progressif selon le nombre de compétences
                if nb_ok >= 1:  # Au moins 1 compétence requise (prérequis de base)
                    if nb_ok == 1:
                        # 1 compétence : bonus de 2%
                        reduction = 0.02
                        print(f"INFO: Agent {agent_nom} - 1 compétence requise, bonus vitesse: +2%")
                    elif nb_ok == 2:
                        # 2 compétences : bonus de 5%
                        reduction = 0.05
                        print(f"INFO: Agent {agent_nom} - 2 compétences requises, bonus vitesse: +5%")
                    elif nb_ok >= 3:
                        # 3+ compétences : bonus de 8%
                        reduction = 0.08
                        print(f"INFO: Agent {agent_nom} - {nb_ok} compétences requises, bonus vitesse: +8%")
                    
                    # Appliquer la réduction de durée
                    nouvelle_duree = max(1, int(round(action.duree_minutes * (1 - reduction))))
                    action.duree_minutes = nouvelle_duree
                    
        except Exception:
            # Ne pas bloquer en cas d'erreur, simplement ignorer le bonus
            pass

        # Utiliser le temps de jeu fourni ou fallback au temps réel
        if current_game_time is None:
            current_game_time = datetime.now()
        
        success, message_demarrage = action.demarrer(agent_nom, current_game_time)
        if not success:
            # Rembourser si échec
            budget.crediter(action.cout, f"Remboursement action échouée")
            return False, message_demarrage
        
        # Marquer qu'une action a été lancée sur la crise
        try:
            from crises import CRISES
            for crise in CRISES:
                if crise.nom == crise_id:
                    crise.action_lancee(current_game_time)
                    break
        except ImportError:
            pass
        
        # Mettre l'agent en mission
        try:
            from agents import get_agent_by_nom
            if ' ' in agent_nom:
                nom, prenom = agent_nom.split(' ', 1)
            else:
                nom, prenom = agent_nom, ""
            
            agent = get_agent_by_nom(nom, prenom)
            if agent:
                agent.mettre_en_mission(f"Action {type_action.value} sur crise {crise_id}")
        except ImportError:
            pass
        
        # Enregistrer l'action
        self.actions_en_cours[action.id] = action
        
        # Ajouter à l'historique
        self.historique_actions.append({
            "action_id": action.id,
            "type": action.type_action.value,
            "crise_id": crise_id,
            "agent_id": agent_nom,
            "date_lancement": current_game_time,
            "cout": action.cout
        })
        
        return True, f"Action {action.type_action.value} lancée. Coût: {action.cout}€, Durée: {action.duree_minutes} minutes"
    
    def avancer_actions(self, current_time):
        """Fait avancer toutes les actions en cours"""
        actions_terminees = []
        
        for action_id, action in self.actions_en_cours.items():
            if action.statut != StatutAction.EN_COURS:
                continue
            
            # Calculer la progression basée sur le temps écoulé
            if action.date_debut and action.date_fin:
                temps_ecoule = current_time - action.date_debut
                temps_total = action.date_fin - action.date_debut
                
                if temps_ecoule >= temps_total:
                    # Action terminée par le temps - déterminer succès ou échec
                    if random.random() < 0.7:  # 70% de chance de succès
                        self._finaliser_action(action, "Succès")
                    else:
                        self._finaliser_action(action, "Échec")
                    actions_terminees.append(action_id)
                else:
                    # Calculer la progression (0% au début, 100% à la fin)
                    progression = min(100, int((temps_ecoule.total_seconds() / temps_total.total_seconds()) * 100))
                    action.progression = progression
                    
                    # Debug
                    print(f"DEBUG: Action {action.id} ({action.type_action.value}) - Temps écoulé: {temps_ecoule}, Temps total: {temps_total}, Progression: {progression}%")
                    
                    # Ajouter des étapes automatiques
                    if progression >= 25 and len(action.etapes) == 0:
                        action.etapes.append({
                            "description": "Phase initiale terminée",
                            "date": current_time,
                            "progression": progression
                        })
                    elif progression >= 50 and len(action.etapes) == 1:
                        action.etapes.append({
                            "description": "Phase intermédiaire en cours",
                            "date": current_time,
                            "progression": progression
                        })
                    elif progression >= 75 and len(action.etapes) == 2:
                        action.etapes.append({
                            "description": "Phase finale en cours",
                            "date": current_time,
                            "progression": progression
                        })
        
        # Retirer les actions terminées
        for action_id in actions_terminees:
            action = self.actions_en_cours.pop(action_id)
            self.actions_terminees[action_id] = action
            
            # Remettre l'agent disponible
            try:
                from agents import get_agent_by_nom
                if action.agent_id and ' ' in action.agent_id:
                    nom, prenom = action.agent_id.split(' ', 1)
                    agent = get_agent_by_nom(nom, prenom)
                    if agent:
                        agent.terminer_mission()
            except ImportError:
                pass
    
    def _finaliser_action(self, action, resultat="Succès"):
        """Finalise une action avec un résultat"""
        # Simuler des informations recueillies selon le type d'action
        informations = self._generer_informations_action(action)
        
        # Terminer l'action selon le résultat
        if resultat == "Succès":
            action.terminer("Succès", informations)
            
            # Bonus de réputation pour action réussie
            try:
                import budget
                bonus_reputation = self._calculer_bonus_reputation_action(action)
                budget.ajouter_reputation_service(bonus_reputation)
                print(f"INFO: Action {action.type_action.value} réussie! Bonus réputation: +{bonus_reputation}")
            except ImportError:
                pass
        else:
            action.echouer("Échec de l'opération")
            
            # Malus de réputation pour action échouée
            try:
                import budget
                malus_reputation = self._calculer_malus_reputation_action(action)
                budget.ajouter_reputation_service(-malus_reputation)
                print(f"INFO: Action {action.type_action.value} échouée! Malus réputation: -{malus_reputation}")
            except ImportError:
                pass
        
        # Calculer l'impact de l'action sur la crise
        impact_crise = self._calculer_impact_action_crise(action)
        
        # Appliquer l'impact sur la crise
        try:
            from crises import CRISES
            for crise in CRISES:
                if crise.nom == action.crise_id:
                    crise.appliquer_resultat_action(impact_crise)
                    break
        except ImportError:
            pass
        
        # Mettre à jour les dossiers suspects si une cible est spécifiée
        if action.cible and action.informations_recueillies:
            self._mettre_a_jour_dossiers_suspects(action)
    
    def _generer_informations_action(self, action):
        """Génère des informations réalistes selon le type d'action"""
        informations = []
        
        if action.type_action == TypeAction.SURVEILLANCE:
            informations.extend([
                "Mouvements du suspect documentés",
                "Contacts identifiés et photographiés",
                "Horaires de routine établis",
                "Lieux fréquentés cartographiés"
            ])
        
        elif action.type_action == TypeAction.INFILTRATION:
            informations.extend([
                "Accès aux locaux obtenu",
                "Documents sensibles récupérés",
                "Écoutes placées dans les zones clés",
                "Structure organisationnelle révélée"
            ])
        
        elif action.type_action == TypeAction.INTERCEPTION:
            informations.extend([
                "Communications téléphoniques interceptées",
                "Emails et messages récupérés",
                "Contacts et réseaux identifiés",
                "Plans et intentions révélés"
            ])
        
        elif action.type_action == TypeAction.ARRESTATION:
            informations.extend([
                "Suspect appréhendé sans incident",
                "Équipements et documents saisis",
                "Interrogatoire initial effectué",
                "Transfert vers centre de détention"
            ])
        
        elif action.type_action == TypeAction.NEUTRALISATION:
            informations.extend([
                "Menace éliminée avec succès",
                "Équipements ennemis récupérés",
                "Zone sécurisée",
                "Pas de victimes collatérales"
            ])
        
        elif action.type_action == TypeAction.RECUPERATION:
            informations.extend([
                "Informations sensibles récupérées",
                "Preuves matérielles collectées",
                "Documents compromettants saisis",
                "Données numériques extraites"
            ])
        
        elif action.type_action == TypeAction.SABOTAGE:
            informations.extend([
                "Équipements ciblés neutralisés",
                "Capacités opérationnelles réduites",
                "Délais imposés à l'adversaire",
                "Dommages contrôlés et ciblés"
            ])
        
        elif action.type_action == TypeAction.INFILTRATION_NUMERIQUE:
            informations.extend([
                "Accès aux systèmes obtenu",
                "Données sensibles extraites",
                "Surveillance continue établie",
                "Backdoors placées pour accès futur"
            ])
        
        # SOURCE_HUMAINE supprimée - action non disponible
        
        elif action.type_action == TypeAction.ANALYSE_FORENSIQUE:
            informations.extend([
                "Analyse des preuves terminée",
                "Traces et indices identifiés",
                "Rapport détaillé produit",
                "Preuves exploitables documentées"
            ])
        
        elif action.type_action == TypeAction.SURVEILLANCE_ELECTRONIQUE:
            informations.extend([
                "Communications interceptées",
                "Données techniques collectées",
                "Réseaux et infrastructures cartographiés",
                "Capacités techniques évaluées"
            ])
        
        elif action.type_action == TypeAction.OPERATION_COVERTE:
            informations.extend([
                "Objectif principal atteint",
                "Informations critiques récupérées",
                "Opération menée sans compromission",
                "Réseau d'agents établi"
            ])
        
        # Ajouter des informations aléatoires pour la variété
        if random.random() < 0.3:
            informations.append("Informations supplémentaires découvertes par hasard")
        
        return informations
    
    def _mettre_a_jour_dossiers_suspects(self, action):
        """Met à jour les dossiers suspects avec les informations recueillies"""
        try:
            # Rechercher le dossier suspect de la cible
            if action.cible:
                # Extraire nom et prénom de la cible (format: "Prénom Nom")
                if ' ' in action.cible:
                    prenom, nom = action.cible.split(' ', 1)
                else:
                    prenom, nom = action.cible, ""
                
                # Rechercher le dossier suspect
                dossier = dossiers_suspects.get_dossier_suspect(f"{nom}_{prenom}_{action.crise_id}")
                
                if dossier and action.resultat == "Succès":
                    # Ajouter les informations recueillies
                    for info in action.informations_recueillies:
                        dossier.ajouter_information(
                            info, 
                            type_info=action.type_action.value,
                            source=f"Action {action.id}"
                        )
                    
                    # Ajouter une note sur l'action
                    dossier.ajouter_note(
                        f"Action {action.type_action.value} terminée avec succès. "
                        f"Résultat: {action.resultat}",
                        source="Gestionnaire d'actions"
                    )
                    
                    # Remplir automatiquement les informations selon le type d'action
                    self._remplir_informations_suspect(dossier, action.type_action)
        except Exception as e:
            print(f"Erreur lors de la mise à jour des dossiers suspects: {e}")
    
    def _remplir_informations_suspect(self, dossier, type_action):
        """Remplit automatiquement les informations du suspect selon le type d'action réussie"""
        try:
            from actions_crises import TypeAction
            
            if type_action == TypeAction.SURVEILLANCE:
                # Surveillance réussie : remplir l'adresse
                if not dossier.adresse or dossier.adresse == "Adresse inconnue":
                    # Générer une adresse réaliste
                    adresse = self._generer_adresse_realiste(dossier.pays)
                    dossier.adresse = adresse
                    dossier.ajouter_note(f"Adresse découverte par surveillance: {adresse}", "Système")
                    print(f"INFO: Adresse du suspect {dossier.nom} {dossier.prenom} mise à jour: {adresse}")
            
            elif type_action in [TypeAction.RECUPERATION, TypeAction.INFILTRATION_NUMERIQUE, TypeAction.SURVEILLANCE_ELECTRONIQUE]:
                # Actions de collecte d'informations : remplir aléatoirement 1 à 3 champs vides
                champs_a_remplir = []
                
                # Vérifier quels champs sont vides
                if not dossier.email or dossier.email == "Email inconnu":
                    champs_a_remplir.append("email")
                if not dossier.adresse or dossier.adresse == "Adresse inconnue":
                    champs_a_remplir.append("adresse")
                if not dossier.telephone or dossier.telephone == "Téléphone inconnu":
                    champs_a_remplir.append("telephone")
                
                if champs_a_remplir:
                    # Choisir aléatoirement 1 à 3 champs à remplir
                    nb_champs = min(len(champs_a_remplir), random.randint(1, 3))
                    champs_choisis = random.sample(champs_a_remplir, nb_champs)
                    
                    for champ in champs_choisis:
                        if champ == "email":
                            email = self._generer_email_realiste(dossier.nom, dossier.prenom)
                            dossier.email = email
                            dossier.ajouter_note(f"Email découvert: {email}", "Système")
                            print(f"INFO: Email du suspect {dossier.nom} {dossier.prenom} mis à jour: {email}")
                        
                        elif champ == "adresse":
                            adresse = self._generer_adresse_realiste(dossier.pays)
                            dossier.adresse = adresse
                            dossier.ajouter_note(f"Adresse découverte: {adresse}", "Système")
                            print(f"INFO: Adresse du suspect {dossier.nom} {dossier.prenom} mise à jour: {adresse}")
                        
                        elif champ == "telephone":
                            telephone = self._generer_telephone_realiste(dossier.pays)
                            dossier.telephone = telephone
                            dossier.ajouter_note(f"Téléphone découvert: {telephone}", "Système")
                            print(f"INFO: Téléphone du suspect {dossier.nom} {dossier.prenom} mis à jour: {telephone}")
                    
                    # Mettre à jour la date de dernière modification
                    from datetime import datetime
                    dossier.derniere_mise_a_jour = datetime.now()
                    
        except Exception as e:
            print(f"Erreur lors du remplissage des informations suspect: {e}")
    
    def _generer_adresse_realiste(self, pays):
        """Génère une adresse réaliste selon le pays"""
        adresses_par_pays = {
            "France": [
                "123 Rue de la Paix, 75001 Paris",
                "45 Avenue des Champs-Élysées, 75008 Paris",
                "78 Boulevard Saint-Germain, 75006 Paris",
                "15 Place de la Concorde, 75001 Paris",
                "67 Rue du Faubourg Saint-Honoré, 75008 Paris"
            ],
            "États-Unis": [
                "123 Main Street, New York, NY 10001",
                "456 Broadway Avenue, Los Angeles, CA 90210",
                "789 Oak Drive, Chicago, IL 60601",
                "321 Pine Street, Miami, FL 33101",
                "654 Elm Road, Boston, MA 02101"
            ],
            "Espagne": [
                "Calle Mayor 123, 28013 Madrid",
                "Avenida Diagonal 456, 08013 Barcelona",
                "Plaza Mayor 78, 28012 Madrid",
                "Calle Gran Vía 321, 28013 Madrid",
                "Paseo de la Castellana 654, 28046 Madrid"
            ],
            "Allemagne": [
                "Hauptstraße 123, 10115 Berlin",
                "Unter den Linden 456, 10117 Berlin",
                "Kurfürstendamm 78, 10719 Berlin",
                "Friedrichstraße 321, 10117 Berlin",
                "Potsdamer Platz 654, 10117 Berlin"
            ]
        }
        
        # Adresse par défaut si le pays n'est pas dans la liste
        adresses_defaut = [
            "123 Main Street, Capital City",
            "456 Central Avenue, Major Town",
            "789 Primary Road, Important City"
        ]
        
        adresses = adresses_par_pays.get(pays, adresses_defaut)
        return random.choice(adresses)
    
    def _generer_email_realiste(self, nom, prenom):
        """Génère un email réaliste basé sur le nom et prénom"""
        domaines = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com"]
        nom_clean = nom.lower().replace(" ", "").replace("-", "").replace("'", "")
        prenom_clean = prenom.lower().replace(" ", "").replace("-", "").replace("'", "")
        
        formats = [
            f"{prenom_clean}.{nom_clean}@{random.choice(domaines)}",
            f"{prenom_clean}{nom_clean}@{random.choice(domaines)}",
            f"{nom_clean}.{prenom_clean}@{random.choice(domaines)}",
            f"{prenom_clean[0]}{nom_clean}@{random.choice(domaines)}"
        ]
        
        return random.choice(formats)
    
    def _generer_telephone_realiste(self, pays):
        """Génère un numéro de téléphone réaliste selon le pays"""
        formats_par_pays = {
            "France": [
                "+33 1 42 12 34 56",
                "+33 1 45 67 89 01",
                "+33 1 48 23 45 67",
                "+33 1 53 45 67 89",
                "+33 1 56 78 90 12"
            ],
            "États-Unis": [
                "+1 (212) 555-0123",
                "+1 (213) 555-0456",
                "+1 (312) 555-0789",
                "+1 (305) 555-0123",
                "+1 (617) 555-0456"
            ],
            "Espagne": [
                "+34 91 123 45 67",
                "+34 93 234 56 78",
                "+34 91 345 67 89",
                "+34 91 456 78 90",
                "+34 91 567 89 01"
            ],
            "Allemagne": [
                "+49 30 123 45 67",
                "+49 30 234 56 78",
                "+49 30 345 67 89",
                "+49 30 456 78 90",
                "+49 30 567 89 01"
            ]
        }
        
        # Format par défaut si le pays n'est pas dans la liste
        formats_defaut = [
            "+1 234 567 8901",
            "+12 345 678 9012",
            "+123 456 789 0123"
        ]
        
        formats = formats_par_pays.get(pays, formats_defaut)
        return random.choice(formats)
    
    def lister_actions_crise(self, crise_id):
        """Liste toutes les actions d'une crise"""
        actions_crise = []
        
        # Actions en cours
        for action in self.actions_en_cours.values():
            if action.crise_id == crise_id:
                actions_crise.append(action)
        
        # Actions terminées
        for action in self.actions_terminees.values():
            if action.crise_id == crise_id:
                actions_crise.append(action)
        
        return actions_crise
    
    def lister_actions_agent(self, agent_id):
        """Liste toutes les actions d'un agent"""
        actions_agent = []
        
        # Actions en cours
        for action in self.actions_en_cours.values():
            if action.agent_id == agent_id:
                actions_agent.append(action)
        
        # Actions terminées
        for action in self.actions_terminees.values():
            if action.agent_id == agent_id:
                actions_agent.append(action)
        
        return actions_agent
    
    def obtenir_statistiques_crise(self, crise_id):
        """Obtient des statistiques sur les actions d'une crise"""
        actions = self.lister_actions_crise(crise_id)
        
        stats = {
            "total_actions": len(actions),
            "actions_en_cours": len([a for a in actions if a.statut == StatutAction.EN_COURS]),
            "actions_terminees": len([a for a in actions if a.statut == StatutAction.TERMINEE]),
            "actions_echouees": len([a for a in actions if a.statut == StatutAction.ECHEC]),
            "cout_total": sum(a.cout for a in actions),
            "impact_total": sum(a.impact_crise for a in actions if hasattr(a, 'impact_crise')),
            "types_actions": {}
        }
        
        # Compter par type d'action
        for action in actions:
            type_str = action.type_action.value
            if type_str not in stats["types_actions"]:
                stats["types_actions"][type_str] = 0
            stats["types_actions"][type_str] += 1
        
        return stats
    
    def annuler_action(self, action_id, raison="Annulation demandée"):
        """Annule une action en cours"""
        if action_id not in self.actions_en_cours:
            return False, "Action non trouvée ou déjà terminée"
        
        action = self.actions_en_cours[action_id]
        
        # Rembourser partiellement le coût
        remboursement = int(action.cout * 0.3)  # 30% de remboursement
        budget.crediter(remboursement, f"Remboursement action annulée {action_id}")
        
        # Annuler l'action
        action.annuler(raison)
        
        # Déplacer vers les actions terminées
        self.actions_terminees[action_id] = action
        del self.actions_en_cours[action_id]
        
        return True, f"Action annulée. Remboursement: {remboursement}€"
    
    def obtenir_actions_urgentes(self):
        """Obtient les actions qui nécessitent une attention immédiate"""
        actions_urgentes = []
        current_time = datetime.now()
        
        for action in self.actions_en_cours.values():
            if action.statut == StatutAction.EN_COURS:
                # Vérifier si l'action est en difficulté
                if action.progression < 25 and action.date_debut:
                    temps_ecoule = current_time - action.date_debut
                    temps_attendu = timedelta(minutes=action.duree_minutes * 0.25)
                    
                    if temps_ecoule > temps_attendu:
                        actions_urgentes.append({
                            "action": action,
                            "raison": "Progression lente",
                            "urgence": "Élevée"
                        })
                
                # Vérifier si l'action est proche de la fin
                if action.date_fin and (action.date_fin - current_time).total_seconds() < 1800:  # 30 minutes
                    actions_urgentes.append({
                        "action": action,
                        "raison": "Fin imminente",
                        "urgence": "Modérée"
                    })
        
        return actions_urgentes
    
    def _calculer_impact_action_crise(self, action):
        """Calcule l'impact d'une action sur la progression de la crise"""
        # Récupérer le pays de la crise pour vérifier le bonus réseau
        pays_crise = None
        try:
            from crises import CRISES
            for crise in CRISES:
                if crise.nom == action.crise_id:
                    pays_crise = crise.pays
                    break
        except ImportError:
            pass
        
        # Vérifier le bonus de réseau
        nom_reseau, bonus_reseau = self._verifier_bonus_reseau(action.agent_id, pays_crise)
        
        if action.resultat == "Succès":
            # Impact positif basé sur le coût de l'action
            if action.cout <= 10000:
                impact_base = random.randint(5, 15)      # Actions bon marché : 5-15%
            elif action.cout <= 25000:
                impact_base = random.randint(15, 30)     # Actions moyennes : 15-30%
            else:
                impact_base = random.randint(30, 50)     # Actions coûteuses : 30-50%
            
            # Appliquer le bonus de réseau
            if bonus_reseau > 0:
                impact_final = impact_base + bonus_reseau
                print(f"INFO: Bonus réseau appliqué! Agent rattaché au réseau '{nom_reseau}' dans {pays_crise}. Impact: {impact_base}% + {bonus_reseau}% = {impact_final}%")
                return impact_final
            else:
                return impact_base
        else:
            # Impact négatif basé sur le coût de l'action
            if action.cout <= 10000:
                return -random.randint(2, 10)     # Actions bon marché : -2 à -10%
            elif action.cout <= 25000:
                return -random.randint(10, 25)    # Actions moyennes : -10 à -25%
            else:
                return -random.randint(25, 40)    # Actions coûteuses : -25 à -40%

    def _calculer_bonus_reputation_action(self, action):
        """Calcule le bonus de réputation pour une action réussie"""
        # Bonus basé sur le coût et le type d'action
        bonus_base = {
            TypeAction.SURVEILLANCE: 50,
            TypeAction.INFILTRATION: 150,
            TypeAction.INTERCEPTION: 100,
            TypeAction.ARRESTATION: 200,
            TypeAction.NEUTRALISATION: 250,
            TypeAction.RECUPERATION: 120,
            TypeAction.SABOTAGE: 180,
            TypeAction.INFILTRATION_NUMERIQUE: 130,
            TypeAction.ANALYSE_FORENSIQUE: 80,
            TypeAction.SURVEILLANCE_ELECTRONIQUE: 90,
            TypeAction.OPERATION_COVERTE: 300
        }
        
        bonus = bonus_base.get(action.type_action, 100)
        
        # Modificateur selon le coût
        if action.cout <= 10000:
            bonus = int(bonus * 0.8)  # Actions bon marché
        elif action.cout >= 35000:
            bonus = int(bonus * 1.2)  # Actions coûteuses
        
        return max(10, bonus)  # Minimum 10 points
    
    def _calculer_malus_reputation_action(self, action):
        """Calcule le malus de réputation pour une action échouée"""
        # Malus basé sur le coût et le type d'action
        malus_base = {
            TypeAction.SURVEILLANCE: 25,
            TypeAction.INFILTRATION: 75,
            TypeAction.INTERCEPTION: 50,
            TypeAction.ARRESTATION: 100,
            TypeAction.NEUTRALISATION: 125,
            TypeAction.RECUPERATION: 60,
            TypeAction.SABOTAGE: 90,
            TypeAction.INFILTRATION_NUMERIQUE: 65,
            TypeAction.ANALYSE_FORENSIQUE: 40,
            TypeAction.SURVEILLANCE_ELECTRONIQUE: 45,
            TypeAction.OPERATION_COVERTE: 150
        }
        
        malus = malus_base.get(action.type_action, 50)
        
        # Modificateur selon le coût
        if action.cout <= 10000:
            malus = int(malus * 0.8)  # Actions bon marché
        elif action.cout >= 35000:
            malus = int(malus * 1.2)  # Actions coûteuses
        
        return max(5, malus)  # Minimum 5 points

    def obtenir_bonus_reseau_agent(self, agent_nom, pays_cible):
        """
        Fonction publique pour obtenir les informations de bonus réseau d'un agent
        Retourne un dictionnaire avec les détails du bonus
        """
        nom_reseau, bonus = self._verifier_bonus_reseau(agent_nom, pays_cible)
        
        if bonus > 0:
            return {
                "reseau": nom_reseau,
                "bonus": bonus,
                "description": f"Agent rattaché au réseau '{nom_reseau}' dans {pays_cible}",
                "type": "responsable" if bonus == 20 else "membre"
            }
        else:
            return {
                "reseau": None,
                "bonus": 0,
                "description": f"Aucun réseau dans {pays_cible}",
                "type": "aucun"
            }
    
    def lister_agents_avec_bonus_reseau(self, pays_cible):
        """
        Liste tous les agents avec leurs bonus réseau pour un pays donné
        Utile pour l'interface utilisateur
        """
        try:
            from agents import AGENTS
            from reseaux import RESEAUX
            
            agents_bonus = []
            
            for agent in AGENTS:
                bonus_info = self.obtenir_bonus_reseau_agent(f"{agent.nom} {agent.prenom}", pays_cible)
                agents_bonus.append({
                    "agent": agent,
                    "bonus_info": bonus_info
                })
            
            # Trier par bonus décroissant
            agents_bonus.sort(key=lambda x: x["bonus_info"]["bonus"], reverse=True)
            return agents_bonus
            
        except ImportError:
            return []

# Instance globale du gestionnaire
gestionnaire_actions = GestionnaireActions()
