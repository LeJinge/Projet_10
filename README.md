# Projet 10 - Développez une API Rest avec Django Rest Framework

Le projet consiste à créer une API Rest pour la gestion de projet. Les utilisateurs pourront créer des projets, ajouter 
des membres à ce projet, créer des tâches et des commentaires pour ces tâches.
Le projet est réalisé avec Django Rest Framework et utilise Poetry pour la gestion des dépendances.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Poetry
- Python
- Django
- Django Rest Framework

## Installation

Suivez ces étapes pour installer et configurer le projet sur votre machine locale.

### Cloner le Répertoire

Pour récupérer le projet depuis Git, ouvrez votre terminal, aller dans le dossier où vous souhaitez cloner le projet et
exécuter la commande suivante :
```
git clone https://github.com/LeJinge/Projet_10.git
```
### Configurer l'Environnement Virtuel

#### Installation de Pipx

- Sur Windows :
```
python -m pip install pipx
```
- Sur Unix ou MacOS :
```
brew install pipx

pipx ensurepath
```
#### Installation de Poetry

- Sur Windows, Unix ou MacOS:
```
pipx install poetry
```

#### Installer les dépendances
Installez toutes les dépendances nécessaires, aller sur la racine du projet et exécuter la commande suivante :
```
poetry install
```

### Lancement du Serveur de Développement
Pour lancer le serveur de développement, exécutez :
```
python manage.py runserver
```