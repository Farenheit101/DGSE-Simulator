# budget.py

SOLDE = 200000  # Solde de départ (modulable)
HISTORIQUE = []

# --- Nouveau système de budget (désactivé par défaut) ---
NEW_BUDGET_ENABLED = False  # Active le nouveau modèle lorsqu'il passera en production

# Montants fixes pour le recrutement d'agents (nouveau système)
RECRUIT_COST_ALEA = 2000
RECRUIT_COST_CIBLE = 5000

# Dépenses planifiées (futures fonctionnalités)
PLANNED_EXPENSES = []  # {"nom": str, "montant": int, "categorie": str, "date": datetime}

# Suivi rente quotidienne
_DERNIERE_RENTE_DATE = None  # last day when rente was credited

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

def get_reputation_service():
    # Placeholder : sera remplacé par le futur système de réputation
    # Retourne une réputation entre 0 et 100
    return 50

def calculer_rente_journaliere(reputation):
    # Formule simple et modulable
    # Exemple: base 1000€ + 30€ par point de réputation
    return 1000 + int(30 * max(0, min(100, reputation)))

def tick_time(current_datetime):
    # Crédite la rente une fois par jour, uniquement si le nouveau système est actif
    global _DERNIERE_RENTE_DATE
    if not NEW_BUDGET_ENABLED:
        return
    if current_datetime is None:
        return
    jour = current_datetime.date()
    if _DERNIERE_RENTE_DATE is None or jour > _DERNIERE_RENTE_DATE:
        _DERNIERE_RENTE_DATE = jour
        rente = calculer_rente_journaliere(get_reputation_service())
        crediter(rente, motif="Rente quotidienne (réputation)")

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
