from backend.regulation_state import REGULATION_STATE

def evaluate_compliance(country_from, country_to, data_type, action_type):
    country_rules = REGULATION_STATE.get(country_from)

    if not country_rules:
        return {
            "status": "BLOCKED",
            "risk_score": 100,
            "ai_explanation": f"No regulation data found for {country_from}."
        }

    # Check allowed data types
    allowed_types = country_rules.get("allowed_data_types", [])
    if data_type not in allowed_types:
        return {
            "status": "BLOCKED",
            "risk_score": 100,
            "ai_explanation": (
                f"{data_type.replace('_', ' ')} is not permitted for cross-border "
                f"transfer from {country_from} under current regulations."
            )
        }

    # Check allowed actions
    allowed_actions = country_rules.get("allowed_actions", [])
    if action_type not in allowed_actions:
        return {
            "status": "BLOCKED",
            "risk_score": 100,
            "ai_explanation": (
                f"The action '{action_type.replace('_', ' ')}' is currently blocked "
                f"for {country_from} due to updated regulations."
            )
        }

    # ---- Risk scoring ----
    risk_score = 20

    if data_type == "personal_data":
        risk_score += 50

    if country_to in ["Germany", "France", "EU"]:
        risk_score += 20  # GDPR impact

    status = "ALLOWED" if risk_score < 80 else "REVIEW_REQUIRED"

    return {
        "status": status,
        "risk_score": risk_score,
        "ai_explanation": (
            f"The transfer involves {data_type.replace('_', ' ')} via action "
            f"'{action_type.replace('_', ' ')}' from {country_from} to {country_to}. "
            f"The data type is allowed by the source country. "
            f"However, regulatory safeguards may still apply based on destination laws."
        )
    }
