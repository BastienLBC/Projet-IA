
from Game.dico import generate_key
from Game.dao import save_entry, find_entry_by_key, find_all_entries,init_db
from Game.game_controller import GameController


if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Save entry 1
    unique_key_1 = generate_key('1', '2', '3', '4', 'matrix_state_1', 'board_state_1')
    save_entry({'unique_key': unique_key_1, 'reward': 0.7})

    # Save entry 2
    unique_key_2 = generate_key('4', '4', '0', '0', 'matrix_state_2', 'board_state_2')
    save_entry({'unique_key': unique_key_2, 'reward': 0.9})

    # Save entry 3
    unique_key_3 = generate_key('7', '7', '2', '2', 'matrix_state_3', 'board_state_3')
    save_entry({'unique_key': unique_key_3, 'reward': 0.3})

    # Fetch and print all entries before the update
    print("Before update:")
    entries = find_all_entries()
    print(entries)

    # Modify the reward of entry with unique_key_1
    new_reward = 1.2
    print(f"Updating reward for unique_key: {unique_key_1} to {new_reward}")
    save_entry({'unique_key': unique_key_1, 'reward': new_reward})

    # Fetch and print all entries after the update
    print("After update:")
    entries = find_all_entries()
    print(entries)
