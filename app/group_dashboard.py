import streamlit as st
import pandas as pd

# === Setup ===
st.set_page_config(page_title="Group Game Recommender", layout="wide")
st.title("🎲 Group Board Game Recommender")

# === Load Data ===
pred_df = pd.read_csv("data/player_game_prediction_matrix.csv", index_col="Player")
surveyed_games = pd.read_csv("data/surveyed_games.csv")

# === Clean up column names ===
surveyed_games["name"] = surveyed_games["name"].astype(str).str.strip()

# === Player Selection ===
players = pred_df.index.tolist()
selected_players = st.multiselect("👥 Select 1 to 10 players", players, max_selections=10)

if not selected_players:
    st.warning("Please select at least one player.")
    st.stop()

group_size = len(selected_players)
st.markdown(f"🔢 Group size: **{group_size} players**")

# === Filter games by group size support ===
surveyed_games["min_players"] = pd.to_numeric(surveyed_games["min_players"], errors="coerce")
surveyed_games["max_players"] = pd.to_numeric(surveyed_games["max_players"], errors="coerce")
surveyed_games = surveyed_games.dropna(subset=["min_players", "max_players"])

valid_games = surveyed_games[
    (surveyed_games["min_players"] <= group_size) &
    (surveyed_games["max_players"] >= group_size)
].copy()

# === Check which games exist in prediction matrix ===
valid_game_names = [name for name in valid_games["name"] if name in pred_df.columns]

if not valid_game_names:
    st.warning("❌ No games match your group size and have enough data.")
    st.stop()

# === Get prediction scores for selected players and valid games ===
group_preds = pred_df.loc[selected_players, valid_game_names]
avg_scores = group_preds.mean().rename("score").reset_index()
avg_scores.rename(columns={"index": "name"}, inplace=True)
avg_scores["name"] = avg_scores["name"].astype(str)

# === Merge predicted scores with game info ===
valid_games["name"] = valid_games["name"].astype(str)
result = pd.merge(valid_games, avg_scores, on="name", how="inner")

# === Show Top 10 Recommendations ===
top10 = result.sort_values(by="score", ascending=False).head(10)

st.subheader(f"🏆 Top 10 Game Recommendations for Group: {', '.join(selected_players)}")

if top10.empty:
    st.warning("No games found after filtering.")
else:
    for _, row in top10.iterrows():
        st.markdown(f"### 🎮 {row['name']} — Avg Predicted Score: `{row['score']:.2f}`")
        st.markdown(f"- 👥 Players: {int(row['min_players'])}–{int(row['max_players'])}")
        st.markdown(f"- 🧠 Weight: {row.get('weight', '?')}")
        st.markdown("- 🤝 Based on similar players' predicted enjoyment.")
        st.markdown("---")
