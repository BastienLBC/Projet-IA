# Projet-IA

## À propos

Le projet est un jeu qui se joue soit en 1 contre 1, ou 1 joueur contre l'ordinateur. C'est le jeu des allumettes, à chaque tour les joueurs devront prendre une, deux ou trois allumettes. Celui qui prend la dernière allumette a perdu. 

## Table des matières

1. [À propos](#à-propos)
2. [Installation](#installation)
3. [Utilisation](#utilisation)
4. [Comment contribuer](#comment-contribuer)
5. [Informations sur la licence](#informations-sur-la-licence)

## Installation
Vous pouvez utiliser un environnement virtuel comme Venv pour isoler les dépendances du projet avant de télécharger les packages.  

Ouvrez votre terminal, et exécutez ces commandes pour installer tout le nécéssaire
```
git clone https://github.com/BastienLBC/Projet-IA.git
cd projet-ia
pip install -r requirements.txt
```

## Utilisation 
Une fois le projet installé, vous pouvez lancer les jeux en exécutant la commande suivante :
```
python launcher.py
```

Une fenêtre va s'ouvrir et vous pourrez choisir le jeu auquel vous souhaitez jouer : Cubee ou Allumettes.

### Cubee

Par défaut, Cubee se joue contre un bot qui joue des coups aléatoires.

Pour jouer contre un autre joueur, modifiez la classe Player en HumanPlayer pour player1 dans le fichier :

```
games/Cube/main.py
```
### Allumettes

Par défaut, vous jouez contre une IA.

Pour jouer contre un autre joueur, modifiez la classe Human en Player pour p1 dans le fichier :
```

games/Allumettes/main.py
```

## Comment contribuer 
Pour contribuer au projet, vous pouvez nous aider à résoudre le problème que nous rencontrons avec l'animation des torches, dans les [`game_view.py`](./games/torches/Game/game_view.py).

## Informations sur la licence
