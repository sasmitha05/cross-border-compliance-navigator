import json
from pathlib import Path

RULES_PATH = Path(__file__).parent / "rules.json"

def simulate_regulation_update():
    with open(RULES_PATH) as f:
        rules = json.load(f)

    # Simulate new law
    rules["India"]["share_customer_data"] = {
        "risk": "HIGH",
        "rule": "New Indian data law requires strict localization",
        "decision": "BLOCK"
    }

    with open(RULES_PATH, "w") as f:
        json.dump(rules, f, indent=2)

    return {
        "message": "🚨 Regulation updated",
        "country": "India",
        "impact": "Data sharing is now BLOCKED"
    }
