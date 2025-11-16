"""
Script de debug pour le bypass Cloudflare
Sauvegarde le HTML reçu pour inspection
"""

import logging
from src.modules.detection.indeed_bypass import IndeedBypassScraper

logging.basicConfig(level=logging.INFO)

print("🔍 Test du bypass avec sauvegarde HTML\n")

# Utiliser le scraper en mode verbose et NON headless pour voir ce qui se passe
with IndeedBypassScraper(headless=False, verbose=True) as scraper:
    # Initialiser le driver
    scraper._init_driver()
    scraper._apply_stealth()

    # Naviguer vers Indeed
    url = "https://fr.indeed.com/jobs?q=Python+Developer&l=Paris&sort=date"
    print(f"📍 Navigation vers: {url}\n")

    scraper.driver.get(url)

    # Attendre un peu plus longtemps pour que Cloudflare se résolve
    import time
    print("⏳ Attente de 10 secondes pour résolution Cloudflare...\n")
    time.sleep(10)

    # Sauvegarder le HTML
    html = scraper.driver.page_source

    with open('indeed_bypass_response.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML sauvegardé dans: indeed_bypass_response.html")
    print(f"📊 Taille: {len(html)} bytes")

    # Vérifier si on voit Cloudflare
    if "cloudflare" in html.lower():
        print("⚠️  Cloudflare détecté dans le HTML")
        if "challenge" in html.lower():
            print("   - Challenge Cloudflare présent")
        if "blocked" in html.lower():
            print("   - Page bloquée")
    else:
        print("✅ Pas de trace de Cloudflare")

    # Vérifier si on voit des offres
    if "jobTitle" in html or "job_seen_beacon" in html:
        print("✅ Classes d'offres détectées dans le HTML")
    else:
        print("❌ Aucune classe d'offre trouvée")

    # Prendre une capture d'écran
    scraper.driver.save_screenshot('indeed_bypass_screenshot.png')
    print("📸 Screenshot sauvegardé: indeed_bypass_screenshot.png")

    print("\n🔍 Ouvrez indeed_bypass_response.html pour voir ce que Indeed retourne")
