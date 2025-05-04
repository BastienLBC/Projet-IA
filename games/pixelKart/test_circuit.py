import unittest
from game_models.circuit import Circuit
from game_models.kart import kart, humanKart

class TestCircuit(unittest.TestCase):
    def test_cpt_laps(self):
        player1 = humanKart(name="Player1", x=0, y=0, speed=1)
        player2 = humanKart(name="Player2", x=0, y=0, speed=1)
        circuit = Circuit(10, 10, player1, player2)
        circuit.start_line = [(0, 0)]
        circuit.current_player = player1

        player1.direction = "Est"
        circuit.cpt_laps()
        self.assertEqual(player1.laps, 1)

        player1.direction = "Nord"
        circuit.cpt_laps()
        self.assertEqual(player1.laps, 1)  # Pas de tour ajouté

    def test_type_case(self):
        circuit_data = "GGG,GRG,GGG"
        player1 = kart(name="Player1", x=1, y=1, speed=1)
        circuit = Circuit(3, 3, player1, None, circuit_data)
        circuit.current_player = player1

        self.assertEqual(circuit.type_case(), "ROAD")

if __name__ == "__main__":
    unittest.main()