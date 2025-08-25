# 🌍 Système de Bonus Linguistiques - Création de Réseaux

## 📋 **Vue d'ensemble**

Le système de bonus linguistiques influence la création de réseaux clandestins selon les compétences linguistiques de l'agent créateur. Un agent maîtrisant les langues locales aura des avantages significatifs.

## 🎯 **Types de Bonus**

### **1. Bonus de Chance de Succès**
- **Langue principale du pays** : +15% de chance de succès
- **2+ langues du pays** : +10% de chance de succès  
- **1 langue du pays** : +5% de chance de succès
- **Aucune langue commune** : Aucun bonus

### **2. Réduction de Coût**
- **Langue principale du pays** : -20% de coût
- **2+ langues du pays** : -15% de coût
- **1 langue du pays** : -10% de coût

### **3. Réduction de Durée**
- **Langue principale du pays** : -30% de durée
- **2+ langues du pays** : -20% de durée
- **1 langue du pays** : -10% de durée

### **4. Bonus de Qualité**
- **Langue principale du pays** : +25% de qualité
- **2+ langues du pays** : +15% de qualité
- **1 langue du pays** : +10% de qualité

## 🆕 **Nouvelles Fonctionnalités**

### **5. Recrutement Ciblé par Langue**
- **Sélection de langue** : Liste déroulante avec 100+ langues disponibles
- **Ciblage intelligent** : L'agent recruté maîtrise obligatoirement la langue ciblée
- **Coût adapté** : 5000€ pour recrutement ciblé, 2000€ pour classique
- **Combinaisons** : Peut être combiné avec ciblage par bureau, compétences et pays

### **6. Formations Linguistiques**
- **Catalogue complet** : 100+ langues disponibles à l'apprentissage
- **Limite de 5 langues** : Un agent ne peut maîtriser que 5 langues maximum
- **Niveaux de difficulté** :
  - 🟢 **Facile** : Anglais, espagnol, italien, portugais, afrikaans
  - 🟠 **Moyenne** : Allemand, russe, turc, polonais, suédois
  - 🔴 **Difficile** : Chinois, japonais, arabe, finnois, grec
  - ⚫ **Très difficile** : Islandais, hawaïen, papou, inuktitut
- **Coûts variables** : De 5000€ (facile) à 12000€ (très difficile)
- **Durées adaptées** : De 3 jours (facile) à 8 jours (très difficile)

### **7. Qualité du Réseau Influencée par le Responsable**
- **Responsable linguistiquement compétent** : +15% à +5% de qualité
- **Responsable ne parlant pas les langues locales** : -10% de qualité
- **Impact sur la recherche de sources** :
  - **Excellente** : +25% de chance de succès
  - **Bonne** : +15% de chance de succès
  - **Améliorée** : +10% de chance de succès
  - **Standard** : Aucun bonus
  - **Faible** : -10% de chance de succès

## 🔧 **Implémentation Technique**

### **Fonction Principale**
```python
# Calculer les bonus de langue pour un agent et un pays
bonus = reseaux.calculer_bonus_langue_agent(agent, pays_cible)

# Créer un réseau avec bonus appliqués
succes, message = reseaux.ajouter_reseau_avec_bonus(nom, pays, ville, agent_createur)

# Mettre à jour la qualité selon le responsable
reseaux.mettre_a_jour_qualite_reseau(nom_reseau)
```

### **Structure des Bonus**
```python
bonus = {
    "chance_succes": 15,      # +15% de chance de succès
    "reduction_cout": 20,     # -20% de coût
    "reduction_duree": 30,    # -30% de durée
    "bonus_qualite": 25,      # +25% de qualité
    "langues_maitrisees": ["français", "anglais"],
    "langues_pays": ["français", "anglais", "allemand"]
}
```

## 📊 **Exemples Concrets**

### **Agent Francophone en France**
- **Langues de l'agent** : français, anglais
- **Langues du pays** : français, anglais, allemand, espagnol, arabe
- **Langues communes** : français, anglais
- **Bonus appliqués** :
  - Chance de succès : +15% (français = langue principale)
  - Réduction de coût : -20%
  - Réduction de durée : -30%
  - Bonus de qualité : +25%

### **Agent Anglophone en Allemagne**
- **Langues de l'agent** : anglais
- **Langues du pays** : allemand, anglais, turc, français
- **Langues communes** : anglais
- **Bonus appliqués** :
  - Chance de succès : +5% (anglais ≠ langue principale)
  - Réduction de coût : -10%
  - Réduction de durée : -10%
  - Bonus de qualité : +10%

### **Agent Monolingue en Chine**
- **Langues de l'agent** : français
- **Langues du pays** : chinois, anglais, cantonais, ouïghour
- **Langues communes** : aucune
- **Bonus appliqués** : Aucun

## 🎮 **Utilisation en Interface**

### **1. Création de Réseau**
L'interface affiche automatiquement :
- Les langues de l'agent sélectionné
- Les langues du pays cible
- Les langues communes identifiées
- Les bonus qui seront appliqués

### **2. Recrutement Ciblé par Langue**
- **Assistant de recrutement** avec sélection de langue
- **Liste déroulante** de 100+ langues disponibles
- **Prévisualisation** des critères de ciblage
- **Coût estimé** en temps réel

### **3. Formations Linguistiques**
- **Catalogue séparé** des formations linguistiques
- **Filtrage automatique** des langues déjà maîtrisées
- **Indicateur de difficulté** avec code couleur
- **Limite de 5 langues** respectée automatiquement

### **4. Affichage des Réseaux**
Les réseaux en cours affichent :
- Le coût final (après réduction)
- Les langues communes utilisées
- Le bonus de chance de succès
- La qualité actuelle du réseau

### **5. Fiche Réseau**
Chaque réseau affiche :
- Sa qualité (Standard, Améliorée, Bonne, Excellente)
- Les bonus linguistiques appliqués
- L'impact du responsable sur la qualité
- L'historique des événements avec mentions linguistiques

### **6. Recherche de Sources**
- **Qualité du réseau** affichée clairement
- **Impact sur la recherche** calculé automatiquement
- **Chance de succès** ajustée selon la qualité
- **Durée estimée** optimisée selon les bonus

## 💰 **Impact Économique**

### **Coût de Base**
- **Réseau standard** : 15 000€
- **Avec bonus linguistique** : 12 000€ à 13 500€

### **Durée de Création**
- **Durée de base** : 10-60 jours
- **Avec bonus linguistique** : 7-54 jours

### **Qualité du Réseau**
- **Standard** : Pas de bonus
- **Améliorée** : +10% de qualité
- **Bonne** : +15% de qualité
- **Excellente** : +25% de qualité

### **Formations Linguistiques**
- **Langues faciles** : 5000-7000€
- **Langues moyennes** : 7000-9000€
- **Langues difficiles** : 9000-11000€
- **Langues très difficiles** : 11000-12000€

## 🚀 **Stratégies Recommandées**

### **1. Formation Linguistique**
- **Former les agents** aux langues des pays d'intérêt
- **Prioriser les langues principales** pour maximiser les bonus
- **Développer le polyglottisme** pour la flexibilité
- **Respecter la limite de 5 langues** par agent

### **2. Affectation Stratégique**
- **Envoyer des agents locuteurs** dans leurs pays d'origine
- **Utiliser des agents multilingues** pour les régions complexes
- **Éviter les agents monolingues** dans des pays étrangers
- **Choisir des responsables** linguistiquement compétents

### **3. Développement de Réseaux**
- **Créer des réseaux de qualité** avec des agents linguistiquement compétents
- **Maximiser les bonus** en choisissant les bons agents
- **Optimiser les coûts** grâce aux réductions linguistiques
- **Maintenir la qualité** avec des responsables compétents

### **4. Recrutement Optimisé**
- **Cibler par langue** pour les missions spécifiques
- **Combiner les critères** (bureau + compétences + langue + pays)
- **Investir dans la formation** linguistique des agents existants
- **Équilibrer coût et efficacité** selon les besoins

## ⚠️ **Limitations et Notes**

- **Langues exactes** : La correspondance doit être exacte (sensible à la casse)
- **Bonus cumulatifs** : Les bonus ne se cumulent pas, le meilleur est appliqué
- **Pays exacts** : La correspondance pays doit être exacte
- **Limite de langues** : Maximum 5 langues par agent
- **Fallback** : Si le module langues n'est pas disponible, aucun bonus n'est appliqué

## 🔍 **Surveillance et Debug**

### **Logs Automatiques**
Le système génère des logs informatifs :
```
INFO: Bonus linguistiques appliqués pour la création du réseau 'Réseau Alpha'
INFO: Agent parle français (langue principale) → +15% succès, -20% coût, -30% durée, +25% qualité
INFO: Qualité du réseau mise à jour: Excellente (+35%)
INFO: Formation linguistique terminée — Agent Dupont Jean a acquis: russe
```

### **Vérification des Bonus**
```python
# Vérifier les bonus d'un agent pour un pays
bonus = reseaux.calculer_bonus_langue_agent(agent, "France")

# Créer un réseau avec bonus
succes, message = reseaux.ajouter_reseau_avec_bonus("Réseau Test", "France", "Paris", agent)

# Mettre à jour la qualité selon le responsable
reseaux.mettre_a_jour_qualite_reseau("Réseau Test")
```

## 🌟 **Évolutions Futures**

- **Bonus de compétence** combinés avec les bonus linguistiques
- **Formations linguistiques avancées** (niveaux de maîtrise)
- **Historique des bonus** appliqués sur les réseaux
- **Interface de gestion** des compétences linguistiques
- **Système de traduction** pour les agents monolingues
- **Évaluation de la maîtrise** des langues (débutant, intermédiaire, expert)
- **Formations combinées** (langue + compétence dans un domaine)
- **Impact sur les relations** avec les agences locales
