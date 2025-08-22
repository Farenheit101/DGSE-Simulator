# budget.py

SOLDE = 200000  # Solde de départ (modulable)
HISTORIQUE = []

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
