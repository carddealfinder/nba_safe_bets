import streamlit as st
import matplotlib.pyplot as plt


def render_player_charts(row):
    """
    Render charts for a single prediction row.
    Supports:
      - Projected vs Line bar chart
      - Cover probability gauge bar
    """

    if row is None or (not isinstance(row, dict) and not hasattr(row, "get")):
        st.error("Invalid row passed to player charts.")
        return

    # Extract fields safely
    player = row.get("player_name", "Unknown Player")
    stat = row.get("stat", "?").upper()
    line = row.get("line", None)
    proj = row.get("model_pred", None)
    prob = row.get("cover_prob", None)

    # Only plot if numbers exist
    if not isinstance(proj, (float, int)) or not isinstance(line, (float, int)):
        st.warning("No projection/line data available for chart.")
        return

    # ---------------------------------------
    # Chart 1 — Projection vs Line
    # ---------------------------------------
    st.subheader(f"{stat}: Projection vs Line")

    fig, ax = plt.subplots(figsize=(5, 3))
    x = ["Projection", "Line"]
    y = [proj, line]

    ax.bar(x, y)
    ax.set_title(f"{player} — {stat}")
    ax.set_ylabel("Value")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)

    # ---------------------------------------
    # Chart 2 — Cover Probability Gauge Bar
    # ---------------------------------------
    st.subheader("Probability of Covering Line")

    if isinstance(prob, (float, int)):
        prob_pct = prob * 100
    else:
        prob_pct = None

    if prob_pct is None:
        st.info("No cover probability available.")
        return

    fig2, ax2 = plt.subplots(figsize=(5, 1.2))

    ax2.barh([""], [prob_pct])
    ax2.set_xlim(0, 100)
    ax2.set_title(f"{prob_pct:.1f}% Chance to Cover")

    # Remove ticks
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Light grid
    ax2.grid(axis="x", linestyle="--", alpha=0.3)

    st.pyplot(fig2)
