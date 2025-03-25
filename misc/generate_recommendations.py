import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Load the data ===
profiles = pd.read_csv("player_preference_profiles.csv")
owned = pd.read_csv("owned_games.csv")
responses = pd.read_csv("player_responses.csv")

# === 2. Prepare data ===
# Extract game name + attributes (mechanics + categories)
game_attrs = {}
for _, row in owned.iterrows():
    game_name = row["name"]
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row["mechanics"]) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row["categories"]) else []
    tags = [f"mechanic::{m}" for m in mechanics] + [f"category::{c}" for c in categories]
    game_attrs[game_name] = tags

# === 3. Get list of players and games they've rated ===
player_rated_games = {}
for _, row in responses.iterrows():
    name = row["Your name"]
    rated = row.drop("Your name").dropna().to_dict()
    player_rated_games[name] = set(g for g, val in rated.items() if val not in ["Haven't played yet", ""])

# === 4. Compute recommendation scores ===
recommendation_data = []

for _, profile in profiles.iterrows():
    player = profile["Player"]
    for game, attrs in game_attrs.items():
        if game in player_rated_games.get(player, set()):
            continue  # skip games already played

        score = sum([profile.get(attr, 0) for attr in attrs])
        recommendation_data.append({
            "Player": player,
            "Game": game,
            "Score": score
        })

rec_df = pd.DataFrame(recommendation_data)

# === 5. Create pivot table ===
pivot = rec_df.pivot(index="Player", columns="Game", values="Score").fillna(0)

# === 6. Save to CSV ===
pivot.to_csv("game_recommendation_matrix.csv")
print("✅ Saved game recommendation matrix to 'game_recommendation_matrix.csv'")

# === 7. Plot heatmap ===
plt.figure(figsize=(max(12, len(pivot.columns) * 0.3), max(6, len(pivot) * 0.6)))
sns.heatmap(pivot, annot=False, cmap="YlGnBu", linewidths=0.5)
plt.title("🎲 Game Recommendation Heatmap")
plt.xlabel("Games")
plt.ylabel("Players")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("game_recommendation_heatmap.png")
plt.show()
