import streamlit as st
import pandas as pd

# === Load Data ===
profiles_df = pd.read_csv("player_preference_profiles.csv")

# Choose game list
game_source = st.radio("🎲 Choose game source:", ["Owned Games", "Top 100 BGG", "Top 50 Hotness"])
game_file = "owned_games.csv" if game_source == "Owned Games" else "top_100_bgg.csv" if game_source == "Top 100 BGG" else "top_50_hotness_bgg.csv"
games_df = pd.read_csv(game_file)

# === Clean game data ===
for col in ["min_players", "max_players", "weight", "playing_time"]:
    if col in games_df.columns:
        games_df[col] = pd.to_numeric(games_df[col], errors="coerce")

# === Player selection ===
st.title("👥 Group Game Recommender")

available_players = profiles_df["Player"].tolist()
selected_players = st.multiselect("Select up to 10 players:", available_players, max_selections=10)

if not selected_players:
    st.warning("Please select at least one player.")
    st.stop()

# === Filters ===
st.sidebar.header("🔧 Game Filters")

min_players = st.sidebar.slider("Minimum players", 1, 10, 1)
max_players = st.sidebar.slider("Maximum players", 1, 20, 20)
min_weight, max_weight = st.sidebar.slider("Game weight (complexity)", 1.0, 5.0, (1.0, 5.0), step=0.1)
min_time, max_time = st.sidebar.slider("Play time (minutes)", 0, 300, (0, 300), step=15)

# === Build group profile ===
group_profiles = profiles_df[profiles_df["Player"].isin(selected_players)].drop(columns=["Player"])
group_avg = group_profiles.mean()

# === Score games ===
game_scores = []

for _, row in games_df.iterrows():
    name = row["name"]
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row.get("mechanics")) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row.get("categories")) else []
    attributes = [f"mechanic::{m}" for m in mechanics] + [f"category::{c}" for c in categories]

    score = sum(group_avg.get(attr, 0) for attr in attributes)
    reason = [attr.split("::")[1] for attr in attributes if group_avg.get(attr, 0) > 0]

    # Check filters
    if (
        row.get("min_players", 1) <= max_players and
        row.get("max_players", 20) >= min_players and
        row.get("weight", 3.0) >= min_weight and row.get("weight", 3.0) <= max_weight and
        row.get("playing_time", 60) >= min_time and row.get("playing_time", 60) <= max_time
    ):
        game_scores.append({
            "Game": name,
            "Score": score,
            "Reason": ", ".join(reason) if reason else "General fit",
            "Players": f"{row.get('min_players', '?')}–{row.get('max_players', '?')}",
            "Weight": row.get("weight", "?"),
            "Play Time": row.get("playing_time", "?")
        })

# === Display Top 5 ===
st.subheader(f"🏆 Top 5 Recommended Games for {', '.join(selected_players)}")

top5 = sorted(game_scores, key=lambda x: x["Score"], reverse=True)[:5]

if not top5:
    st.warning("No games match the current filter and preferences.")
else:
    for i, game in enumerate(top5, 1):
        st.markdown(f"### {i}. 🎮 {game['Game']} — Score: `{game['Score']:.1f}`")
        st.markdown(f"- 👥 Players: {game['Players']}")
        st.markdown(f"- 🧠 Weight: {game['Weight']}")
        st.markdown(f"- ⏱️ Play Time: {game['Play Time']} mins")
        st.markdown(f"- 🎯 Why: {game['Reason']}")
        st.markdown("---")
