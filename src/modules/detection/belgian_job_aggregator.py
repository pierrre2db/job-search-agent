"""
Agrégateur d'offres d'emploi pour la Belgique

Combine plusieurs sources:
- API VDAB (Flandre) - Officielle et gratuite
- Indeed Belgique - Scraping avec bypass Cloudflare
- Future: StepStone, Jobat, Forem, etc.
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .vdab_api import VDABScraper, VDABJobOffer
from .indeed_bypass import IndeedBypassScraper, JobOffer as IndeedJobOffer

logger = logging.getLogger(__name__)


@dataclass
class AggregatedJobOffer:
    """
    Offre d'emploi normalisée provenant de différentes sources

    Permet d'avoir un format uniforme quelle que soit la source
    """
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str  # "VDAB", "Indeed", etc.
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    contract_type: Optional[str] = None
    remote: bool = False
    scraped_at: datetime = None

    # Métadonnées
    raw_data: Optional[Dict[str, Any]] = None  # Données originales

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'source': self.source,
            'posted_date': self.posted_date,
            'salary': self.salary,
            'contract_type': self.contract_type,
            'remote': self.remote,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None
        }


class BelgianJobAggregator:
    """
    Agrégateur multi-sources pour le marché belge

    Combine:
    - VDAB API (Flandre) - Gratuit, légal, fiable
    - Indeed BE - Scraping avec bypass Cloudflare

    Future:
    - StepStone BE
    - Jobat.be
    - Forem (Wallonie)
    """

    def __init__(
        self,
        vdab_client_id: Optional[str] = None,
        indeed_headless: bool = False,
        enable_deduplication: bool = True
    ):
        """
        Initialise l'agrégateur

        Args:
            vdab_client_id: Client ID VDAB (optionnel si dans .env)
            indeed_headless: Mode headless pour Indeed (False recommandé)
            enable_deduplication: Activer la déduplication des offres
        """
        self.enable_deduplication = enable_deduplication

        # Initialiser les scrapers
        try:
            self.vdab_scraper = VDABScraper(client_id=vdab_client_id)
            self.vdab_available = True
            logger.info("✅ VDAB API disponible")
        except Exception as e:
            logger.warning(f"⚠️ VDAB API non disponible: {e}")
            self.vdab_scraper = None
            self.vdab_available = False

        self.indeed_scraper = IndeedBypassScraper(
            headless=indeed_headless,
            country='be'
        )
        logger.info("✅ Indeed BE scraper initialisé")

    def search(
        self,
        query: str,
        location: str = "Belgique",
        max_results_per_source: int = 50,
        sources: Optional[List[str]] = None
    ) -> List[AggregatedJobOffer]:
        """
        Recherche d'offres sur toutes les sources disponibles

        Args:
            query: Mots-clés de recherche
            location: Localisation (ex: "Bruxelles", "Belgique")
            max_results_per_source: Nombre max de résultats par source
            sources: Liste des sources à utiliser (None = toutes)

        Returns:
            Liste d'offres normalisées et éventuellement dédupliquées
        """
        all_offers = []

        # Sources par défaut
        if sources is None:
            sources = []
            if self.vdab_available:
                sources.append('vdab')
            sources.append('indeed')

        logger.info(f"🔍 Recherche agrégée: '{query}' à {location}")
        logger.info(f"📊 Sources actives: {', '.join(sources)}")

        # VDAB
        if 'vdab' in sources and self.vdab_available:
            try:
                vdab_offers = self._search_vdab(query, location, max_results_per_source)
                all_offers.extend(vdab_offers)
                logger.info(f"  ✅ VDAB: {len(vdab_offers)} offres")
            except Exception as e:
                logger.error(f"  ❌ Erreur VDAB: {e}")

        # Indeed BE
        if 'indeed' in sources:
            try:
                indeed_offers = self._search_indeed(query, location, max_results_per_source)
                all_offers.extend(indeed_offers)
                logger.info(f"  ✅ Indeed: {len(indeed_offers)} offres")
            except Exception as e:
                logger.error(f"  ❌ Erreur Indeed: {e}")

        # Déduplication
        if self.enable_deduplication and len(all_offers) > 0:
            all_offers = self._deduplicate(all_offers)
            logger.info(f"🔄 Après déduplication: {len(all_offers)} offres uniques")

        logger.info(f"🎉 Total: {len(all_offers)} offres")
        return all_offers

    def _search_vdab(
        self,
        query: str,
        location: str,
        max_results: int
    ) -> List[AggregatedJobOffer]:
        """Recherche sur VDAB"""
        # Adapter la localisation pour VDAB (néerlandais)
        vdab_location = self._adapt_location_for_vdab(location)

        vdab_offers = self.vdab_scraper.search(
            query=query,
            location=vdab_location,
            max_results=max_results
        )

        # Normaliser au format AggregatedJobOffer
        return [self._normalize_vdab_offer(offer) for offer in vdab_offers]

    def _search_indeed(
        self,
        query: str,
        location: str,
        max_results: int
    ) -> List[AggregatedJobOffer]:
        """Recherche sur Indeed BE"""
        # Calculer le nombre de pages
        max_pages = max(1, max_results // 16)  # ~16 offres/page

        indeed_offers = self.indeed_scraper.scrape(
            query=query,
            location=location,
            max_pages=max_pages
        )

        # Normaliser au format AggregatedJobOffer
        return [self._normalize_indeed_offer(offer) for offer in indeed_offers]

    def _normalize_vdab_offer(self, offer: VDABJobOffer) -> AggregatedJobOffer:
        """Normalise une offre VDAB"""
        return AggregatedJobOffer(
            id=f"vdab_{offer.id}",
            title=offer.title,
            company=offer.company,
            location=offer.location,
            description=offer.description,
            url=offer.url,
            source="VDAB",
            posted_date=offer.posted_date,
            salary=offer.salary,
            contract_type=offer.contract_type,
            remote=offer.remote,
            scraped_at=offer.scraped_at,
            raw_data=offer.to_dict()
        )

    def _normalize_indeed_offer(self, offer: IndeedJobOffer) -> AggregatedJobOffer:
        """Normalise une offre Indeed"""
        return AggregatedJobOffer(
            id=f"indeed_{hash(offer.url)}",  # Utiliser hash de l'URL comme ID
            title=offer.title,
            company=offer.company,
            location=offer.location,
            description=offer.description,
            url=offer.url,
            source="Indeed BE",
            posted_date=offer.posted_date,
            salary=offer.salary,
            contract_type=None,  # Indeed n'a pas toujours cette info
            remote=offer.remote,
            scraped_at=offer.scraped_at
        )

    def _deduplicate(self, offers: List[AggregatedJobOffer]) -> List[AggregatedJobOffer]:
        """
        Déduplique les offres basé sur titre + entreprise

        Stratégie:
        1. Normaliser titre et entreprise (lowercase, trim)
        2. Créer une clé (titre, entreprise)
        3. Garder la première occurrence de chaque clé
        """
        seen = set()
        unique_offers = []

        for offer in offers:
            # Créer une clé normalisée
            title_norm = offer.title.lower().strip()
            company_norm = offer.company.lower().strip()
            key = (title_norm, company_norm)

            if key not in seen:
                seen.add(key)
                unique_offers.append(offer)
            else:
                logger.debug(f"Doublon ignoré: {offer.title} @ {offer.company}")

        duplicates_count = len(offers) - len(unique_offers)
        if duplicates_count > 0:
            logger.info(f"  🗑️ {duplicates_count} doublons supprimés")

        return unique_offers

    def _adapt_location_for_vdab(self, location: str) -> str:
        """
        Adapte la localisation pour VDAB (néerlandais)

        Bruxelles -> Brussel
        Anvers -> Antwerpen
        Gand -> Gent
        Belgique -> Vlaanderen
        """
        mapping = {
            'bruxelles': 'Brussel',
            'brussels': 'Brussel',
            'anvers': 'Antwerpen',
            'gand': 'Gent',
            'louvain': 'Leuven',
            'belgique': 'Vlaanderen',
            'belgium': 'Vlaanderen',
            'flandre': 'Vlaanderen',
            'flanders': 'Vlaanderen'
        }

        location_lower = location.lower().strip()
        return mapping.get(location_lower, location)

    def close(self):
        """Ferme les connections"""
        if self.vdab_scraper:
            self.vdab_scraper.close()
        if self.indeed_scraper:
            self.indeed_scraper.close()

    def __enter__(self):
        """Support context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup context manager"""
        self.close()


# Exemple d'utilisation
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 80)
    print("🇧🇪 AGRÉGATEUR D'EMPLOIS BELGES")
    print("=" * 80)
    print()
    print("Sources:")
    print("  ✅ VDAB (Flandre) - API officielle")
    print("  ✅ Indeed BE - Scraping")
    print()
    print("=" * 80)
    print()

    with BelgianJobAggregator(indeed_headless=False) as aggregator:
        # Recherche agrégée
        offers = aggregator.search(
            query="Python Developer",
            location="Bruxelles",
            max_results_per_source=10
        )

        print(f"\n✅ {len(offers)} offres trouvées au total\n")

        # Grouper par source
        by_source = {}
        for offer in offers:
            source = offer.source
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(offer)

        # Afficher par source
        for source, source_offers in by_source.items():
            print(f"\n📊 {source}: {len(source_offers)} offres")
            print("-" * 80)

            for i, offer in enumerate(source_offers[:5], 1):  # Max 5 par source
                print(f"{i}. {offer.title}")
                print(f"   🏢 {offer.company}")
                print(f"   📍 {offer.location}")
                if offer.salary:
                    print(f"   💰 {offer.salary}")
                if offer.remote:
                    print(f"   🏠 Remote")
                print(f"   🔗 {offer.url[:80]}...")
                print()

        # Statistiques globales
        print(f"\n{'=' * 80}")
        print("📈 Statistiques globales:")
        print(f"{'=' * 80}")
        print(f"Total: {len(offers)} offres")
        for source, source_offers in by_source.items():
            print(f"  - {source}: {len(source_offers)}")

        remote_count = sum(1 for o in offers if o.remote)
        with_salary = sum(1 for o in offers if o.salary)

        print(f"\nRemote: {remote_count} ({remote_count*100//len(offers) if len(offers) > 0 else 0}%)")
        print(f"Avec salaire: {with_salary} ({with_salary*100//len(offers) if len(offers) > 0 else 0}%)")
