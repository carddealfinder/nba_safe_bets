import pandas as pd
import streamlit as st


# -------------------------------------------------------------------
# Color gradient helper (green → yellow → red)
# -------------------------------------------------------------------
def _color_from_value(v):
    """
    Returns a hex color for the bar based on the magnitude of v (0–1).
    0.0 = red, 0.5 = yellow, 1.0 = green
    """
    r = int((1 - v) * 255)
    g = int(v * 255)
    b = 60
    return f"rgb({r}, {g}, {b})"


# -------------------------------------------------------------------
# Enhanced SHAP-lite bar renderer with tooltip + gradient color
# -------------------------------------------------------------------
def _enhanced_bar(val, label, tooltip_text):
    """
    Creates a visually rich horizontal bar with tooltip support.
    """

    pct = int(val * 100)
    bar_width = int(val * 200)  # pixel width scaling
    color = _color_from_value(val)

    html = f"""
    <div style="margin-bottom:6px;">
        <div style="font-weight:600; margin-bottom:4px;">
            {label} — {pct}%
        </div>
        <div title="{tooltip_text}"
             style="
                height: 14px;
                width: 200px;
                background-color: #eee;
                border-radius: 8px;
                overflow: hidden;
                position: relative;"
        >
            <div style="
                height: 100%;
                width: {bar_width}px;
                background: {color};
                border-radius: 8px;">
            </div>
        </div>
    </div>
    """

    return html


# -------------------------------------------------------------------
# Main bet table
# -------------------------------------------------------------------
def render_bet_table(df):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        st.warning("No predictions available.")
        return

    # Required fields
    required_cols = [
        "player", "stat", "line",
        "cover_prob", "final_score", "explain_factors"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing required prediction columns: {missing}")
        return

    # -------------------------------
    # Display main table
    # -------------------------------
    df_main = df[["player", "stat", "line", "cover_prob", "final_score"]].copy()
    df_main["cover_prob"] = df_main["cover_prob"].round(3)
    df_main["final_score"] = df_main["final_score"].round(3)

    st.dataframe(df_main, hide_index=True, use_container_width=True)

    # -------------------------------
    # Explanation Section
    # -------------------------------
    st.markdown("### 🔎 Why These Bets Rank High")

    for _, row in df.iterrows():
        player = row["player"]
        stat = row["stat"].upper()
        
        explain = row["explain_factors"]

        with st.expander(f"📌 {player} — {stat} {row['line']}+"):
            st.markdown("#### SHAP-Lite Breakdown (Feature Influence)")

            bars = [
                ("📈 Cover Probability", explain.get("cover_prob", 0), "Likelihood model expects player to exceed the line"),
                ("⚔ Matchup Score", explain.get("matchup_score", 0), "Impact of opponent defense vs this stat"),
                ("🏃‍♂️ Pace", explain.get("pace", 0), "Expected game speed and extra possessions"),
                ("🔥 Usage Boost", explain.get("usage_boost", 0), "Projected minutes increase, injuries, or rotation changes"),
            ]

            # Render bars with HTML
            for label, val, tooltip in bars:
                st.markdown(_enhanced_bar(val, label, tooltip), unsafe_allow_html=True)

            st.divider()
