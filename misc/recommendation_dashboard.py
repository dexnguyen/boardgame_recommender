import streamlit as st
import pandas as pd

# === Setup ===
st.set_page_config(page_title="Group Board Game Recommender", layout="wide")
st.title("🎲 Group Board Game Recommender (Collaborative Filtering)")

# === Load prediction matrix ===
pred_df = pd.read_csv("player_game_prediction_matrix.csv", index_col="Player")

# === Game source toggle ===
game_source = st.radio("🗂 Choose game list:", ["Top 100 BGG", "Owned Games", "Top 50 Hotness BGG"])

if game_source == "Top 100 BGG":
    game_df = pd.read_csv("top_100_bgg.csv")
elif game_source == "Owned Games":
    game_df = pd.read_csv("owned_games.csv")
else:
    game_df = pd.read_csv("top_50_hotness_bgg.csv")

# Normalize game names
available_games = set(game_df["name"].str.strip())

# === Player selection ===
players = pred_df.index.tolist()
selected_players = st.multiselect("👥 Select up to 10 players:", players, max_selections=10)

if not selected_players:
    st.warning("Please select at least one player.")
    st.stop()

# === Filters ===
st.sidebar.header("🔎 Game Filters")

weight_min, weight_max = st.sidebar.slider("🧠 Game Weight (Complexity)", 1.0, 5.0, (1.0, 5.0), step=0.1)
min_players_filter = st.sidebar.slider("👥 Min Player Count", 1, 10, (1, 10))
max_players_filter = st.sidebar.slider("👥 Max Player Count", 1, 10, (1, 10))

# === Calculate group predictions ===
group_preds = pred_df.loc[selected_players]
avg_scores = group_preds.mean().sort_values(ascending=False)
filtered_scores = avg_scores[avg_scores.index.isin(available_games)]

# Merge game data
merged = pd.DataFrame({"name": filtered_scores.index, "score": filtered_scores.values})
merged = merged.merge(game_df, on="name", how="left")

# Apply filters
filtered = merged[
    (merged["weight"].astype(float).between(weight_min, weight_max, inclusive="both")) &
    (merged["min_players"].astype(int).between(min_players_filter[0], min_players_filter[1], inclusive="both")) &
    (merged["max_players"].astype(int).between(max_players_filter[0], max_players_filter[1], inclusive="both"))
]

# === Show Top 5 ===
top5 = filtered.sort_values(by="score", ascending=False).head(5)

st.subheader(f"🎯 Top 5 Games Recommended for Group: {', '.join(selected_players)}")

if top5.empty:
    st.warning("No games match your filter criteria.")
else:
    for _, row in top5.iterrows():
        st.markdown(f"### 🎮 {row['name']} — Avg Predicted Score: `{row['score']:.2f}`")
        st.markdown(f"- 👥 Players: {row['min_players']}–{row['max_players']}")
        st.markdown(f"- 🧠 Weight: {row['weight']}")
        st.markdown("- 🤝 Recommended based on your group's predicted enjoyment.")
        st.markdown("---")
