# Guide de Déploiement sur GitHub

## Étapes Rapides

### 1. Configuration Git (une seule fois)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### 2. Créer le Dépôt sur GitHub

1. Allez sur [github.com](https://github.com) → **New repository**
2. Nom : `pulmonary-gas-exchange`
3. Description : `Modélisation numérique 2D des échanges gazeux pulmonaires`
4. Public ou Private
5. **NE PAS** cocher "Initialize with README"
6. Créer

### 3. Initialiser et Pousser

```bash
# Dans le dossier du projet
cd C:\Users\moham\Documents\biomed

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Modélisation des échanges gazeux pulmonaires"

# Lier au dépôt GitHub (remplacer [votre-username])
git remote add origin https://github.com/[votre-username]/pulmonary-gas-exchange.git

# Pousser sur GitHub
git branch -M main
git push -u origin main
```

### 4. Personnaliser le README

Ouvrez `README.md` et remplacez :
- `[votre-username]` → votre nom GitHub
- `[Votre Nom]` → votre nom complet
- `[Votre Institution]` → votre université/école
- `[votre.email@institution.fr]` → votre email

### 5. Vérifier

Actualisez votre page GitHub → tous les fichiers doivent apparaître.

## Mises à Jour Futures

```bash
# Après modification de fichiers
git add .
git commit -m "Description des changements"
git push
```

## Structure Finale

```
biomed/
├── README.md                    ✅ Documentation complète
├── requirements.txt             ✅ Dépendances
├── .gitignore                   ✅ Fichiers ignorés
├── docs/
│   ├── rapport_Biomedical_Groupe01.pdf
│   └── guide_utilisation.pdf
├── diffusion/
│   ├── diffusion_sans_def.py
│   ├── diffusion_avec_def.py
│   └── diffusion_temporel.py
└── convection/
    ├── convection_sans_def.py
    ├── convection_sans_def_2.py
    ├── convection_avec_def.py
    └── convection_temporel.py
```

✅ Tout est prêt pour GitHub !
