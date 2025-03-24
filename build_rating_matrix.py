import pandas as pd

# === 1. Load responses ===
df = pd.read_csv("player_responses.csv")

# === 2. Remove timestamp if it exists ===
if "Timestamp" in df.columns:
    df = df.drop(columns=["Timestamp"])

# === 3. Define rating conversion ===
rating_map = {
    "Love it! Want to play again.": 2,
    "Like it! Can play again": 1,
    "It's okay": 0,
    "Don't like it.": -1,
    "Hate it! Wouldn't play again.": -2,
    "Haven't played yet": None
}

# === 4. Convert game columns ===
converted = df.copy()
game_columns = [col for col in df.columns if col != "Your name"]

for col in game_columns:
    converted[col] = converted[col].map(rating_map)

# === 5. Set player names as index ===
converted = converted.rename(columns={"Your name": "Player"})
converted.set_index("Player", inplace=True)

# === 6. Save output ===
converted.to_csv("player_game_rating_matrix.csv")
print("✅ Cleaned rating matrix saved as 'player_game_rating_matrix.csv'")
