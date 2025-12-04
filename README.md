# 🎰 Casino Python - Hub de Jeux de Casino

Un projet de casino virtuel complet développé en Python avec une interface graphique moderne utilisant Tkinter. Ce projet comprend un hub central permettant de naviguer entre différents jeux de casino avec un solde partagé.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Jeux disponibles](#-jeux-disponibles)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Fonctionnalités détaillées](#-fonctionnalités-détaillées)
- [Technologies utilisées](#-technologies-utilisées)
- [Aperçu](#-aperçu)

## ✨ Fonctionnalités

- **Hub central** : Navigation fluide entre les différents jeux dans une seule fenêtre
- **Solde partagé** : Votre solde est synchronisé automatiquement entre tous les jeux
- **Interface graphique moderne** : Design soigné avec des couleurs de casino authentiques
- **Système de jetons** : Jetons visuels avec drag & drop pour placer vos mises
- **Animations** : Roulette animée avec rotation réaliste
- **Historique** : Suivi des résultats précédents
- **Mode triche** : Fonctionnalité cachée pour le blackjack (cliquez sur le titre)

## 🎮 Jeux disponibles

### 🂡 Blackjack

Un jeu de blackjack complet avec toutes les règles classiques :

- **Règles du jeu** :
  - Approchez-vous de 21 sans dépasser
  - Battez le croupier pour gagner
  - Blackjack (21 en 2 cartes) = gain 3:2
  - Possibilité de doubler votre mise
  - Le croupier tire jusqu'à 17 minimum

- **Fonctionnalités** :
  - 6 paquets de cartes (configurable : 1, 2, 4, 6 ou 8 paquets)
  - Remélange automatique à 10% des cartes restantes
  - Affichage des cartes avec couleurs (rouge/noir)
  - Système de jetons avec drag & drop
  - Mode triche (cliquez sur le titre "BLACKJACK")
  - Compteur de cartes restantes

### 🎰 Roulette

Une roulette européenne complète (0-36) avec tous les types de paris :

- **Types de paris disponibles** :
  - **Paris simples** : Rouge, Noir, Pair, Impair, Manque (1-18), Passe (19-36)
  - **Douzaines** : 1-12, 13-24, 25-36
  - **Colonnes** : Colonne 1, 2, 3 (multiplicateur 2:1)
  - **Pari sur nombre** : Pari direct sur un numéro (multiplicateur 36:1)

- **Fonctionnalités** :
  - Animation réaliste de la roue avec ralentissement progressif
  - Table de paris interactive avec clic pour placer les mises
  - Historique des 20 derniers numéros
  - Récapitulatif détaillé des gains et pertes
  - Répétition des mises précédentes
  - Réinitialisation des mises avec remboursement

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- Tkinter (généralement inclus avec Python)

### Installation des dépendances

Aucune dépendance externe n'est requise ! Le projet utilise uniquement les bibliothèques standard de Python :

- `tkinter` - Interface graphique
- `random` - Génération aléatoire
- `math` - Calculs mathématiques pour les animations
- `typing` - Annotations de type

### Téléchargement

```bash
git clone https://github.com/votre-username/casino-python.git
cd casino-python
```

## 💻 Utilisation

### Lancer le Casino Hub

Pour démarrer l'application complète avec le hub central :

```bash
python Casino_Hub.py
```

### Lancer les jeux individuellement

Vous pouvez également lancer chaque jeu séparément :

```bash
# Blackjack seul
python Blackjack.py

# Roulette seule
python Roulette.py
```

### Navigation dans l'interface

1. **Hub principal** : Choisissez votre jeu (Blackjack ou Roulette)
2. **Retour au Hub** : Utilisez le bouton "🏠 Retour au Hub" dans chaque jeu
3. **Solde** : Votre solde est automatiquement synchronisé entre les jeux
4. **Réinitialisation** : Utilisez le bouton "🔄 Réinitialiser le solde" dans le hub

## 📁 Structure du projet

```
casino-python/
│
├── Casino_Hub.py          # Hub central avec navigation entre les jeux
├── Blackjack.py           # Jeu de blackjack complet
├── Roulette.py            # Jeu de roulette européenne
└── README.md              # Ce fichier
```

## 🔧 Fonctionnalités détaillées

### Blackjack

#### Système de cartes
- **Paquets multiples** : Utilisez 1, 2, 4, 6 ou 8 paquets (par défaut : 6)
- **Remélange automatique** : Le jeu est remélangé automatiquement quand il ne reste que 10% des cartes
- **Affichage visuel** : Cartes avec bordures ASCII et couleurs appropriées

#### Système de mise
- **Jetons disponibles** : 5, 10, 25, 50, 100, 500 jetons
- **Drag & Drop** : Glissez-déposez les jetons dans la zone de mise
- **Confirmation** : Confirmez votre mise avant de commencer à jouer
- **Double** : Doublez votre mise et recevez une seule carte supplémentaire

#### Mode triche
- Cliquez sur le titre "🂡 BLACKJACK 🂡" pour activer/désactiver
- Affiche les cartes qui seront distribuées avant de placer la mise
- Révèle la carte cachée du croupier pendant le jeu

### Roulette

#### Animation
- **Rotation réaliste** : La boule tourne autour de la roue avec ralentissement progressif
- **Easing** : Animation fluide avec courbe d'accélération/décélération
- **Position finale** : Le numéro gagnant est déterminé par la position finale de la boule

#### Système de paris
- **Sélection de jeton** : Cliquez sur un jeton pour le sélectionner
- **Placement** : Cliquez sur la table de paris pour placer votre mise
- **Multiples paris** : Placez plusieurs paris avec le même jeton sélectionné
- **Empilage visuel** : Les jetons s'empilent visuellement sur la table

#### Récapitulatif
- Affichage détaillé de chaque pari gagnant/perdant
- Calcul automatique des gains selon les multiplicateurs
- Historique des 20 derniers numéros avec couleurs

## 🛠️ Technologies utilisées

- **Python 3.7+** : Langage de programmation
- **Tkinter** : Interface graphique native
- **Random** : Génération de nombres aléatoires
- **Math** : Calculs pour les animations de la roulette
- **Typing** : Annotations de type pour une meilleure maintenabilité

## 📸 Aperçu

### Hub Principal
- Interface centrale avec sélection de jeu
- Affichage du solde partagé
- Bouton de réinitialisation

### Blackjack
- Zone de mise avec drag & drop
- Affichage des cartes du joueur et du croupier
- Compteur de points en temps réel
- Indicateur de cartes restantes

### Roulette
- Roue animée avec numéros colorés
- Table de paris interactive
- Historique des numéros
- Récapitulatif des gains/pertes

## 🎯 Règles des jeux

### Blackjack
- **Objectif** : Obtenir une main plus proche de 21 que le croupier sans dépasser
- **Valeurs** : As = 11 ou 1, Figures = 10, Autres = valeur nominale
- **Blackjack** : 21 en 2 cartes = gain 3:2
- **Croupier** : Tire jusqu'à atteindre au moins 17
- **Double** : Doublez votre mise et recevez une seule carte

### Roulette
- **Type** : Roulette européenne (0-36)
- **Multiplicateurs** :
  - Pari sur nombre : 36:1
  - Douzaines/Colonnes : 3:1
  - Paris simples (rouge/noir/pair/impair/manque/passe) : 2:1

## 🐛 Fonctionnalités cachées

- **Mode triche Blackjack** : Cliquez sur le titre "🂡 BLACKJACK 🂡" pour voir les cartes à l'avance
- **Changement de paquets** : Cliquez sur le sous-titre des paquets pour changer le nombre de paquets

## 📝 Notes

- Le solde initial est de 1000 jetons
- Le solde est partagé entre tous les jeux
- Les gains et pertes sont calculés selon les règles officielles des casinos
- L'historique de la roulette conserve les 20 derniers numéros

## 👨‍💻 Auteur

- Arnaud KINDBEITER
---
