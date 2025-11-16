"""
Script de test et diagnostic du scraper Indeed
"""

import logging
from src.modules.detection.jobboard_scraper import IndeedScraper

# Configuration du logging détaillé
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_scraper():
    """Test du scraper avec diagnostic"""

    print("=" * 80)
    print("🧪 TEST DU SCRAPER INDEED")
    print("=" * 80)

    # Créer le scraper
    scraper = IndeedScraper(
        rate_limit_delay=(1, 2),  # Plus rapide pour le test
        timeout=30
    )

    # Test 1: Scraping basique
    print("\n📋 Test 1: Scraping de 1 page...")
    print("-" * 80)

    try:
        offers = scraper.scrape(
            query="Développeur Python",  # En français
            location="Paris",
            max_pages=1,
            radius=25
        )

        print(f"\n✅ Scraping terminé")
        print(f"📊 Nombre d'offres trouvées: {len(offers)}")

        if offers:
            print(f"\n🎯 Première offre:")
            print(f"   Titre: {offers[0].title}")
            print(f"   Entreprise: {offers[0].company}")
            print(f"   Localisation: {offers[0].location}")
            print(f"   URL: {offers[0].url}")
            print(f"   Remote: {offers[0].remote}")
            if offers[0].salary:
                print(f"   Salaire: {offers[0].salary}")

            # Afficher toutes les offres trouvées
            print(f"\n📝 Liste de toutes les offres:")
            for i, offer in enumerate(offers, 1):
                print(f"\n{i}. {offer.title} @ {offer.company}")
                print(f"   📍 {offer.location}")
                if offer.salary:
                    print(f"   💰 {offer.salary}")
                print(f"   🔗 {offer.url[:80]}...")
        else:
            print("\n⚠️ Aucune offre trouvée")
            print("\n🔍 Diagnostic:")
            print("   - Les sélecteurs HTML ont peut-être changé")
            print("   - Indeed bloque peut-être le scraping")
            print("   - Essayez une requête différente")

            # Faire un test de connexion de base
            print("\n🌐 Test de connexion à Indeed...")
            import requests
            try:
                response = requests.get(
                    "https://fr.indeed.com/jobs",
                    params={'q': 'Python', 'l': 'Paris'},
                    timeout=10
                )
                print(f"   Status code: {response.status_code}")
                print(f"   Taille HTML: {len(response.text)} bytes")

                # Sauvegarder le HTML pour inspection
                with open('indeed_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"   ✅ HTML sauvegardé dans: indeed_response.html")

            except Exception as e:
                print(f"   ❌ Erreur de connexion: {e}")

    except Exception as e:
        print(f"\n❌ Erreur lors du scraping: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Vérifier les User-Agents
    print("\n" + "=" * 80)
    print("🔧 Test 2: Vérification des User-Agents")
    print("-" * 80)
    for i in range(3):
        ua = scraper._get_random_user_agent()
        print(f"UA {i+1}: {ua[:60]}...")

    print("\n" + "=" * 80)
    print("✅ Tests terminés")
    print("=" * 80)

if __name__ == "__main__":
    test_scraper()
