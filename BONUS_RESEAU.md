# 🎯 Système de Bonus Réseau

## 📋 **Vue d'ensemble**

Le système de bonus réseau permet d'améliorer les chances de réussite des actions quand un agent est rattaché à un réseau clandestin dans le pays de la crise.

## 🏆 **Types de Bonus**

### **Membre de Réseau**
- **Bonus**: +15% sur l'impact des actions réussies
- **Condition**: L'agent doit être rattaché à un réseau dans le pays de la crise
- **Exemple**: Agent rattaché au "Réseau Paris" en France

### **Responsable de Réseau**
- **Bonus**: +20% sur l'impact des actions réussies
- **Condition**: L'agent doit être le responsable d'un réseau dans le pays de la crise
- **Exemple**: Agent responsable du "Réseau Madrid" en Espagne

## 🔧 **Implémentation Technique**

### **Fonctions Principales**

```python
# Vérifier le bonus réseau d'un agent
bonus_info = gestionnaire_actions.obtenir_bonus_reseau_agent("Nom Prénom", "Pays")

# Lister tous les agents avec leurs bonus pour un pays
agents_bonus = gestionnaire_actions.lister_agents_avec_bonus_reseau("Pays")
```

### **Calcul Automatique**
Le bonus est automatiquement appliqué lors du calcul de l'impact des actions :
- **Actions réussies** : Bonus ajouté à l'impact de base
- **Actions échouées** : Aucun bonus (impact négatif inchangé)

## 📊 **Exemples d'Impact**

### **Action de Surveillance (Coût: 5000€)**
- **Sans réseau**: 5-15% d'impact
- **Avec réseau**: 20-30% d'impact (+15%)
- **Avec réseau (responsable)**: 25-35% d'impact (+20%)

### **Action d'Infiltration (Coût: 15000€)**
- **Sans réseau**: 15-30% d'impact
- **Avec réseau**: 30-45% d'impact (+15%)
- **Avec réseau (responsable)**: 35-50% d'impact (+20%)

## 🎮 **Utilisation en Jeu**

### **1. Créer un Réseau**
```python
# Créer un réseau dans un pays
ajouter_reseau("Réseau Alpha", "France", "Paris", 48.8566, 2.3522)
```

### **2. Rattacher un Agent**
```python
# Rattacher un agent au réseau
rattacher_agent_reseau("Réseau Alpha", agent)

# Ou le définir comme responsable
definir_responsable("Réseau Alpha", agent)
```

### **3. Lancer une Action**
Quand vous lancez une action avec un agent rattaché à un réseau dans le pays de la crise, le bonus est automatiquement appliqué.

## 📈 **Stratégies Recommandées**

### **Développement de Réseaux**
1. **Créer des réseaux** dans les pays d'intérêt stratégique
2. **Rattacher des agents** spécialisés selon les besoins
3. **Désigner des responsables** pour maximiser les bonus

### **Optimisation des Missions**
1. **Choisir des agents** avec des réseaux dans le pays cible
2. **Prioriser les responsables** de réseau pour les actions critiques
3. **Développer la couverture** géographique des réseaux

## 🔍 **Surveillance et Debug**

### **Logs Automatiques**
Le système génère automatiquement des logs informatifs :
```
INFO: Bonus réseau appliqué! Agent rattaché au réseau 'Réseau Paris' dans France. 
Impact: 15% + 15% = 30%
```

### **Vérification des Bonus**
```python
# Vérifier le bonus d'un agent spécifique
bonus = gestionnaire_actions.obtenir_bonus_reseau_agent("Agent Nom", "Pays")

# Lister tous les agents avec bonus pour un pays
agents = gestionnaire_actions.lister_agents_avec_bonus_reseau("Pays")
```

## ⚠️ **Limitations et Notes**

- **Bonus uniquement sur succès** : Les échecs ne bénéficient pas du bonus
- **Pays exact** : La correspondance pays doit être exacte (sensible à la casse)
- **Un réseau par pays** : Un agent ne peut avoir qu'un bonus par pays
- **Priorité responsable** : Si un agent est à la fois membre et responsable, le bonus de responsable est appliqué

## 🚀 **Évolutions Futures**

- **Bonus cumulatifs** pour plusieurs réseaux dans la même région
- **Bonus de compétence** combinés avec les bonus réseau
- **Interface graphique** pour visualiser les bonus réseau
- **Historique des bonus** appliqués sur les actions
