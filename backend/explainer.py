def generate_explanation(country_from, country_to, data_type, status, risk_score):
    reasons = []

    reasons.append(
        f"The data transfer originates from {country_from} and is intended for {country_to}."
    )

    if data_type == "personal_data":
        reasons.append(
            "The data being transferred contains personal information, which increases regulatory obligations."
        )

    if country_to in ["Germany", "France", "EU"]:
        reasons.append(
            f"{country_to} is governed by GDPR, which allows cross-border data transfers only when adequate safeguards are in place."
        )

    if status == "BLOCKED":
        reasons.append(
            f"Current regulations in {country_from} prohibit cross-border data sharing, making this transfer legally disallowed."
        )
    elif status == "REVIEW_REQUIRED":
        reasons.append(
            "Although the transfer is not explicitly prohibited, it requires compliance review and legal safeguards before proceeding."
        )
    else:
        reasons.append(
            "No regulatory restrictions were triggered, and the transfer is considered low risk."
        )

    reasons.append(f"The final risk score for this transfer is {risk_score} out of 100.")

    return " ".join(reasons)
