import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

def fetch_top_100_game_ids():
    print("📡 Fetching Top 100 board games from BGG...")
    response = requests.get("https://boardgamegeek.com/xmlapi2/hot?type=boardgame")
    root = ET.fromstring(response.content)

    game_ids = []
    for item in root.findall("item"):
        game_id = item.attrib.get("id")
        if game_id:
            game_ids.append(game_id)
        if len(game_ids) >= 100:
            break
    return game_ids

def fetch_game_details(game_id):
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error fetching game {game_id}")
        return None

    root = ET.fromstring(response.content)

    name_element = root.find(".//name[@type='primary']")
    min_players_element = root.find(".//minplayers")
    max_players_element = root.find(".//maxplayers")
    avg_rating_element = root.find(".//statistics//ratings//average")
    rank_element = root.find(".//statistics//ratings//ranks//rank[@name='boardgame']")
    weight_element = root.find(".//statistics//ratings//averageweight")
    thumbnail_element = root.find(".//thumbnail")

    categories = [cat.attrib["value"] for cat in root.findall(".//link[@type='boardgamecategory']")]
    mechanics = [mech.attrib["value"] for mech in root.findall(".//link[@type='boardgamemechanic']")]

    if name_element is None:
        return None

    return {
        "id": game_id,
        "name": name_element.attrib["value"],
        "min_players": min_players_element.attrib["value"] if min_players_element is not None else "N/A",
        "max_players": max_players_element.attrib["value"] if max_players_element is not None else "N/A",
        "avg_rating": avg_rating_element.attrib["value"] if avg_rating_element is not None else "N/A",
        "ranking": rank_element.attrib["value"] if rank_element is not None else "N/A",
        "weight": weight_element.attrib["value"] if weight_element is not None else "N/A",
        "categories": ", ".join(categories) if categories else "N/A",
        "mechanics": ", ".join(mechanics) if mechanics else "N/A",
        "thumbnail": thumbnail_element.text if thumbnail_element is not None else ""
    }

def main():
    game_ids = fetch_top_100_game_ids()
    print(f"✅ Found {len(game_ids)} games. Now fetching details...")

    games = []
    for i, game_id in enumerate(game_ids):
        print(f"🔍 Fetching game {i+1}/{len(game_ids)} - ID {game_id}")
        details = fetch_game_details(game_id)
        if details:
            games.append(details)
        time.sleep(2)  # BGG rate limit

    df = pd.DataFrame(games)
    df.to_csv("top_100_bgg.csv", index=False)
    print("✅ Saved top 100 games to 'top_100_bgg.csv'")

if __name__ == "__main__":
    main()
