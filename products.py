"""
Grandcru Grapes — WooCommerce productenlijst
"""
import requests

WP_USER = "jannes_v36jq7op"
WP_PASS = "yN7I hBQQ 0vzZ 7jSw a6rS ByBy"
BASE_URL = "https://grandcrugrapes.com/wp-json/wc/v3"

def fetch_all_products():
    products = []
    page = 1
    while True:
        r = requests.get(
            f"{BASE_URL}/products",
            auth=(WP_USER, WP_PASS),
            params={"per_page": 100, "page": page, "orderby": "name", "order": "asc"},
            timeout=30,
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        products.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return products

def main():
    products = fetch_all_products()
    print(f"Totaal: {len(products)} producten\n")
    print(f"{'ID':<8} {'Status':<12} {'Prijs':<10} Naam")
    print("─" * 60)
    for p in products:
        pid    = p.get("id", "")
        name   = p.get("name", "")
        status = p.get("status", "")
        price  = p.get("price", "")
        print(f"{pid:<8} {status:<12} €{price:<9} {name}")

if __name__ == "__main__":
    main()
