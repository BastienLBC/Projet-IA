"""
Module qui gère la logique des alumettes / gestions des tours
"""
import random

class GameModel:
    """
    Modèle du jeu
    gère la gestion du jeu, gestion du nombres d'alumettes

    Attributes:
        original_nb (int): nombre d'alumettes au départ
        nb (int): nombre d'alumette actuellement
        players (list): liste des joueurs
        displayable (bool): active/désactive l'affichage dans la console
        current_player: Joueur dont c'est le tour
    """
    def __init__(self, nb_torch:int, players1, players2, display: bool=True)->None:
        """
        Initialise une partie.

        Args:
            nb_torch (int): nombre d'alumettes au départ
            players (list): liste des joueurs
            displayable (bool): active/désactive l'affichage dans la console (true par défaut)
        """
        self.original_nb = nb_torch
        self.nb = nb_torch
        self.players1 = players1
        self.players2 = players2
        self.displayable = display
        self.current_player = None

        self.players1.game = self
        self.players2.game = self

        self.shuffle()

    def shuffle(self)->None:
        """
        Selecte aléatoirement un joueur pour commencer
        """
        self.current_player = random.choice([self.players1, self.players2])

    def reset(self)->None:
        """
        Reinitialise le nombre d'alumette et
        rechoisi un joueur aleatoire pour commencer
        """
        self.nb = self.original_nb
        self.shuffle()

    def display(self)->None:
        """
        affiche le nombre d'alumettes restantes dans la console
        """
        if self.displayable:
            print(f"Allumettes restantes: {self.nb}")

    def step(self, action:int)->None:
        """
        Execute l'action, soustrait le nombre d'alumettes choisie

        Args:
            action(int) : nb d'alumettes à retirer
        """
        self.nb -= action

    def is_game_over(self)->bool:
        """
        Verifie si la partie est finie

        Returns:
            bool: si il n'y a plus d'alumettess -> true
        """
        return self.nb <= 0

    def play(self)->None:
        """
        Lance la partie complète
        et alterne les joueurs jusqu'à ce qu'il n'y ai plus d'alumettes
        """
        while self.nb > 0:
            self.display()
            self.step(self.current_player.play())
            if self.nb <= 0:
                self.current_player.lose()
            self.switch_player()
        self.current_player.win()

    def switch_player(self)->None:
        """
        Inverse le joueur courant
        """
        self.current_player = self.players1 if self.current_player == self.players2 else self.players2

    def get_current_player(self)->str:
        """
        Retourne le joueur actuel

        Returns:
            Player: joueur actuel
        """
        return self.current_player

    def get_winner(self)->str:
        """
        Retourne le gagnant de la partie

        Returns: 
            Player: joueur gagnant
        """
        return self.current_player if self.is_game_over() else None

    def get_loser(self)->str:
        """
        Retourne le perdant de la partie

        Returns:
            Player: joueur perdant
        """
        return self.players1 if self.get_winner() == self.players2 else self.players2
