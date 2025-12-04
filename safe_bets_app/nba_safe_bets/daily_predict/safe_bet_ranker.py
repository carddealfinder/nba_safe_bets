import pandas as pd


def rank_safe_bets(df, models):
    """
    Apply each model (points, assists, etc.) and produce a ranking score.
    """

    if df.empty:
        return pd.DataFrame()

    output_rows = []

    for stat, model in models.items():
        if stat not in ["points", "rebounds", "assists", "threes"]:
            continue

        if not hasattr(model, "predict_proba"):
            continue

        # Fill missing
        features = df.select_dtypes(include=['number']).fillna(0)

        if features.empty:
            continue

        try:
            proba = model.predict_proba(features)[:, 1]
        except Exception:
            continue

        for idx, p in df.iterrows():
            output_rows.append({
                "player": f"{p['first_name']} {p['last_name']}",
                "team": p.get("team"),
                "stat": stat,
                "model_prob": proba[idx],
                "line": p.get("line", None),
                "opponent": p.get("opponent", None)
            })

    ranked = pd.DataFrame(output_rows)

    if ranked.empty:
        return ranked

    ranked["safety_score"] = ranked["model_prob"].rank(pct=True)

    return ranked.sort_values("safety_score", ascending=False)
