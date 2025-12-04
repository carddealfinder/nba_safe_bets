import streamlit as st
import pandas as pd


def render_charts(player_row: pd.Series):
    """
    Display prediction bars (model probability, final probability, weighted score)
    using matplotlib rendered inside Streamlit.
    """

    # Lazy import matplotlib ONLY inside the function
    # (prevents Streamlit Cloud load-time import errors)
    import matplotlib.pyplot as plt

    # ----- Validate input -----
    if player_row is None or not isinstance(player_row, pd.Series):
        st.warning("No player data available for chart rendering.")
        return

    # Extract fields safely
    player_name = player_row.get("player", "Unknown Player")
    stat = player_row.get("stat", "stat")
    line = player_row.get("line", None)

    ml_prob = float(player_row.get("ml_prob", 0))
    final_prob = float(player_row.get("final_prob", 0))
    weighted_prob = float(player_row.get("weighted_prob", 0))

    labels = ["Model Prob", "Final Prob", "Weighted Prob"]
    values = [ml_prob, final_prob, weighted_prob]

    # ----- Create Chart -----
    fig, ax = plt.subplots(figsize=(6, 3.5))

    bars = ax.bar(labels, values)

    # Add tooltips/value labels
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.01,
            f"{val:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="black"
        )

    ax.set_ylim(0, 1)  # probabilities 0–1
    ax.set_ylabel("Probability Score")
    ax.set_title(f"{player_name} — {stat} Line: {line}")

    st.pyplot(fig)
