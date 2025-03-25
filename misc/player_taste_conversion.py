import pandas as pd
from collections import defaultdict

# === CONFIGURATION ===
RESPONSES_FILE = "../data/player_responses.csv"
OWNED_GAMES_FILE = "../data/owned_games.csv"
OUTPUT_FILE = "../data/player_preference_profiles.csv"

# === 1. Load data ===
responses_df = pd.read_csv(RESPONSES_FILE)
games_df = pd.read_csv(OWNED_GAMES_FILE)

# === 2. Rating conversion map ===
rating_map = {
    "Hate it! Wouldn't play again.": -2,
    "Don't like it.": -1,
    "It's okay": 0,
    "Like it! Can play again": 1,
    "Love it! Want to play again.": 2,
    "Haven't played yet": 0
}

# === 3. Unpivot response table ===
melted_df = responses_df.melt(id_vars=["Your name"], var_name="Game Name", value_name="Rating")
melted_df["Score"] = melted_df["Rating"].map(rating_map)

# === 4. Merge with owned games (match Game Name to name) ===
merged = melted_df.merge(games_df, left_on="Game Name", right_on="name", how="inner")

# === 5. Tally scores per player per mechanic/category ===
player_profiles = defaultdict(lambda: defaultdict(int))

for _, row in merged.iterrows():
    player = row["Your name"]
    score = row["Score"]
    
    if pd.isna(score):
        continue

    # Split mechanics/categories
    mechanics = str(row["mechanics"]).split(", ") if pd.notna(row["mechanics"]) else []
    categories = str(row["categories"]).split(", ") if pd.notna(row["categories"]) else []

    for mech in mechanics:
        player_profiles[player][f"mechanic::{mech}"] += score
    for cat in categories:
        player_profiles[player][f"category::{cat}"] += score

# === 6. Convert profiles into DataFrame ===
all_attrs = sorted(set(attr for profile in player_profiles.values() for attr in profile))
rows = []

for player, profile in player_profiles.items():
    row = {"Player": player}
    for attr in all_attrs:
        row[attr] = profile.get(attr, 0)
    rows.append(row)

profile_df = pd.DataFrame(rows)
profile_df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Done! Player preference profiles saved to: {OUTPUT_FILE}")
