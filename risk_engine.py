def analyze_slip(legs):
    risk_score = 0
    warnings = []
    suggestions = []
    flagged_legs = []

    matches = {}

    for leg in legs:
        odds = leg.get("odds", 1.5)
        match = leg.get("match", "")
        market = leg.get("market", "")

        if odds > 2.0:
            risk_score += 15
            flagged_legs.append(leg)

        if match in matches:
            matches[match] += 1
        else:
            matches[match] = 1

        if market.lower() in ["btts", "over 2.5", "winner"]:
            risk_score += 10

    for match, count in matches.items():
        if count > 1:
            warnings.append(f"Multiple selections from {match}")
            risk_score += 15

    if len(legs) >= 5:
        warnings.append("High leg count increases variance")
        risk_score += 20

    if risk_score > 60:
        suggestions.append("Consider removing the highest odds leg")
        suggestions.append("Reduce same-game selections")

    risk_score = min(risk_score, 100)

    return {
        "risk_score": risk_score,
        "warnings": warnings,
        "suggestions": suggestions,
        "flagged_legs": flagged_legs
    }