import requests, time

BRANDS = {
    'Stone Island': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=73306', 'Webhook Indsættes her'),
    'Ralph Lauren': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=88,4273,430791', 'Webhook Indsættes her'),
    'Nike X Patta': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=6081602', 'Webhook Indsættes her'),
    'CP Company': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=73952', 'Webhook Indsættes her'),
    'Ami Paris': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=7228770', 'Webhook Indsættes her'),
    'Arcteryx': ('https://www.vinted.dk/api/v2/catalog/items?page=1&per_page=96&order=newest_first&brand_ids=319730', 'Webhook Indsættes her')
}

def fetch_items(url):
    return requests.get(url).json().get("items", []) if requests.Session().get('https://www.vinted.dk').status_code == 200 else []

def send_to_discord(item, brand, webhook):
    payload = {
        "embeds": [{
            "title": f"🧥 {brand}: {item['title']}",
            "url": item['url'],
            "color": 0x90EE90,
            "fields": [
                {"name": "💸 Pris", "value": f"{item['price']['amount']} {item['price']['currency_code']}", "inline": True},
                {"name": "📦 Levering", "value": item.get('service_fee', 'Ikke angivet'), "inline": True},
                {"name": "👤 Sælger", "value": item['user']['login']},
                {"name": "❤️ Favorites", "value": str(item.get('favourite_count', 0)), "inline": True},
                {"name": "📦 Tilstand", "value": item['status'], "inline": True},
                {"name": "📏 Størrelse", "value": item['size_title']}
            ],
            "image": {"url": item['photo']['url']}
        }]
    }
    requests.post(webhook, json=payload, headers={"Content-Type": "application/json"})

def monitor():
    last_seen = {}
    while True:
        for brand, (url, webhook) in BRANDS.items():
            items = fetch_items(url)
            if items and (latest := items[0]['id']) != last_seen.get(brand):
                send_to_discord(items[0], brand, webhook)
                last_seen[brand] = latest
        time.sleep(20)

if __name__ == "__main__": monitor()
