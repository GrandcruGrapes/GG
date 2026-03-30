"""
Grandcru Grapes — idealwine lot monitor
"""

import requests
import json
import os
import datetime

ALGOLIA_APP_ID  = os.environ.get("ALGOLIA_APP_ID",  "QYOXXVLLKU")
ALGOLIA_API_KEY = os.environ.get("ALGOLIA_API_KEY", "8319a3608b7579514df153d9c8ba64bd")
GMAIL_ADDRESS   = os.environ.get("GMAIL_ADDRESS",   "")
GMAIL_APP_PW    = os.environ.get("GMAIL_APP_PW",    "")
MAIL_TO         = os.environ.get("MAIL_TO",         "")
AUCTION_COSTS   = 1.215
SEEN_FILE       = "seen_lots.json"

PRODUCERS = [
    "Alexandre Chaillon", "Anne Gros", "Antinori", "Antoine Sanzay",
    "Armand Rousseau", "Arnaud Ente", "Arnaud Lambert", "Arnoux-Lachaux",
    "Bartolo Mascarello", "Benoit Lahaye", "Bérêche et Fils", "Bernard Baudry",
    "Berthaut-Gerbet", "Bodegas Vega Sicilia", "Bollinger", "Bonneau Du Martray",
    "Bruno Clair", "Bruno Giacosa", "Cantina Terlano", "Caroline Morey",
    "Cecile Tremblay", "Chartogne-Taillet", "Chateau de Beaucastel",
    "Charles Lachaux", "Chave", "Christian Moreau", "Clos Rougeard",
    "Coche Dury", "Comte Armand", "Comtes Lafon", "Dagueneau", "David Duband",
    "Denis Mortet", "Didier Dagueneau", "Dom Perignon", "Dom Pérignon",
    "Domaine Armand Rousseau", "Domaine Auguste Clape", "Domaine Aux Moines",
    "Domaine Berthaut-Gerbet", "Domaine Bruno Clair", "Domaine Coche-Dury",
    "Domaine De La Romanée-Conti", "Domaine de Montille",
    "Domaine Des Lambrays", "Domaine Dujac", "Domaine Etienne Sauzet",
    "Domaine Fourrier", "Domaine Georges Mugneret-Gibourg",
    "Domaine Georges Roumier", "Domaine Guiberteau", "Domaine Guy Roulot",
    "Domaine Henri Gouges", "Domaine Huet", "Domaine Jacques-Frédéric Mugnier",
    "Domaine Jamet", "Domaine Leflaive", "Domaine Leroy",
    "Domaine Marquis D'Angerville", "Domaine Méo-Camuzet",
    "Domaine Michel Lafarge", "Domaine Mugneret-Gibourg", "Domaine Ponsot",
    "Domaine Prieuré Roch", "Domaine Raveneau", "Domaine René Vincent Dauvissat",
    "Domaine Robert Chevillon", "Domaine Vacheron", "Domaine Vincent Pinard",
    "E. Guigal", "Egly-Ouriet", "Egon Müller", "Emmanuel Houillon",
    "Francois Raveneau", "Frederic Savart", "Gangloff", "Gaspard Brochet",
    "Georges Mugneret Gibourg", "Giovanni Canonica", "Guy Breton",
    "Henri Boillot", "Hubert Lignier", "Hudelot-Noellat",
    "Jacques Selosse", "Jacques-Frédéric Mugnier", "Jacquesson & Fils",
    "Jean Claude Ramonet", "Jean Foillard", "Jean-Francois Ganevat",
    "Jerome Prevost", "Jules Brochet", "Krug", "La Grange Tiphaine",
    "Lapierre", "Marc Sorrel", "Montevertine", "Opus One", "Ornellaia",
    "Pascal Cotat", "Philippe Pacalet", "Pierre Girardin", "Pierre Gonon",
    "Pierre Overnoy", "Pierre Péters", "Pierre-Yves Colin-Morey",
    "Ramonet", "Raveneau", "Richard Leroy", "Ridge Vineyards", "Rinaldi",
    "Rostaing", "Ruinart", "Sadie Family Wines", "Stella di Campalto",
    "Stéphane Bernaudeau", "Stéphane Tissot", "Sylvain Cathiard",
    "Sylvain Pataille", "Tenuta San Guido", "Thierry Allemand",
    "Thierry Germain", "Trimbach", "Vega Sicilia", "Vietti",
    "Vincent Dauvissat", "Vouette et Sobée", "Weingut Knoll",
    "Weingut Robert Weil", "Weingut Wittmann", "Giacomo Conterno",
    "Etienne Sauzet", "Roulot", "Comte Liger-Belair",
]

PORTFOLIO_PRODUCERS = [
    "Anne Gros", "Raveneau", "Vincent Dauvissat", "Krug", "Bollinger",
    "Tenuta San Guido", "Comtes Lafon", "Gaspard Brochet", "Giovanni Canonica",
    "Pierre Girardin", "Jean Claude Ramonet", "Sadie Family",
]

TOP_PRODUCERS = [
    "Domaine De La Romanée-Conti", "Armand Rousseau", "Domaine Leroy",
    "Domaine Dujac", "Georges Roumier", "Giacomo Conterno", "Bartolo Mascarello",
    "Jacques Selosse", "Egon Müller", "Sylvain Cathiard", "Domaine Leflaive",
    "Domaine Méo-Camuzet", "Comte Liger-Belair", "Coche Dury",
    "Raveneau", "Vincent Dauvissat", "Vega Sicilia", "Ornellaia",
]

def vintage_score(vintage_str):
    try:
        age = 2026 - int(vintage_str)
        if age <= 2:  return 1
        if age == 3:  return 4
        if age <= 5:  return 6
        if age <= 10: return 9
        if age <= 15: return 10
        if age <= 20: return 8
        return 5
    except:
        return 6

def producer_score(name):
    n = name.lower()
    if any(p.lower() in n for p in TOP_PRODUCERS):       return 3
    if any(p.lower() in n for p in PORTFOLIO_PRODUCERS): return 2
    return 1

def price_score(all_in):
    if all_in < 40:   return 2
    if all_in < 80:   return 5
    if all_in < 150:  return 8
    if all_in < 300:  return 10
    if all_in < 500:  return 8
    if all_in < 800:  return 6
    return 4

def score_lot(lot):
    vs = vintage_score(str(lot.get("vintage", "")))
    ps = producer_score(lot.get("name", ""))
    pr = price_score(lot.get("price_per_bottle", 0) * AUCTION_COSTS)
    return vs + (ps * 3) + pr, vs, ps, pr

def fetch_lots():
    url = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/*/queries"
    headers = {
        "x-algolia-api-key": ALGOLIA_API_KEY,
        "x-algolia-application-id": ALGOLIA_APP_ID,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    all_hits = {}
    batch_size = 15
    for i in range(0, len(PRODUCERS), batch_size):
        batch = PRODUCERS[i:i + batch_size]
        producer_filter = " OR ".join([f'domain:"{p}"' for p in batch])
        payload = {
            "requests": [{
                "indexName": "prod_lots",
                "params": (
                    "query="
                    f"&filters=({producer_filter})"
                    '&facetFilters=["sale_type:auction","bottle_size:bottle",'
                    '"bottle_level:into-neck","bottle_condition:good-appearance"]'
                    "&hitsPerPage=100"
                    "&attributesToRetrieve=objectID,name,vintage,region,"
                    "appellation,price,quantity,end_date,url,domain,current_bids"
                )
            }]
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            hits = r.json()["results"][0].get("hits", [])
            for hit in hits:
                if hit.get("objectID"):
                    all_hits[hit["objectID"]] = hit
            print(f"  Batch {i//batch_size+1}: {len(hits)} loten")
        except Exception as e:
            print(f"  Batch {i//batch_size+1} fout: {e}")

    # Print één voorbeeld lot zodat we de veldnamen kunnen controleren
    if all_hits:
        print("\n=== VOORBEELD LOT (ruwe data) ===")
        example = list(all_hits.values())[0]
        print(json.dumps(example, indent=2, ensure_ascii=False))
        print("=================================\n")

    print(f"Totaal unieke loten: {len(all_hits)}")
    return list(all_hits.values())

def main():
    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M}] Monitor gestart\n")
    lots = fetch_lots()
    if not lots:
        print("Geen loten — controleer API-credentials of index-naam.")
        return

    scored = []
    for lot in lots:
        price = lot.get("price", 0)
        qty   = max(lot.get("quantity", 1), 1)
        lot["price_per_bottle"] = price / qty
        total, vs, ps, pr = score_lot(lot)
        scored.append((lot, total, vs, ps, pr))

    scored.sort(key=lambda x: -x[1])

    top  = [(l,s,vs,ps,pr) for l,s,vs,ps,pr in scored if s >= 20]
    mid  = [(l,s,vs,ps,pr) for l,s,vs,ps,pr in scored if 14 <= s < 20]
    skip = [(l,s,vs,ps,pr) for l,s,vs,ps,pr in scored if s < 14]

    print(f"{'═'*55}")
    print(f"RESULTATEN — {datetime.date.today()}")
    print(f"Totaal: {len(lots)} loten | Interessant: {len(top)} | Mogelijk: {len(mid)} | Skip: {len(skip)}")
    print(f"{'═'*55}\n")

    if top:
        print(f"★ DIRECT INTERESSANT ({len(top)})\n{'─'*40}")
        for rank, (lot,s,vs,ps,pr) in enumerate(top, 1):
            name    = lot.get("name","?")
            vintage = lot.get("vintage","NV")
            app     = lot.get("appellation", lot.get("region",""))
            ppb     = lot.get("price_per_bottle", 0)
            incl    = ppb * AUCTION_COSTS
            qty     = lot.get("quantity",1)
            bids    = lot.get("current_bids",0)
            end     = (lot.get("end_date","") or "")[:10]
            url     = lot.get("url","")
            print(f"#{rank} {name} {vintage}")
            print(f"   {app}")
            print(f"   €{ppb:.0f}/fles → incl. veiling €{incl:.0f} | {qty} fles(sen) | {bids} bod(en) | sluit {end}")
            print(f"   Score {s}/25 (drinkvenster {vs} · producent {ps} · prijs {pr})")
            print(f"   {url}\n")

    if mid:
        print(f"\n◎ MOGELIJK INTERESSANT ({len(mid)})\n{'─'*40}")
        for rank, (lot,s,vs,ps,pr) in enumerate(mid, 1):
            name    = lot.get("name","?")
            vintage = lot.get("vintage","NV")
            ppb     = lot.get("price_per_bottle", 0)
            incl    = ppb * AUCTION_COSTS
            end     = (lot.get("end_date","") or "")[:10]
            print(f"#{rank} {name} {vintage} | €{incl:.0f} incl. | score {s}/25 | sluit {end}")

    if skip:
        print(f"\n✕ OVERGESLAGEN ({len(skip)} loten)")
        for lot,s,vs,ps,pr in skip[:5]:
            print(f"   - {lot.get('name','?')} {lot.get('vintage','NV')} (score {s}/25)")
        if len(skip) > 5:
            print(f"   ... en {len(skip)-5} anderen")

if __name__ == "__main__":
    main()
