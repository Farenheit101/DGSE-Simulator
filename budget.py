# budget.py

SOLDE = 200000  # Solde de départ (modulable)
HISTORIQUE = []

# --- Nouveau système de budget (activé par défaut) ---
NEW_BUDGET_ENABLED = True  # Active le nouveau modèle

# Montants fixes pour le recrutement d'agents (nouveau système)
RECRUIT_COST_ALEA = 2000
RECRUIT_COST_CIBLE = 5000

# Dépenses planifiées (futures fonctionnalités)
PLANNED_EXPENSES = []  # {"nom": str, "montant": int, "categorie": str, "date": datetime}

# Suivi rente mensuelle
_DERNIERE_RENTE_MOIS = None  # (année, mois) du dernier crédit de rente

def is_new_budget_enabled():
    return NEW_BUDGET_ENABLED

def solde():
    return SOLDE

def debiter(montant, motif=""):
    global SOLDE
    if SOLDE < montant:
        return False
    SOLDE -= montant
    HISTORIQUE.append((motif, -montant))
    return True

def crediter(montant, motif=""):
    global SOLDE
    SOLDE += montant
    HISTORIQUE.append((motif, montant))
    return True

# -------- Anciennes fonctions de coûts (compat legacy) --------
def cout_recrutement(bureau, legende=False, recherche_bdl=False):
    base = 15000 if bureau == "BDL" else 10000
    if legende: base += 20000
    if recherche_bdl: base += 10000
    return base

def cout_legende_temporaire(pays):
    pays_risque = ["Iran", "Chine", "Russie"]
    return 12000 if pays in pays_risque else 7000

def cout_recrutement_source():
    return 5000

def cout_reseau_clandestin(pays):
    pays_risque = ["Iran", "Chine", "Russie"]
    return 25000 if pays in pays_risque else 15000

def historique():
    return list(HISTORIQUE)

# -------- Nouveau modèle: API (inactif si flag = False) --------
def cout_recrutement_mode(type_recrutement):
    t = (type_recrutement or "").lower()
    if t == "classique":
        return RECRUIT_COST_ALEA
    if t == "cible":
        return RECRUIT_COST_CIBLE
    # Par défaut, considérer aléatoire si inconnu
    return RECRUIT_COST_ALEA

# Variable globale pour la réputation
REPUTATION_SERVICE = 50  # Réputation entre 0 et 100

def get_reputation_service():
    """Retourne la réputation actuelle du service"""
    return REPUTATION_SERVICE

def modifier_reputation_service(nouvelle_reputation):
    """Modifie la réputation du service (entre 0 et 100)"""
    global REPUTATION_SERVICE
    REPUTATION_SERVICE = max(0, min(100, nouvelle_reputation))
    return REPUTATION_SERVICE

def ajouter_reputation_service(points):
    """Ajoute des points de réputation"""
    global REPUTATION_SERVICE
    REPUTATION_SERVICE = max(0, min(100, REPUTATION_SERVICE + points))
    return REPUTATION_SERVICE

def calculer_rente_journaliere(reputation):
    # Formule simple et modulable
    # Exemple: base 1000€ + 30€ par point de réputation
    return 1000 + int(30 * max(0, min(100, reputation)))

def tick_time(current_datetime):
    # Crédite la rente une fois par mois ingame (10 000€), uniquement si le nouveau système est actif
    global _DERNIERE_RENTE_MOIS
    if not NEW_BUDGET_ENABLED:
        return
    if current_datetime is None:
        return
    annee_mois = (current_datetime.year, current_datetime.month)
    if _DERNIERE_RENTE_MOIS is None or annee_mois != _DERNIERE_RENTE_MOIS:
        _DERNIERE_RENTE_MOIS = annee_mois
        crediter(10000, motif="Rente mensuelle")

def planifier_depense(nom, montant, categorie="général", date=None):
    # Enregistre une dépense à exécuter plus tard (non bloquant tant que désactivé)
    PLANNED_EXPENSES.append({
        "nom": nom,
        "montant": int(montant),
        "categorie": categorie,
        "date": date
    })
    return True

def executer_depenses_planifiees(current_datetime):
    if not NEW_BUDGET_ENABLED:
        return
    a_executer = []
    for d in PLANNED_EXPENSES:
        if d.get("date") is None or (current_datetime and current_datetime >= d["date"]):
            a_executer.append(d)
    for d in a_executer:
        debiter(d["montant"], motif=f"Dépense planifiée: {d['nom']} ({d.get('categorie','général')})")
        PLANNED_EXPENSES.remove(d)
