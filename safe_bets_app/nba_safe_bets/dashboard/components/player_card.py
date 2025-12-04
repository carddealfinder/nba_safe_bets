import streamlit as st

def render_player_card(df):
    stat = df.iloc[0]["stat"]
    line = df.iloc[0]["line"]

    ml = df.iloc[0]["ml_prob"]
    weighted = df.iloc[0]["weighted_prob"]
    finalp = df.iloc[0]["final_prob"]
    score = df.iloc[0]["safety_score"]

    st.markdown(f"""
    ### Player ID: `{df.iloc[0]['player']}`

    **Prop Line:** {stat.upper()} {line}+  
    **Final Probability:** {finalp:.3f}  
    **ML Probability:** {ml:.3f}  
    **Weighted Probability:** {weighted:.3f}  
    **Safety Score:** {score:.1f}  

    ---
    """)
