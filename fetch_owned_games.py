print("✅ Script started!")

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

# Load your owned games CSV
collection_file = "dex_collection.csv"
df = pd.read_csv(collection_file)

# Ensure 'objectid' column exists (this holds game IDs)
if "objectid" not in df.columns or "objectname" not in df.columns:
    print("❌ ERROR: Required columns ('objectid' or 'objectname') not found in CSV!")
    exit()

# Extract game IDs and names
game_ids = df["objectid"].tolist()
game_names = df["objectname"].tolist()

def get_board_game(game_id, game_name, index, total):
    """Fetch board game details from BoardGameGeek API with progress updates"""
    print(f"🔄 [{index}/{total}] Fetching: {game_name} (ID: {game_id})...")

    url = f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error fetching game {game_name} (ID: {game_id})")
        return None

    root = ET.fromstring(response.content)

    name_element = root.find(".//name[@type='primary']")
    min_players_element = root.find(".//minplayers")
    max_players_element = root.find(".//maxplayers")
    avg_rating_element = root.find(".//statistics//ratings//average")
    rank_element = root.find(".//statistics//ratings//ranks//rank[@name='boardgame']")
    weight_element = root.find(".//statistics//ratings//averageweight")

    categories = [cat.attrib["value"] for cat in root.findall(".//link[@type='boardgamecategory']")]
    mechanics = [mech.attrib["value"] for mech in root.findall(".//link[@type='boardgamemechanic']")]

    # Ensure essential elements exist
    if name_element is None or min_players_element is None or max_players_element is None:
        print(f"⚠️ Warning: Missing data for {game_name} (ID: {game_id})")
        return None

    return {
        "id": game_id,
        "name": name_element.attrib["value"],
        "min_players": min_players_element.attrib["value"],
        "max_players": max_players_element.attrib["value"],
        "avg_rating": avg_rating_element.attrib["value"] if avg_rating_element is not None else "N/A",
        "ranking": rank_element.attrib["value"] if rank_element is not None else "N/A",
        "weight": weight_element.attrib["value"] if weight_element is not None else "N/A",
        "categories": ", ".join(categories) if categories else "N/A",
        "mechanics": ", ".join(mechanics) if mechanics else "N/A"
    }

# Fetch data for all owned games with progress tracking
games_data = []
total_games = len(game_ids)

for index, (game_id, game_name) in enumerate(zip(game_ids, game_names), start=1):
    game_info = get_board_game(game_id, game_name, index, total_games)
    if game_info:
        games_data.append(game_info)
    time.sleep(2)  # Prevent hitting API too fast

# Save the final dataset
df_games = pd.DataFrame(games_data)
df_games.to_csv("owned_games.csv", index=False)

print("\n✅ Done! Board game data saved to owned_games.csv!")
