import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
from bs4 import BeautifulSoup

def scrape_top_100_game_ids():
    print("📡 Scraping Top 100 ranked games from BGG...")
    url = "https://boardgamegeek.com/browse/boardgame"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    game_ids = []
    for row in soup.select("tr[id^='row_']")[:100]:
        link = row.select_one("a.primary")
        href = link["href"]  # Example: /boardgame/174430/gloomhaven
        game_id = href.split("/")[2]
        game_ids.append(game_id)

    print(f"✅ Found {len(game_ids)} game IDs.")
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
    game_ids = scrape_top_100_game_ids()

    games = []
    for i, game_id in enumerate(game_ids):
        print(f"🔍 Fetching game {i+1}/100 - ID {game_id}")
        details = fetch_game_details(game_id)
        if details:
            games.append(details)
        time.sleep(2)  # Respect API rate limit

    df = pd.DataFrame(games)
    df.to_csv("top_100_bgg.csv", index=False)
    print("✅ Saved top 100 ranked games to 'top_100_bgg.csv'")

if __name__ == "__main__":
    main()
