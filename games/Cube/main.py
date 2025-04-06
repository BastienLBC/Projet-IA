
from Game.dico import generate_key
from Game.dao import save_entry, find_entry_by_key, find_all_entries,init_db
from Game.game_controller import GameController


if __name__ == "__main__":
    init_db()

    # Save an initial entry
    unique_key = generate_key('A1', 'B2', 'C3', 'D4', 'matrix_state', 'board_state')
    entry_dto = {'unique_key': unique_key, 'reward': 0.5}
    save_entry(entry_dto)

    # Find and print the entry
    found_entry = find_entry_by_key(unique_key)
    print("Found entry before update:", found_entry)

    # Update the reward for the existing entry
    updated_entry_dto = {'unique_key': unique_key, 'reward': 0.7}
    save_entry(updated_entry_dto)

    # Find and print the updated entry
    found_entry = find_entry_by_key(unique_key)
    print("Found entry after update:", found_entry)
