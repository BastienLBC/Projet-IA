from games.pixelKart.dao import init_db, commit_session
from games.pixelKart.pixelKart_dao import get_by_name
from games.pixelKart.game_models.circuit import Circuit
from games.pixelKart.game_models.kart import aiKart, kart

def train(circuit_name: str, episodes: int = 1000, laps: int = 1, max_steps: int = 500):
    circuit_data = get_by_name(circuit_name)
    if circuit_data is None:
        raise ValueError(f"Circuit '{circuit_name}' not found")

    ai = aiKart("AI")
    bob = kart("bob")
    env = Circuit(ai, bob, gp=circuit_data)
    env.nb_laps = laps

    for _ in range(episodes):
        env.start()
        ai.circuit = env.circuit
        ai.grid = env.grid
        env.current_player = ai

        done = False
        steps = 0
        while not done and steps < max_steps:
            state = ai.state_key()
            action = ai.choose_action()
            env.one_action(action)

            reward = -1
            if not ai.inLife:
                reward = -100
                done = True
            elif env.game_over or ai.laps >= env.nb_laps:
                reward = 100
                done = True
            else:
                case = env.type_case()
                if case == "GRASS":
                    reward -= 2
                elif case == "WALL":
                    reward -= 50
                    done = True

            next_state = ai.state_key()
            ai.update_q_table(state, action, reward, next_state)
            steps += 1

        ai.next_epsilon()

    commit_session()



def main():
    init_db()
    train("Masque", 100000, 2)

if __name__ == "__main__":
    main()