import streamlit as st
import pandas as pd

# === Load Data ===
top5_df = pd.read_csv("top_5_recommendations.csv")
game_data = pd.read_csv("top_100_bgg.csv")
profiles = pd.read_csv("player_preference_profiles.csv")

# === Prepare Attribute Map ===
game_attr_map = {}
for _, row in game_data.iterrows():
    game = row["name"]
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row["mechanics"]) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row["categories"]) else []
    game_attr_map[game] = mechanics + categories

# === Streamlit UI ===
st.set_page_config(page_title="Board Game Recommender", layout="wide")
st.title("🎲 Personalized Board Game Recommender")

player_names = top5_df["Player"].unique()
selected_player = st.selectbox("Choose a player", player_names)

st.subheader(f"Top 5 Recommendations for {selected_player}")

# === Display Top 5 with Reasoning ===
for _, row in top5_df[top5_df["Player"] == selected_player].sort_values(by="Score", ascending=False).iterrows():
    game = row["Game"]
    score = row["Score"]
    st.markdown(f"### 🎮 {game} — Score: `{score}`")

    attributes = game_attr_map.get(game, [])
    matching_attrs = []

    for attr in attributes:
        mechanic_key = f"mechanic::{attr}"
        category_key = f"category::{attr}"
        score_mech = profiles.loc[profiles["Player"] == selected_player, mechanic_key].values[0] if mechanic_key in profiles.columns else 0
        score_cat = profiles.loc[profiles["Player"] == selected_player, category_key].values[0] if category_key in profiles.columns else 0
        if score_mech > 0:
            matching_attrs.append(f"❤️ Mechanic: {attr} (+{score_mech})")
        if score_cat > 0:
            matching_attrs.append(f"❤️ Category: {attr} (+{score_cat})")

    if matching_attrs:
        st.markdown("**Why this game?**")
        for reason in matching_attrs:
            st.markdown(f"- {reason}")
    else:
        st.markdown("_No strong preference match, but still recommended!_")

    st.markdown("---")
