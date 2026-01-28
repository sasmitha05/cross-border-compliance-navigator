import json
import os
from pathlib import Path

# Use absolute path relative to this file
FILE_PATH = Path(__file__).parent / "regulation_state.json"

def load_state():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    # On Vercel, writes will fail - handle gracefully
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"State save failed (expected on Vercel): {e}")

REGULATION_STATE = load_state()