# square_api.py
import requests

def fetch_catalog(access_token: str, location_id: str) -> dict:
    """
    Returns dict {item_name_lower: price_float}
    """
    if not access_token:
        raise Exception("Square access token is required.")
    url = "https://connect.squareupsandbox.com/v2/catalog/list?types=ITEM"
    headers = {
        "Square-Version": "2023-09-20",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise Exception(f"Square API error ({resp.status_code}): {resp.text}")
    data = resp.json()
    items = data.get("objects", [])
    catalog = {}
    for obj in items:
        if obj.get("type") != "ITEM":
            continue
        item_data = obj.get("item_data", {})
        name = item_data.get("name", "").strip().lower()
        # try to read first variation price
        try:
            variation = item_data["variations"][0]["item_variation_data"]
            amount = variation["price_money"]["amount"]
            price = float(amount) / 100.0
            if name:
                catalog[name] = price
        except Exception:
            # skip items without price
            continue
    return catalog
