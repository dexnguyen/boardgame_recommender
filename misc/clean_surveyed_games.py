import pandas as pd

# Load files
owned_games = pd.read_csv("../data/owned_games.csv")
player_responses = pd.read_csv("../data/player_responses.csv")

# Rename objectname to name if needed
if "objectname" in owned_games.columns and "name" not in owned_games.columns:
    owned_games.rename(columns={"objectname": "name"}, inplace=True)

# Extract all game names from player_responses columns
game_names_from_responses = player_responses.columns.tolist()
game_names_from_responses = game_names_from_responses[1:]  # Skip 'Your name' column

# Strip and match game names
owned_games["name"] = owned_games["name"].str.strip()
surveyed_games = owned_games[owned_games["name"].isin(game_names_from_responses)].copy()

# Save to new file
surveyed_games.to_csv("../data/surveyed_games.csv", index=False)
print(f"✅ Saved {len(surveyed_games)} surveyed games to '../data/surveyed_games.csv'")
