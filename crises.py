import random
from datetime import datetime, timedelta

NOMS_OPERATION = [
    "Aigle Noir", "Tempête Blanche", "Lynx Gris", "Phénix Rouge",
    "Opale", "Quasar", "Icebreaker", "Spectre", "Jade", "Mamba", "Sahara", "Bison", "Saturne"
]

# Nouvelles listes pour les origines et gravités
ORIGINES_POSSIBLES = [
    "Trafic d'armes", "Espionnage industriel", "Terrorisme", "Trafic de drogue",
    "Cyber-attaque", "Sabotage", "Trafic d'êtres humains", "Blanchiment d'argent",
    "Contrebande", "Extorsion", "Infiltration", "Manipulation d'opinion",
    "Vol de technologies", "Assassinat ciblé", "Déstabilisation politique"
]

GRAVITES_POSSIBLES = ["Faible", "Modérée", "Élevée", "Critique", "Maximale"]

def generer_nom_operation():
    return random.choice(NOMS_OPERATION) + "-" + str(random.randint(10, 99))

def generer_origine_crise():
    """Génère une origine aléatoire pour une crise"""
    return random.choice(ORIGINES_POSSIBLES)

def generer_gravite_crise():
    """Génère une gravité aléatoire pour une crise"""
    return random.choice(GRAVITES_POSSIBLES)

def generer_suspects_crise(pays, nb_suspects=1):
    """
    Génère des suspects en fonction du pays de la crise.
    Si le pays n'est pas dans la liste des noms, génère des noms aléatoires.
    """
    try:
        # Import local pour éviter les problèmes de dépendances circulaires
        from noms import generer_nom_prenom
        
        suspects = []
        for _ in range(nb_suspects):
            try:
                nom, prenom = generer_nom_prenom(pays)
                suspects.append(f"{prenom} {nom}")  # Format: "Prénom Nom"
            except:
                # Fallback si le pays n'existe pas dans noms.py
                suspects.append(f"Suspect {random.randint(1000, 9999)}")
        return suspects
    except ImportError:
        # Fallback si le module noms n'est pas disponible
        return [f"Suspect {random.randint(1000, 9999)}" for _ in range(nb_suspects)]

CRISES = []

class Crise:
    def __init__(self, nom=None, statut="En attente", origine=None, gravite=None, etapes=None, suspects=None, dossier=None, lat=48.85, lon=2.35, date_debut=None, date_fin=None, pays=None):
        self.nom = nom if nom else generer_nom_operation()
        self.statut = statut
        self.origine = origine if origine else generer_origine_crise()
        self.gravite = gravite if gravite else generer_gravite_crise()
        self.etapes = etapes or []
        self.suspects = suspects or []
        self.dossier = dossier or {}
        self.lat = lat
        self.lon = lon
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.pays = pays  # Nouveau : pays de la crise
        
        # Système d'avancement de la crise
        self.progression = 99  # Commence à 99% pour permettre la dégradation
        self.derniere_action_date = None  # Date de la dernière action
        self.actions_lancees = False  # Si au moins une action a été lancée
        
        # Génération automatique des suspects si aucun n'est fourni et qu'un pays est spécifié
        if not self.suspects and self.pays:
            nb_suspects = random.randint(1, 3)  # Entre 1 et 3 suspects
            self.suspects = generer_suspects_crise(self.pays, nb_suspects)
            
            # Créer automatiquement les dossiers suspects
            try:
                from dossiers_suspects import creer_dossier_suspect
                for suspect in self.suspects:
                    # Le format des suspects est "Prénom Nom"
                    if ' ' in suspect:
                        prenom, nom = suspect.split(' ', 1)
                    else:
                        prenom, nom = suspect, ''
                    creer_dossier_suspect(nom, prenom, self.pays, self.nom)
                    print(f"DEBUG: Dossier suspect créé pour {prenom} {nom} avec ID: {nom}_{prenom}_{self.nom}")
            except ImportError:
                pass  # Si le module n'est pas disponible, on continue sans

    def ajouter_etape(self, texte):
        self.etapes.append(texte)

    def ajouter_suspect(self, personne):
        self.suspects.append(personne)

    def clore(self, resultat):
        self.statut = "Clôturée"
        self.dossier["resultat"] = resultat

    def demarrer(self, now, duree_minutes):
        self.date_debut = now
        self.date_fin = now + timedelta(minutes=duree_minutes)
        # Le statut reste "En attente" jusqu'à ce qu'une action soit lancée
        print(f"DEBUG: Crise {self.nom} démarrée à {now}, fin prévue à {self.date_fin}")

    def maj_etat(self, now):
        # Vérifier si la crise atteint 100% (succès) en premier
        if self.progression >= 100 and self.statut == "En cours":
            self.statut = "Réussite"
            self.dossier["resultat"] = "Réussite - objectif atteint"
            
            # Appliquer bonus de réputation et d'argent
            try:
                import budget
                bonus_reputation, bonus_argent = self._calculer_bonus_reussite()
                budget.crediter(bonus_argent, f"Bonus argent - succès crise {self.nom}")
                budget.ajouter_reputation_service(bonus_reputation)
                print(f"INFO: Crise {self.nom} réussie! Bonus: +{bonus_reputation} réputation, +{bonus_argent}€ argent")
            except ImportError:
                pass
                
            # Nettoyer les dossiers suspects
            try:
                from dossiers_suspects import supprimer_dossiers_crise
                nb_dossiers_supprimes = supprimer_dossiers_crise(self.nom)
                if nb_dossiers_supprimes > 0:
                    print(f"INFO: {nb_dossiers_supprimes} dossier(s) suspect(s) supprimé(s) pour la crise {self.nom}")
            except ImportError:
                pass
            return
            
        # Vérifier si la crise atteint 0% (échec)
        if self.progression <= 0 and self.actions_lancees and self.statut == "En cours":
            self.statut = "Échec"
            self.dossier["resultat"] = "Échec - progression à 0%"
            print(f"INFO: Crise {self.nom} marquée comme échec (progression: {self.progression}%)")
            
            # Appliquer malus de réputation
            try:
                import budget
                malus_reputation = self._calculer_malus_reputation()
                budget.ajouter_reputation_service(-malus_reputation)
                print(f"INFO: Malus réputation appliqué: -{malus_reputation} réputation")
            except ImportError:
                pass
                
            # Nettoyer les dossiers suspects
            try:
                from dossiers_suspects import supprimer_dossiers_crise
                nb_dossiers_supprimes = supprimer_dossiers_crise(self.nom)
                if nb_dossiers_supprimes > 0:
                    print(f"INFO: {nb_dossiers_supprimes} dossier(s) suspect(s) supprimé(s) pour la crise {self.nom}")
            except ImportError:
                pass
            return
            
        # Vérifier si la crise doit être clôturée par le temps (DÉSACTIVÉ POUR TESTS)
        # if self.date_fin and now >= self.date_fin:
        #     if not self.actions_lancees:
        #         # Aucune action lancée : clôture automatique
        #         self.statut = "Clôturée"
        #         self.dossier["resultat"] = "Clôturée automatiquement par le temps"
        #         print(f"INFO: Crise {self.nom} clôturée automatiquement (aucune action)")
        #         
        #         # Nettoyer les dossiers suspects
        #         try:
        #             from dossiers_suspects import supprimer_dossiers_crise
        #             nb_dossiers_supprimes = supprimer_dossiers_crise(self.nom)
        #             if nb_dossiers_supprimes > 0:
        #                         print(f"INFO: {nb_dossiers_supprimes} dossier(s) suspect(s) supprimé(s) pour la crise {self.nom}")
        #         except ImportError:
        #             pass

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        c = Crise(
            d.get('nom'), d.get('statut', 'En cours'), d.get('origine'), d.get('gravite'),
            d.get('etapes', []), d.get('suspects', []), d.get('dossier', {}), d.get('lat', 48.85), d.get('lon', 2.35),
            d.get('date_debut', None), d.get('date_fin', None), d.get('pays')
        )
        return c

    def _calculer_taux_degradation_journaliere(self):
        """Calcule le taux de dégradation journalière selon la gravité"""
        taux_degradation = {
            "Faible": 4,
            "Modérée": 5,
            "Élevée": 8,
            "Critique": 10,
            "Maximale": 20
        }
        return taux_degradation.get(self.gravite, 2)
    
    def _calculer_bonus_reussite(self):
        """Calcule les bonus de réputation et d'argent pour une crise réussie"""
        bonus_base = {
            "Faible": {"reputation": 1000, "argent": 5000},
            "Modérée": {"reputation": 2000, "argent": 10000},
            "Élevée": {"reputation": 4000, "argent": 20000},
            "Critique": {"reputation": 8000, "argent": 40000},
            "Maximale": {"reputation": 15000, "argent": 75000}
        }
        
        bonus = bonus_base.get(self.gravite, {"reputation": 2000, "argent": 10000})
        return bonus["reputation"], bonus["argent"]
    
    def _calculer_malus_reputation(self):
        """Calcule le malus de réputation pour une crise échouée"""
        malus_base = {
            "Faible": 500,
            "Modérée": 1000,
            "Élevée": 2000,
            "Critique": 4000,
            "Maximale": 8000
        }
        return malus_base.get(self.gravite, 1000)
    
    def appliquer_degradation_naturelle(self, current_time):
        """Applique la dégradation naturelle de la crise (appelée quotidiennement)"""
        if self.statut != "En cours":
            return
            
        # Si aucune action n'a été lancée, utiliser la date de début de la crise
        date_reference = self.derniere_action_date if self.derniere_action_date else self.date_debut
        
        if date_reference:
            jours_ecoules = (current_time - date_reference).days
            if jours_ecoules > 0:
                taux = self._calculer_taux_degradation_journaliere()
                degradation = jours_ecoules * taux
                self.progression = max(0, self.progression - degradation)
                
                print(f"DEBUG: Crise {self.nom} - Dégradation: {degradation}% (taux: {taux}%/jour, jours: {jours_ecoules})")
                
                if self.progression <= 0:
                    print(f"INFO: Crise {self.nom} atteint 0% de progression")
    
    def action_lancee(self, current_time):
        """Marque qu'une action a été lancée sur cette crise"""
        self.actions_lancees = True
        self.derniere_action_date = current_time
        
        # Changer le statut à "En cours" quand la première action est lancée
        if self.statut == "En attente":
            self.statut = "En cours"
            print(f"INFO: Crise {self.nom} passe en statut 'En cours'")
        
        # Réduire la progression de 1% quand une action est lancée
        self.progression = max(0, self.progression - 1)
        print(f"INFO: Action lancée sur crise {self.nom}, progression: {self.progression}%")
    
    def appliquer_resultat_action(self, impact_action):
        """Applique le résultat d'une action sur la progression de la crise"""
        if self.statut != "En cours":
            return
            
        ancienne_progression = self.progression
        self.progression = max(0, min(100, self.progression + impact_action))
        
        print(f"INFO: Crise {self.nom} - Progression: {ancienne_progression}% → {self.progression}% (impact: {impact_action:+d}%)")
        
        # Mettre à jour la date de la dernière action
        from datetime import datetime
        self.derniere_action_date = datetime.now()

def ajouter_crise(crise):
    CRISES.append(crise)

def supprimer_crise(idx):
    if 0 <= idx < len(CRISES):
        CRISES.pop(idx)

def modifier_crise(idx, **kwargs):
    if 0 <= idx < len(CRISES):
        crise = CRISES[idx]
        for k, v in kwargs.items():
            setattr(crise, k, v)

def lister_crises(etat=None):
    return [c for c in CRISES if (etat is None or c.statut == etat)]

def get_crises():
    return CRISES
