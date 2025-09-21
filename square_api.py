import os
import requests
from dotenv import load_dotenv

load_dotenv()

SQUARE_SANDBOX_TOKEN = os.getenv("SQUARE_SANDBOX_TOKEN")
SQUARE_LOCATION_ID = os.getenv("SQUARE_LOCATION_ID")

def fetch_catalog():
    url = f"https://connect.squareupsandbox.com/v2/catalog/list"
    headers = {
        "Authorization": f"Bearer {SQUARE_SANDBOX_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    catalog_items = {}

    if response.status_code == 200:
        data = response.json()
        for item in data.get("objects", []):
            if item["type"] == "ITEM":
                name = item["item_data"]["name"].lower()
                price = item["item_data"]["variations"][0]["item_variation_data"]["price_money"]["amount"] / 100
                catalog_items[name] = price
    else:
        print("Error fetching catalog:", response.text)

    return catalog_items
