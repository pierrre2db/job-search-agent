"""
Script de test pour l'API VDAB
Service officiel d'emploi flamand (Belgique)
"""

import logging
from src.modules.detection.vdab_api import VDABScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 80)
print("🇧🇪 TEST API VDAB - SERVICE OFFICIEL FLAMAND")
print("=" * 80)
print()

# Créer le scraper (charge automatiquement les credentials depuis .env)
try:
    with VDABScraper() as scraper:
        print("🔍 Recherche: 'Python Developer' à Brussel\n")

        # Test de recherche
        offers = scraper.search(
            query="Python Developer",
            location="Brussel",
            max_results=10,
            sort_by="date"
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
                    print(f"   🏠 Thuiswerk/Remote")

                if offer.contract_type:
                    print(f"   📝 {offer.contract_type}")

                if offer.number_of_positions and offer.number_of_positions > 1:
                    print(f"   👥 {offer.number_of_positions} postes")

                if offer.study_level:
                    print(f"   🎓 Niveau: {offer.study_level}")

                print(f"   🔗 {offer.url[:80]}...")
                print()

            # Statistiques
            remote_count = sum(1 for o in offers if o.remote)
            with_salary = sum(1 for o in offers if o.salary)
            multiple_positions = sum(1 for o in offers if o.number_of_positions and o.number_of_positions > 1)

            print(f"\n📊 Statistiques:")
            print(f"   Total: {len(offers)} offres")
            print(f"   Remote: {remote_count} ({remote_count*100//len(offers) if len(offers) > 0 else 0}%)")
            print(f"   Avec salaire: {with_salary} ({with_salary*100//len(offers) if len(offers) > 0 else 0}%)")
            print(f"   Postes multiples: {multiple_positions}")

        else:
            print("❌ Aucune offre trouvée")
            print()
            print("💡 Suggestions:")
            print("   - Essayez une requête plus générale (ex: 'Developer')")
            print("   - Vérifiez la localisation (ex: 'Vlaanderen', 'Antwerpen')")
            print("   - Consultez https://www.vdab.be/vindeenjob pour voir les offres disponibles")

except ValueError as e:
    print(f"❌ Configuration incorrecte: {e}")
    print()
    print("📝 Pour configurer l'API VDAB:")
    print("   1. Créez un compte sur https://developer.vdab.be/openservices/")
    print("   2. Créez une application et obtenez votre Client ID")
    print("   3. Créez le fichier: config/credentials/vdab_credentials.env")
    print("   4. Ajoutez: VDAB_CLIENT_ID=votre_client_id")
    print()
    print("📖 Guide complet: docs/VDAB_SETUP_GUIDE.md")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'=' * 80}")
print("Test terminé")
print(f"{'=' * 80}")
