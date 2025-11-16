"""
Test du scraper Indeed en mode VISIBLE (non-headless)
Ce mode est plus fiable contre Cloudflare
"""

import logging
from src.modules.detection.indeed_bypass import IndeedBypassScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 80)
print("🧪 TEST SCRAPER INDEED - MODE VISIBLE")
print("=" * 80)
print()
print("ℹ️  Une fenêtre Chrome va s'ouvrir (c'est normal)")
print("   Ne la fermez pas pendant le scraping")
print()

# Utiliser en mode NON-headless (fenêtre visible)
with IndeedBypassScraper(headless=False, verbose=False) as scraper:
    offers = scraper.scrape(
        query="Python Developer",
        location="Paris",
        max_pages=1  # 1 page pour le test
    )

    print(f"\n{'=' * 80}")
    print(f"✅ {len(offers)} offres trouvées")
    print(f"{'=' * 80}\n")

    if offers:
        for i, offer in enumerate(offers, 1):
            print(f"{i}. {offer.title}")
            print(f"   🏢 {offer.company}")
            print(f"   📍 {offer.location}")
            if offer.salary:
                print(f"   💰 {offer.salary}")
            if offer.remote:
                print(f"   🏠 Remote")
            print(f"   🔗 {offer.url[:80]}...")
            print()
    else:
        print("❌ Aucune offre trouvée")
        print("\nPossibles raisons:")
        print("- Cloudflare bloque toujours")
        print("- Problème de parsing HTML")
        print("- Connexion internet")

print(f"{'=' * 80}")
print("Test terminé")
print(f"{'=' * 80}")
