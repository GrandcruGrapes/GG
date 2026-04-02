"""
Grandcru Grapes — Maak een WordPress pagina aan via de REST API.
Gebruik: python create_post.py
"""
import requests

WP_USER = "jannes_v36jq7op"
WP_PASS = "yN7I hBQQ 0vzZ 7jSw a6rS ByBy"
API_URL = "https://grandcrugrapes.com/wp-json/wp/v2/pages"

POST = {
    "title": "Bourgogne",
    "status": "draft",
    "content": "Bourgogne is een van de meest gerespecteerde wijnregio's ter wereld, bekend om zijn uitzonderlijke Pinot Noir en Chardonnay. De regio is opgedeeld in vijf hoofdgebieden: Chablis, Cote de Nuits, Cote de Beaune, Cote Chalonnaise en Maconnais. Elk gebied heeft zijn eigen karakter, maar deelt dezelfde toewijding aan terroir en ambacht.",
}

def main():
    r = requests.post(API_URL, auth=(WP_USER, WP_PASS), json=POST, timeout=30)
    if r.status_code in (200, 201):
        data = r.json()
        print(f"Pagina aangemaakt!")
        print(f"  ID:     {data['id']}")
        print(f"  Titel:  {data['title']['rendered']}")
        print(f"  Status: {data['status']}")
        print(f"  Link:   {data['link']}")
    else:
        print(f"Fout {r.status_code}: {r.text[:300]}")

if __name__ == "__main__":
    main()
