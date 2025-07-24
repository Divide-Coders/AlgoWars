import json

def load_missile_inventory(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

