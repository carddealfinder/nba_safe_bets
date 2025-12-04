import streamlit as st

def render_player_card(df):
    """
    Show a player's best stat. Avoids crashes when no data exists.
    """

    if df is None or df.empty:
        st.write("No stats available for this player.")
        return

    row = df.iloc[0]

    player = row.get("player", "Unknown Player")
    stat = row.get("stat", "N/A")
    prob = row.get("final_prob", "N/A")
    score = row.get("safety_score", "N/A")

    st.markdown(f"""
        ### {player}
        **Best Stat:** {stat}  
        **Probability:** {prob}  
        **Safety Score:** {score}
    """)
