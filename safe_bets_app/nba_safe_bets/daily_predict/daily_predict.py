from ..scrapers.balldontlie_players import get_player_list
from ..scrapers.schedule_scraper import get_daily_schedule
from ..scrapers.injury_report import get_injury_report
from ..scrapers.defense_rankings import get_defense_rankings
from ..scrapers.DraftKings_scraper import get_draftkings_odds

from .model_loader import load_models
from .safe_bet_ranker import rank_safe_bets

from ..processors.feature_builder import build_features
from ..processors.context_features import add_context_features


# --- Models & Ranking ---
from .model_loader import load_models
from .safe_bet_ranker import rank_safe_bets


def daily_predict():
    st.write("🔍 DEBUG: Starting Daily Prediction Engine")

    # 1. Load players
    players = get_player_list()
    st.write("Players DF Shape:", players.shape)

    if players.empty:
        st.write("❌ Player list empty — stopping")
        return pd.DataFrame()

    # 2. Load schedule
    schedule = get_daily_schedule()
    if isinstance(schedule, list):
        schedule = pd.DataFrame(schedule)

    st.write("Schedule DF Shape:", schedule.shape)

    # 3. Injuries
    injuries = get_injury_report()
    st.write("Injury DF Shape:", injuries.shape)

    # 4. Defense rankings
    defense = get_defense_rankings()
    st.write("Defense keys:", list(defense.columns))

    # 5. DraftKings odds
    dk = get_draftkings_odds()
    st.write("DraftKings DF Shape:", dk.shape)

    # 6. Load trained models
    models = load_models()
    st.write("Models Loaded:", list(models.keys()))

    if not models:
        st.write("❌ No models loaded — cannot continue")
        return pd.DataFrame()

    # 7. Merge everything into a feature table
    merged = players.copy()
    merged = merged.merge(schedule, on="team", how="left")
    merged = merged.merge(defense, on="team", how="left")

    # injuries (left merge on player id)
    if not injuries.empty:
        merged = merged.merge(injuries, on="id", how="left")

    # DK odds (merge on player name)
    if not dk.empty:
        merged = merged.merge(dk, on="player", how="left")

    # Sanity check
    st.write("Merged DF Shape:", merged.shape)

    # 8. Run ranker
    ranked = rank_safe_bets(merged, models)
    st.write("Final ranked DF Shape:", ranked.shape)

    return ranked
