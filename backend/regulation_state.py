# backend/regulation_state.py
import json
import os

FILE_PATH = "backend/regulation_state.json"

def load_state():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_state(state):
    with open(FILE_PATH, "w") as f:
        json.dump(state, f, indent=2)

REGULATION_STATE = load_state()
