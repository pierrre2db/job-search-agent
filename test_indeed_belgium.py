"""
Test du scraper Indeed pour le marché BELGE
"""

import logging
from src.modules.detection.indeed_bypass import IndeedBypassScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 80)
print("🇧🇪 TEST SCRAPER INDEED - MARCHÉ BELGE")
print("=" * 80)
print()

# Test avec différentes villes belges
locations = [
    "Bruxelles",
    "Liège",
    "Anvers",
    "Belgique"  # Recherche nationale
]

print("📍 Villes testées:")
for loc in locations:
    print(f"   - {loc}")
print()

# Tester avec Bruxelles
print(f"🔍 Test avec: Bruxelles\n")

with IndeedBypassScraper(headless=False, verbose=False) as scraper:
    # Modifier l'URL de base pour Indeed Belgique
    scraper.BASE_URL = "https://be.indeed.com"
    scraper.SEARCH_URL = f"{scraper.BASE_URL}/jobs"

    offers = scraper.scrape(
        query="Python Developer",
        location="Bruxelles",
        max_pages=1
    )

    print(f"\n{'=' * 80}")
    print(f"✅ {len(offers)} offres trouvées à Bruxelles")
    print(f"{'=' * 80}\n")

    if offers:
        for i, offer in enumerate(offers[:10], 1):  # Afficher max 10
            print(f"{i}. {offer.title}")
            print(f"   🏢 {offer.company}")
            print(f"   📍 {offer.location}")
            if offer.salary:
                print(f"   💰 {offer.salary}")
            if offer.remote:
                print(f"   🏠 Remote/Télétravail")
            print(f"   🔗 {offer.url[:80]}...")
            print()

        # Statistiques
        remote_count = sum(1 for o in offers if o.remote)
        with_salary = sum(1 for o in offers if o.salary)

        print(f"\n📊 Statistiques:")
        print(f"   Total: {len(offers)} offres")
        print(f"   Remote: {remote_count} ({remote_count*100//len(offers)}%)")
        print(f"   Avec salaire: {with_salary} ({with_salary*100//len(offers)}%)")
    else:
        print("❌ Aucune offre trouvée")
        print("\n💡 Suggestions:")
        print("   - Essayer une requête plus générale ('Developer', 'Informatique')")
        print("   - Vérifier la connexion Internet")
        print("   - Tester avec 'Belgique' comme localisation")

print(f"\n{'=' * 80}")
print("Test terminé")
print(f"{'=' * 80}")
