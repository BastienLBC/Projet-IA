def on_key_press(self, event):
        """
        Récupère la touche pressée au clavier et appelle la fonction de déplacement du contrôleur
        """
        bind = event.keysym.upper()
        if bind == "Z":
            bind = "Nord"
        elif bind == "S":
            bind = "Sud"
        elif bind == "Q":
            bind = "Ouest"
        elif bind == "D":
            bind = "Est"

        self.kart.direction(bind)
