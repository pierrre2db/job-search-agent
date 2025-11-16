"""
Démonstration complète du système de recherche d'emploi pour la Belgique

Ce script montre:
1. Recherche sur Indeed BE (sans VDAB si pas de Client ID)
2. Recherche sur VDAB (si Client ID configuré)
3. Agrégation et déduplication
4. Export des résultats

Usage:
    python demo_belgium.py
"""

import logging
import json
from datetime import datetime
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 80)
print("🇧🇪 DÉMONSTRATION - SYSTÈME DE RECHERCHE D'EMPLOI BELGIQUE")
print("=" * 80)
print()
print("Ce script va:")
print("  1. Rechercher des offres sur Indeed BE")
print("  2. Rechercher des offres sur VDAB (si configuré)")
print("  3. Agréger et dédupliquer les résultats")
print("  4. Sauvegarder dans results/belgium_jobs.json")
print()
print("=" * 80)
print()

# Configuration de la recherche
QUERY = "Python Developer"
LOCATION = "Bruxelles"
MAX_RESULTS = 20

print(f"📋 Paramètres de recherche:")
print(f"   Requête: {QUERY}")
print(f"   Localisation: {LOCATION}")
print(f"   Max résultats: {MAX_RESULTS}")
print()

# ============================================================================
# Test 1: Indeed BE seul
# ============================================================================

print("=" * 80)
print("📊 TEST 1: INDEED BELGIQUE")
print("=" * 80)
print()

try:
    from src.modules.detection.indeed_bypass import IndeedBypassScraper

    print("🔍 Lancement du scraper Indeed BE...")
    print("   ⚠️  Une fenêtre Chrome va s'ouvrir (mode non-headless)")
    print()

    with IndeedBypassScraper(headless=False, country='be') as scraper:
        indeed_offers = scraper.scrape(
            query=QUERY,
            location=LOCATION,
            max_pages=2  # 2 pages = ~32 offres max
        )

    print(f"\n✅ Indeed BE: {len(indeed_offers)} offres trouvées")

    # Afficher les 5 premières
    print("\n📝 Aperçu des offres Indeed BE:")
    for i, offer in enumerate(indeed_offers[:5], 1):
        print(f"\n{i}. {offer.title}")
        print(f"   🏢 {offer.company}")
        print(f"   📍 {offer.location}")
        if offer.remote:
            print(f"   🏠 Remote/Télétravail")
        print(f"   🔗 {offer.url[:70]}...")

except Exception as e:
    print(f"❌ Erreur Indeed BE: {e}")
    indeed_offers = []

# ============================================================================
# Test 2: VDAB (si configuré)
# ============================================================================

print("\n\n" + "=" * 80)
print("📊 TEST 2: API VDAB")
print("=" * 80)
print()

vdab_offers = []

try:
    from src.modules.detection.vdab_api import VDABScraper

    print("🔍 Tentative de connexion à l'API VDAB...")

    with VDABScraper() as scraper:
        vdab_offers = scraper.search(
            query=QUERY,
            location="Brussel",  # Version néerlandaise
            max_results=MAX_RESULTS
        )

    print(f"✅ VDAB: {len(vdab_offers)} offres trouvées")

    # Afficher les 5 premières
    print("\n📝 Aperçu des offres VDAB:")
    for i, offer in enumerate(vdab_offers[:5], 1):
        print(f"\n{i}. {offer.title}")
        print(f"   🏢 {offer.company}")
        print(f"   📍 {offer.location}")
        if offer.remote:
            print(f"   🏠 Thuiswerk/Remote")
        if offer.number_of_positions and offer.number_of_positions > 1:
            print(f"   👥 {offer.number_of_positions} postes")
        print(f"   🔗 {offer.url[:70]}...")

except ValueError as e:
    print(f"⚠️  VDAB non configuré: {e}")
    print()
    print("💡 Pour activer VDAB:")
    print("   1. Créez un compte sur https://developer.vdab.be/openservices/")
    print("   2. Obtenez votre Client ID")
    print("   3. Créez: config/credentials/vdab_credentials.env")
    print("   4. Ajoutez: VDAB_CLIENT_ID=votre_id")
    print()
    print("📖 Guide complet: docs/VDAB_SETUP_GUIDE.md")

except Exception as e:
    print(f"❌ Erreur VDAB: {e}")

# ============================================================================
# Test 3: Agrégateur (si on a des offres)
# ============================================================================

if indeed_offers or vdab_offers:
    print("\n\n" + "=" * 80)
    print("📊 TEST 3: AGRÉGATION ET DÉDUPLICATION")
    print("=" * 80)
    print()

    try:
        from src.modules.detection.belgian_job_aggregator import BelgianJobAggregator

        # Utiliser l'agrégateur
        print("🔄 Utilisation de l'agrégateur multi-sources...")

        with BelgianJobAggregator(indeed_headless=False) as aggregator:
            all_offers = aggregator.search(
                query=QUERY,
                location=LOCATION,
                max_results_per_source=MAX_RESULTS
            )

        print(f"\n✅ Agrégateur: {len(all_offers)} offres uniques après déduplication")

        # Statistiques par source
        by_source = {}
        for offer in all_offers:
            source = offer.source
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(offer)

        print("\n📊 Répartition par source:")
        for source, offers in by_source.items():
            print(f"   {source}: {len(offers)} offres")

        # Statistiques globales
        remote_count = sum(1 for o in all_offers if o.remote)
        with_salary = sum(1 for o in all_offers if o.salary)

        print("\n📈 Statistiques:")
        print(f"   Total: {len(all_offers)} offres")
        print(f"   Remote: {remote_count} ({remote_count*100//len(all_offers) if len(all_offers) > 0 else 0}%)")
        print(f"   Avec salaire: {with_salary} ({with_salary*100//len(all_offers) if len(all_offers) > 0 else 0}%)")

    except Exception as e:
        print(f"❌ Erreur agrégateur: {e}")
        all_offers = []

else:
    print("\n⚠️ Aucune offre disponible pour l'agrégation")
    all_offers = []

# ============================================================================
# Export des résultats
# ============================================================================

print("\n\n" + "=" * 80)
print("💾 EXPORT DES RÉSULTATS")
print("=" * 80)
print()

if all_offers:
    # Créer le dossier results s'il n'existe pas
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Préparer les données pour export
    export_data = {
        'metadata': {
            'query': QUERY,
            'location': LOCATION,
            'timestamp': datetime.now().isoformat(),
            'total_offers': len(all_offers),
            'sources': list(by_source.keys()) if 'by_source' in locals() else []
        },
        'statistics': {
            'by_source': {src: len(offers) for src, offers in by_source.items()} if 'by_source' in locals() else {},
            'remote_count': remote_count if 'remote_count' in locals() else 0,
            'with_salary': with_salary if 'with_salary' in locals() else 0
        },
        'offers': [offer.to_dict() for offer in all_offers]
    }

    # Sauvegarder en JSON
    output_file = results_dir / "belgium_jobs.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Résultats sauvegardés dans: {output_file}")
    print(f"   Fichier: {output_file.absolute()}")
    print(f"   Taille: {output_file.stat().st_size / 1024:.1f} KB")

    # Créer aussi un fichier CSV simple
    import csv
    csv_file = results_dir / "belgium_jobs.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Titre', 'Entreprise', 'Localisation', 'Source', 'Remote', 'URL'])

        for offer in all_offers:
            writer.writerow([
                offer.title,
                offer.company,
                offer.location,
                offer.source,
                'Oui' if offer.remote else 'Non',
                offer.url
            ])

    print(f"✅ Export CSV créé: {csv_file}")

else:
    print("⚠️ Aucune offre à exporter")

# ============================================================================
# Résumé final
# ============================================================================

print("\n\n" + "=" * 80)
print("📊 RÉSUMÉ DE LA DÉMONSTRATION")
print("=" * 80)
print()

print("Sources testées:")
print(f"  ✅ Indeed BE: {'OK' if indeed_offers else 'ÉCHEC'} ({len(indeed_offers)} offres)")
print(f"  {'✅' if vdab_offers else '⚠️ '} VDAB: {'OK' if vdab_offers else 'Non configuré'} ({len(vdab_offers)} offres)")
print()

if all_offers:
    print(f"✅ Total final: {len(all_offers)} offres uniques")
    print()
    print("📁 Fichiers générés:")
    print(f"   - results/belgium_jobs.json")
    print(f"   - results/belgium_jobs.csv")
    print()
    print("💡 Prochaines étapes:")
    print("   1. Consultez les fichiers dans le dossier results/")
    print("   2. Configurez VDAB pour encore plus d'offres")
    print("   3. Adaptez les paramètres de recherche selon vos besoins")
else:
    print("⚠️ Aucune offre trouvée")
    print()
    print("💡 Suggestions:")
    print("   1. Vérifiez votre connexion Internet")
    print("   2. Essayez une requête plus générale")
    print("   3. Configurez VDAB pour accéder à plus d'offres")

print()
print("=" * 80)
print("✅ Démonstration terminée")
print("=" * 80)
