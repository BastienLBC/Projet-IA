def on_key_press(self, event):
        """
        Récupère la touche pressée au clavier et appelle la fonction de déplacement du contrôleur
        """
        bind = event.keysym.upper()
        if bind == "Z":
            bind = "Accelerate"
        elif bind == "S":
            bind = "Decelerate"
        elif bind == "Q":
            bind = "Left"
        elif bind == "D":
            bind = "Right"

        self.circuit.one_action(bind)
