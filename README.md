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
Une fois le projet installé, vous pouvez lancer le jeu en exécutant le fichier Alumettes.py. Une fenêtre va alors s'ouvrir et vous pourrez jouer au jeu. Si vous voulez jouer contre l'ordinateur, il vous suffit de modifier la classe `Human` de `p1` en `Player`.
Ou exécutez le dans votre terminal via :
```
python games\torches\Alumettes.py
```
Si vous voulez jouer a cubee, vous pouvez lancer le jeu en exécutant le fichier main.py dans le dossier Cube. Une fenêtre va alors s'ouvrir et vous pourrez jouer au jeu. Par défaut vous jouer contre un bot qui joue en aléatoire, si vous voulez jouer contre un autre joueur il vous suffit de modifier la classe `HumanPlayer` en `Player`.
Ou exécutez le dans votre terminal via :
```
python games\Cube\main.py
```
## Comment contribuer 
Pour contribuer au projet, vous pouvez nous aider à résoudre le problème que nous rencontrons avec l'animation des torches, dans les [`game_view.py`](./games/torches/Game/game_view.py).

## Informations sur la licence
