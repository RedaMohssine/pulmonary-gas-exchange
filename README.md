# Modélisation Numérique des Échanges Gazeux Pulmonaires

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Description

Projet de recherche biomédicale sur la **modélisation numérique 2D des échanges gazeux dans les poumons**. Ce projet implémente des simulations de diffusion et convection pulmonaire en utilisant des méthodes numériques avancées (différences finies, Crank-Nicolson) pour résoudre des équations aux dérivées partielles.

**Période** : Novembre 2024 – Janvier 2025  
**Encadrement** : M. Marcel Filoche

> **Pour les détails physiques et scientifiques complets de cette modélisation**, consultez le [rapport technique](docs/rapport_Biomedical_Groupe01.pdf).

## Structure du Projet

```
biomed/
├── README.md                         # Documentation complète
├── requirements.txt                  # Dépendances Python
├── .gitignore                       # Fichiers à ignorer par Git
│
├── docs/                            # Documentation
│   ├── rapport_Biomedical_Groupe01.pdf   # Rapport technique complet
│   └── guide_utilisation.pdf             # Guide d'utilisation PDF
│
├── diffusion/                       # Module de diffusion
│   ├── diffusion_sans_def.py       #  Cas simple - Validation analytique
│   ├── diffusion_avec_def.py       #  Interface graphique - Géométries complexes
│   └── diffusion_temporel.py       #  Évolution temporelle - Animation
│
└── convection/                      # Module de convection
    ├── convection_sans_def.py      # Cas simple
    ├── convection_sans_def_2.py    # Validation Poiseuille complète
    ├── convection_avec_def.py      # Écoulement avec obstacles
    └── convection_temporel.py      #  Évolution temporelle - Animation
```

##  Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des dépendances

```bash
# Cloner le dépôt
git clone https://github.com/[votre-username]/pulmonary-gas-exchange.git
cd pulmonary-gas-exchange

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Module Diffusion

#### 1. Cas Simple avec Validation (`diffusion_sans_def.py`)

Simulation de référence avec validation analytique.

```bash
python diffusion/diffusion_sans_def.py
```

**Résultats** : Carte de concentration, champ de flux, comparaison numérique vs analytique, calcul du débit.

#### 2. Géométries Complexes (`diffusion_avec_def.py`)

Interface graphique pour créer des géométries personnalisées avec obstacles.

```bash
python diffusion/diffusion_avec_def.py
```

**Utilisation** : Choisir une forme (Rectangle/Ellipse/Polygone) → Ajuster dimensions → Placer → Définir conditions limites → Lancer simulation.

#### 3. Évolution Temporelle (`diffusion_temporel.py`)

Animation de la diffusion au cours du temps.

```bash
python diffusion/diffusion_temporel.py
```

**Fonctionnalités** : Animation temps réel, export GIF, convergence vers état stationnaire.

### Module Convection

#### 1. Cas Simple (`convection_sans_def_2.py`) Recommandé

Validation complète avec solution de Poiseuille.

```bash
python convection/convection_sans_def_2.py
```

**Résultats** : Champs de vitesse et pression, validation Poiseuille, analyse des résidus, calcul du débit.

#### 2. Écoulement avec Obstacles (`convection_avec_def.py`)

Simulation autour d'obstacles sphériques.

```bash
python convection/convection_avec_def.py
```

#### 3. Évolution Temporelle (`convection_temporel.py`)

Animation de l'évolution de l'écoulement.

```bash
python convection/convection_temporel.py
```

**Fonctionnalités** : Animation double (pression + vitesse), export GIF, évolution du débit.

## 📚 Documentation Complète

Pour les détails physiques, scientifiques et mathématiques complets de cette modélisation :
- **[Rapport Technique Complet](docs/rapport_Biomedical_Groupe01.pdf)** : Contexte biomédical, formulation mathématique, méthodes numériques, validation et analyses
- **[Guide d'Utilisation PDF](docs/guide_utilisation.pdf)** : Instructions détaillées

## Technologies Utilisées

- **Python 3.8+**
- **NumPy** : Calcul numérique et algèbre linéaire
- **SciPy** : Résolution de systèmes linéaires creux
- **Matplotlib** : Visualisation 2D/3D et animations
- **Tkinter** : Interface graphique (inclus avec Python)

## Dépannage

### Problèmes Courants

** Erreur : "Matrix is singular"**
- Vérifier que le domaine est connexe
- Ajouter au moins un point de condition de Dirichlet
- Réduire la taille du maillage

** Animation ne se sauvegarde pas**
```bash
pip install pillow
```

** "tkinter not found"**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows : Réinstaller Python avec option "tcl/tk and IDLE"
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## Auteur

**Auteur** : Groupe 1 (dont moi : Mohamed MOHSSINE)
**Encadrant** : M. Marcel Filoche  
**Période** : Novembre 2024 – Janvier 2025

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !
