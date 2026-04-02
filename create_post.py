"""
Grandcru Grapes — Maak een WordPress post aan via de REST API.
Gebruik: python create_post.py
"""
import requests

WP_USER = "jannes_v36jq7op"
WP_PASS = "yN7I hBQQ 0vzZ 7jSw a6rS ByBy"
API_URL = "https://grandcrugrapes.com/wp-json/wp/v2/posts"

POST = {
    "title": "Bourgogne: de heilige grond van de wijnwereld",
    "status": "draft",  # wijzig naar "publish" om direct te publiceren
    "content": """
<!-- wp:paragraph -->
<p>Er is geen wijnregio ter wereld die zo veel ontzag afdwingt als <strong>Bourgogne</strong>. Op een relatief klein lapje grond in het oosten van Frankrijk — van Chablis in het noorden tot Mâcon in het zuiden — worden enkele van de meest begeerde wijnen ooit gemaakt.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Pinot Noir &amp; Chardonnay: twee druiven, eindeloze diepte</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Bourgogne werkt met slechts twee druivenrassen. <strong>Pinot Noir</strong> voor de rode wijnen, <strong>Chardonnay</strong> voor de witte. Geen blends, geen toegevoegde smaakstoffen. Alles staat of valt met de terroir — de unieke combinatie van bodem, helling, expositie en microklimaat die elke wijngaard zijn eigen karakter geeft.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>De hiërarchie van het land</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Bourgogne kent een strikt classificatiesysteem, van regionaal tot grand cru:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Régionale</strong> – wijnen die de naam van de regio dragen, zoals Bourgogne Rouge of Bourgogne Blanc.</li>
<li><strong>Village</strong> – wijnen uit één specifiek dorp, zoals Gevrey-Chambertin, Meursault of Puligny-Montrachet.</li>
<li><strong>Premier Cru</strong> – wijnen van aangewezen topwijngaarden binnen een dorp. Er zijn meer dan 600 premiers crus in Bourgogne.</li>
<li><strong>Grand Cru</strong> – de absolute top. Slechts 33 grand crus bestaan, goed voor minder dan 2% van de totale productie.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Domaines om te kennen</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Namen als <strong>Domaine de la Romanée-Conti</strong>, <strong>Armand Rousseau</strong>, <strong>Domaine Leroy</strong> en <strong>Coche-Dury</strong> zijn geen marketingverhalen — het zijn families die generaties lang hetzelfde perceel hebben bewerkt, jaar na jaar. Hun wijnen zijn schaars, begeerd en tijdloos.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Bij Grandcru Grapes volgen wij deze producenten op de voet. Of het nu gaat om een toegankelijke village-wijn of een zeldzame grand cru uit een topjaar — kwaliteit en authenticiteit staan altijd centraal.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Wanneer drinken?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Bourgogne vraagt geduld. Een grand cru Pinot Noir heeft doorgaans 10 tot 20 jaar nodig om volledig open te bloeien. Witte grand crus uit Puligny of Meursault kunnen na een initiële openingsfase een gesloten periode ingaan — en daarna spectaculair opengaan. De beloning voor wie wacht is groot.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><em>Ontdek ons actuele aanbod Bourgognes — van cellaardirecte premiers crus tot rijpe grands crus klaar voor de tafel.</em></p>
<!-- /wp:paragraph -->
""",
    "excerpt": "Bourgogne is de heilige grond van de wijnwereld. Pinot Noir en Chardonnay, grand crus en legendarische domaines — een introductie op de meest geliefde wijnregio.",
    "format": "standard",
}

def main():
    r = requests.post(API_URL, auth=(WP_USER, WP_PASS), json=POST, timeout=30)
    if r.status_code in (200, 201):
        data = r.json()
        print(f"Post aangemaakt!")
        print(f"  ID:     {data['id']}")
        print(f"  Titel:  {data['title']['rendered']}")
        print(f"  Status: {data['status']}")
        print(f"  Link:   {data['link']}")
    else:
        print(f"Fout {r.status_code}: {r.text[:300]}")

if __name__ == "__main__":
    main()
