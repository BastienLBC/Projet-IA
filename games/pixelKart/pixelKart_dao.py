import os

FILE_PATH = "circuits.txt"

def get_all():
    """Retrieve all circuits from the file as a dictionary {name: str}."""
    circuits = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                name,circuit = line.split(":")
                if name:
                    circuits[name] = circuit
    return circuits

def get_by_name(name):
    """Retrieve a circuit by its name."""
    circuits = get_all()
    return circuits.get(name)

def save_circuit(name, string):
    """Save a new circuit to the file."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")
    circuits = get_all()
    if name in circuits:
        raise ValueError(f"The circuit '{name}' already exists.")
    with open(FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"\n{name}:{string}")

def delete_circuit(name):
    """Delete a circuit by its name."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")
    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")
    del circuits[name]
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        for circuit_name in circuits:
            file.write(circuit_name + "\n")

def update_circuit(name, string):
    """Update the name of an existing circuit."""
    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")
    
    circuits[name] = string
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        for circuit_name in circuits:
            file.write(circuit_name + "\n")