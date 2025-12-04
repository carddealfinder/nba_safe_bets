import streamlit as st
from nba_safe_bets.utils.headshots import get_player_headshot_url


def render_player_card(row):
    """Renders a player card including headshot + bet info."""

    player = row["player"]
    player_id = row["player_id"]
    team = row.get("team", "N/A")
    stat = row["stat"]
    line = row["line"]
    prob = row["cover_prob"]
    dk = row.get("dk_odds", None)

    # -----------------------------------------------------
    # Fetch image
    # -----------------------------------------------------
    img_url = get_player_headshot_url(player_id, player)

    # -----------------------------------------------------
    # Layout — image on left, stats on right
    # -----------------------------------------------------
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(img_url, width=130)

    with col2:
        st.markdown(f"""
        ### **{player}** ({team})
        **Prop:** {stat} **{line}+**  
        **Cover Probability:** `{prob:.1%}`  
        {"**DraftKings:** " + str(dk) if dk else ""}
        """)

    st.markdown("---")
