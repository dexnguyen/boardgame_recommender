import os
import re
from io import BytesIO

import polars as pl
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def sanitize_filename(filename: str) -> str:
    # Replace any characters that are not allowed in file names
    return re.sub(r'[<>:"/\\|?*]', "", filename)


def search_and_save_thumbnail(
    driver: webdriver.Chrome, game_name: str, game_id: str
) -> None:
    # Open the BoardGameGeek website
    driver.get(f"https://boardgamegeek.com/boardgame/{game_id}/{game_name}")

    # Wait for the search results to load and display the results
    wait = WebDriverWait(driver, 10)
    first_result = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@ng-href, '/image/')]/img")
        )
    )
    first_result.click()

    enlarged_image = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//img[contains(@class, 'tw-cursor-zoom-in')]")
        )
    )
    enlarged_image.click()

    # Click once more to reach the final enlarged state
    final_enlarged_image = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//img[contains(@class, 'img-modal-img')]")
        )
    )
    fit_to_screen_image_url = final_enlarged_image.get_attribute("src")

    # Download the image
    response = requests.get(fit_to_screen_image_url)
    image = Image.open(BytesIO(response.content))
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Save the image as a JPG
    sanitized_game_name = sanitize_filename(game_name)
    image_path = os.path.join("data", f"{sanitized_game_name}_thumbnail.jpg")
    image.save(image_path, "JPEG")

    print(f"Final enlarged thumbnail saved as {image_path}")


def main() -> None:
    df = pl.read_csv("collection (1).csv")
    service = Service()
    driver = webdriver.Chrome(service=service)

    for game_name, game_id in df.select("objectname", "objectid").rows():
        try:
            search_and_save_thumbnail(driver, game_name, game_id)
        except Exception as e:
            print(f"Error processing {game_name} with ID {game_id}: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
