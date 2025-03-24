import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Load the data ===
profiles_df = pd.read_csv("player_preference_profiles.csv")
games_df = pd.read_csv("top_100_bgg.csv")

# === 2. Prepare game attribute map ===
game_attrs = {}
for _, row in games_df.iterrows():
    game = row["name"]
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row["mechanics"]) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row["categories"]) else []
    attributes = [f"mechanic::{m}" for m in mechanics] + [f"category::{c}" for c in categories]
    game_attrs[game] = attributes

# === 3. Calculate recommendation score for each player and game ===
recommendations = []

for _, profile in profiles_df.iterrows():
    player = profile["Player"]
    for game, attrs in game_attrs.items():
        score = sum(profile.get(attr, 0) for attr in attrs)
        recommendations.append({
            "Player": player,
            "Game": game,
            "Score": score
        })

rec_df = pd.DataFrame(recommendations)

# === 4. Pivot to matrix ===
matrix = rec_df.pivot(index="Player", columns="Game", values="Score").fillna(0)

# === 5. Save to CSV ===
matrix.to_csv("top_100_recommendation_matrix.csv")
print("✅ Saved to 'top_100_recommendation_matrix.csv'")

# === 6. Plot Heatmap ===
plt.figure(figsize=(max(12, len(matrix.columns) * 0.3), max(6, len(matrix) * 0.6)))
sns.heatmap(matrix, cmap="YlGnBu", annot=False, linewidths=0.5)
plt.title("🎲 Top 100 BGG Game Recommendations")
plt.xlabel("Games")
plt.ylabel("Players")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("top_100_recommendation_heatmap.png")
plt.show()
