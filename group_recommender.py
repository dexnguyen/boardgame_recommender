import pandas as pd

# === 1. Load data ===
profiles = pd.read_csv("player_preference_profiles.csv")

# Ask user which game list to use
print("🎲 Choose game source:")
print("1. Owned Games (owned_games.csv)")
print("2. Top 100 BGG Games (top_100_bgg.csv)")
source = input("Enter 1 or 2: ").strip()

game_file = "owned_games.csv" if source == "1" else "top_100_bgg.csv"
games_df = pd.read_csv(game_file)

# List available players
print("\n👥 Available players:")
player_list = profiles["Player"].tolist()
for i, name in enumerate(player_list):
    print(f"{i+1}. {name}")

selected_indices = input("\nSelect players by numbers (comma-separated, max 10): ")
indices = [int(i.strip()) - 1 for i in selected_indices.split(",") if i.strip().isdigit()]
selected_players = [player_list[i] for i in indices[:10]]

print(f"\n✅ Selected players: {', '.join(selected_players)}")

# === 2. Create group profile (average of selected players) ===
group_profile = profiles[profiles["Player"].isin(selected_players)].drop(columns=["Player"])
group_scores = group_profile.mean()

# === 3. Build game attribute map ===
game_attrs = {}
for _, row in games_df.iterrows():
    name = row["name"]
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row["mechanics"]) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row["categories"]) else []
    attributes = [f"mechanic::{m}" for m in mechanics] + [f"category::{c}" for c in categories]
    game_attrs[name] = attributes

# === 4. Score each game ===
recommendations = []

for game, attrs in game_attrs.items():
    score = sum(group_scores.get(attr, 0) for attr in attrs)
    matching = [attr.replace("mechanic::", "").replace("category::", "") 
                for attr in attrs if group_scores.get(attr, 0) > 0]
    recommendations.append({
        "Game": game,
        "Score": score,
        "Reason": ", ".join(matching) if matching else "General fit"
    })

# === 5. Sort and show top 5 ===
top5 = sorted(recommendations, key=lambda x: x["Score"], reverse=True)[:5]

print("\n🏆 Top 5 Game Recommendations for the Group:\n")
for i, rec in enumerate(top5, 1):
    print(f"{i}. {rec['Game']} — Score: {rec['Score']:.2f}")
    print(f"   🎯 Why: Matches group interest in: {rec['Reason']}\n")

# Optional: Save to CSV
pd.DataFrame(top5).to_csv("group_top_5_recommendations.csv", index=False)
print("📄 Saved to group_top_5_recommendations.csv")
