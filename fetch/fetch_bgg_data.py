import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time  # Add this to prevent API rate limits

def get_board_game(game_id):
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching game {game_id}")
        return None

    # Print part of the API response to debug
    print(f"\n=== Debugging Game ID {game_id} ===")
    print("Response Content (First 1000 chars):")
    print(response.text[:1000])  # Print first 1000 characters to check structure

    # Parse XML
    root = ET.fromstring(response.content)

    name_element = root.find(".//name[@type='primary']")
    min_players_element = root.find(".//minplayers")
    max_players_element = root.find(".//maxplayers")
    
    avg_rating_element = root.find(".//statistics//ratings//average")
    rank_element = root.find(".//statistics//ratings//ranks//rank[@name='boardgame']")
    weight_element = root.find(".//statistics//ratings//averageweight")

    categories = [cat.attrib["value"] for cat in root.findall(".//link[@type='boardgamecategory']")]
    mechanics = [mech.attrib["value"] for mech in root.findall(".//link[@type='boardgamemechanic']")]

    # Check if essential elements exist
    if name_element is None or min_players_element is None or max_players_element is None:
        print(f"❌ Missing data for game {game_id}")
        return None

    return {
        "name": name_element.attrib["value"],
        "min_players": min_players_element.attrib["value"],
        "max_players": max_players_element.attrib["value"],
        "avg_rating": avg_rating_element.attrib["value"] if avg_rating_element is not None else "N/A",
        "ranking": rank_element.attrib["value"] if rank_element is not None else "N/A",
        "weight": weight_element.attrib["value"] if weight_element is not None else "N/A",
        "categories": ", ".join(categories) if categories else "N/A",
        "mechanics": ", ".join(mechanics) if mechanics else "N/A"
    }

# List of game IDs to fetch
game_ids = [13, 174430, 822, 31260, 68448]  # Catan, Gloomhaven, Dominion, 7 Wonders, Pandemic

# Fetch data for all games with delay to avoid API rate limits
games_data = []
for game_id in game_ids:
    game_info = get_board_game(game_id)
    if game_info:
        games_data.append(game_info)
    time.sleep(2)  # Prevent hitting API too fast

# Convert to a DataFrame and save to CSV
df = pd.DataFrame(games_data)
df.to_csv("boardgames.csv", index=False)

print("\n✅ Board game data saved to boardgames.csv!")
