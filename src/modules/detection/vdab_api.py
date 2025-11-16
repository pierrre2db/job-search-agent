"""
VDAB API Scraper - Service officiel d'emploi flamand (Belgique)

L'API VDAB est gratuite, légale et officielle.
Documentation: https://developer.vdab.be/openservices/

Pour commencer:
1. Créer un compte sur https://developer.vdab.be/openservices/
2. Créer une application pour obtenir votre Client ID
3. Sauvegarder le Client ID dans config/credentials/vdab_credentials.env
"""

import os
import logging
import requests
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class VDABJobOffer:
    """Représente une offre d'emploi VDAB"""
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str = "VDAB"
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    contract_type: Optional[str] = None
    remote: bool = False
    scraped_at: datetime = None

    # Champs spécifiques VDAB
    number_of_positions: Optional[int] = None
    study_level: Optional[str] = None
    experience_required: Optional[str] = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'offre en dictionnaire"""
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
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'number_of_positions': self.number_of_positions,
            'study_level': self.study_level,
            'experience_required': self.experience_required
        }


class VDABScraper:
    """
    Scraper officiel pour l'API VDAB (Flandre, Belgique)

    Avantages:
    - ✅ Gratuit et légal
    - ✅ API officielle du service public flamand
    - ✅ Jusqu'à ~1000 requêtes/jour
    - ✅ Données structurées et fiables

    Documentation: https://developer.vdab.be/openservices/
    """

    # URLs de l'API
    BASE_URL_PROD = "https://openservices.vdab.be"
    BASE_URL_TEST = "https://openservices-trn.vdab.be"

    # Endpoints API v4
    VACATURES_ENDPOINT = "/vacature/v4/vacatures"

    def __init__(
        self,
        client_id: Optional[str] = None,
        use_test_env: bool = False,
        timeout: int = 30
    ):
        """
        Initialise le scraper VDAB

        Args:
            client_id: Client ID VDAB (ou via variable d'environnement VDAB_CLIENT_ID)
            use_test_env: Utiliser l'environnement de test au lieu de production
            timeout: Timeout des requêtes HTTP (secondes)
        """
        # Charger les credentials depuis .env si disponible
        load_dotenv('config/credentials/vdab_credentials.env')

        self.client_id = client_id or os.getenv('VDAB_CLIENT_ID')

        if not self.client_id:
            logger.warning(
                "⚠️ Aucun Client ID VDAB fourni. "
                "Créez un compte sur https://developer.vdab.be/openservices/"
            )

        # Sélectionner l'environnement
        self.base_url = self.BASE_URL_TEST if use_test_env else self.BASE_URL_PROD
        self.timeout = timeout

        # Configuration de la session
        self.session = requests.Session()
        self.session.headers.update({
            'X-IBM-Client-Id': self.client_id or '',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        logger.info(f"VDAB Scraper initialisé (env: {'TEST' if use_test_env else 'PROD'})")

    def search(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        max_results: int = 50,
        sort_by: str = "date",
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VDABJobOffer]:
        """
        Recherche d'offres d'emploi via l'API VDAB

        Args:
            query: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Brussel", "Antwerpen", "Vlaanderen")
            max_results: Nombre maximum de résultats (défaut: 50)
            sort_by: Tri des résultats ("date", "relevance")
            filters: Filtres additionnels (dict)

        Returns:
            Liste d'offres VDAB

        Raises:
            ValueError: Si aucun Client ID n'est configuré
            requests.RequestException: En cas d'erreur API
        """
        if not self.client_id:
            raise ValueError(
                "Client ID VDAB manquant. "
                "Créez un compte sur https://developer.vdab.be/openservices/ "
                "et configurez VDAB_CLIENT_ID dans config/credentials/vdab_credentials.env"
            )

        logger.info(f"🔍 Recherche VDAB: '{query}' à {location or 'Flandre'}")

        # Construire les paramètres de recherche
        params = self._build_search_params(
            query=query,
            location=location,
            max_results=max_results,
            sort_by=sort_by,
            filters=filters
        )

        try:
            # Appel API
            url = f"{self.base_url}{self.VACATURES_ENDPOINT}"

            logger.debug(f"GET {url}")
            logger.debug(f"Params: {params}")

            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            # Parser les résultats
            offers = self._parse_response(data)

            logger.info(f"✅ {len(offers)} offres VDAB trouvées")
            return offers

        except requests.RequestException as e:
            logger.error(f"❌ Erreur API VDAB: {e}")

            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Status code: {e.response.status_code}")
                logger.error(f"Response: {e.response.text[:500]}")

            raise

    def get_vacancy_by_id(self, vacancy_id: str) -> Optional[VDABJobOffer]:
        """
        Récupère une offre spécifique par son ID

        Args:
            vacancy_id: ID de la vacature VDAB

        Returns:
            L'offre VDAB ou None si non trouvée
        """
        if not self.client_id:
            raise ValueError("Client ID VDAB manquant")

        try:
            url = f"{self.base_url}{self.VACATURES_ENDPOINT}/{vacancy_id}"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            return self._parse_vacancy(data)

        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération de la vacature {vacancy_id}: {e}")
            return None

    def _build_search_params(
        self,
        query: Optional[str],
        location: Optional[str],
        max_results: int,
        sort_by: str,
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Construit les paramètres de recherche pour l'API"""
        params: Dict[str, Any] = {
            'limit': min(max_results, 100)  # VDAB limite généralement à 100
        }

        # Recherche par mots-clés
        if query:
            params['q'] = query

        # Localisation
        if location:
            params['plaats'] = location  # 'plaats' = lieu en néerlandais

        # Tri
        if sort_by == "date":
            params['sorteer'] = 'publicatiedatum:desc'
        elif sort_by == "relevance":
            params['sorteer'] = 'relevantie:desc'

        # Filtres additionnels
        if filters:
            params.update(filters)

        return params

    def _parse_response(self, data: Dict[str, Any]) -> List[VDABJobOffer]:
        """Parse la réponse JSON de l'API VDAB"""
        offers = []

        # Structure typique: { "vacatures": [...] } ou { "items": [...] }
        vacancies = data.get('vacatures') or data.get('items') or []

        for vacancy in vacancies:
            try:
                offer = self._parse_vacancy(vacancy)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.debug(f"Erreur parsing vacature: {e}")
                continue

        return offers

    def _parse_vacancy(self, vacancy: Dict[str, Any]) -> Optional[VDABJobOffer]:
        """Parse une vacature individuelle"""
        try:
            # ID
            vacancy_id = str(vacancy.get('id') or vacancy.get('vacaturenummer', ''))

            # Titre
            title = vacancy.get('titel') or vacancy.get('functienaam', 'N/A')

            # Entreprise
            company = vacancy.get('werkgever', {}).get('naam', 'N/A')
            if isinstance(company, dict):
                company = company.get('naam', 'N/A')

            # Localisation
            location_data = vacancy.get('werklocatie') or vacancy.get('plaats', {})
            if isinstance(location_data, dict):
                location = location_data.get('gemeente', 'N/A')
            else:
                location = str(location_data)

            # Description
            description = vacancy.get('omschrijving') or vacancy.get('functiebeschrijving', '')
            if isinstance(description, dict):
                description = description.get('tekst', '')

            # URL
            url = vacancy.get('url') or f"https://www.vdab.be/vindeenjob/vacatures/{vacancy_id}"

            # Date de publication
            posted_date = vacancy.get('publicatiedatum') or vacancy.get('aanmaakdatum')

            # Salaire (rarement disponible)
            salary = None
            if 'salaris' in vacancy:
                salary_data = vacancy['salaris']
                if isinstance(salary_data, dict):
                    salary = salary_data.get('omschrijving')

            # Type de contrat
            contract_type = vacancy.get('contractType') or vacancy.get('type')

            # Remote/télétravail
            remote = False
            if description:
                desc_lower = description.lower()
                remote = any(kw in desc_lower for kw in [
                    'thuiswerk', 'remote', 'télétravail', 'telewerk', 'work from home'
                ])

            # Champs spécifiques VDAB
            number_of_positions = vacancy.get('aantalOpenstaandeVacatures', 1)
            study_level = vacancy.get('studieniveau', {}).get('omschrijving')
            experience_required = vacancy.get('ervaring', {}).get('omschrijving')

            if not vacancy_id or not title:
                return None

            return VDABJobOffer(
                id=vacancy_id,
                title=title,
                company=company,
                location=location,
                description=description[:500],  # Limiter la taille
                url=url,
                posted_date=posted_date,
                salary=salary,
                contract_type=contract_type,
                remote=remote,
                number_of_positions=number_of_positions,
                study_level=study_level,
                experience_required=experience_required
            )

        except Exception as e:
            logger.error(f"Erreur parsing vacature: {e}")
            logger.debug(f"Données vacature: {vacancy}")
            return None

    def close(self):
        """Ferme la session"""
        self.session.close()

    def __enter__(self):
        """Support du context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup du context manager"""
        self.close()


# Exemple d'utilisation
if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    print("=" * 80)
    print("🇧🇪 VDAB API SCRAPER - SERVICE OFFICIEL FLAMAND")
    print("=" * 80)
    print()
    print("ℹ️  Pour utiliser cette API:")
    print("   1. Créez un compte sur https://developer.vdab.be/openservices/")
    print("   2. Créez une application pour obtenir votre Client ID")
    print("   3. Ajoutez VDAB_CLIENT_ID=votre_id dans config/credentials/vdab_credentials.env")
    print()
    print("=" * 80)
    print()

    # Tenter de charger les credentials
    load_dotenv('config/credentials/vdab_credentials.env')
    client_id = os.getenv('VDAB_CLIENT_ID')

    if not client_id:
        print("❌ Aucun Client ID trouvé.")
        print()
        print("📝 Créez le fichier: config/credentials/vdab_credentials.env")
        print("   Contenu:")
        print("   VDAB_CLIENT_ID=votre_client_id_ici")
        print()
    else:
        print(f"✅ Client ID trouvé: {client_id[:10]}...")
        print()

        # Test de l'API
        with VDABScraper(client_id=client_id) as scraper:
            try:
                offers = scraper.search(
                    query="Python Developer",
                    location="Brussel",
                    max_results=10
                )

                print(f"✅ {len(offers)} offres trouvées\n")

                for i, offer in enumerate(offers, 1):
                    print(f"{i}. {offer.title}")
                    print(f"   🏢 {offer.company}")
                    print(f"   📍 {offer.location}")
                    if offer.salary:
                        print(f"   💰 {offer.salary}")
                    if offer.remote:
                        print(f"   🏠 Remote/Thuiswerk")
                    if offer.number_of_positions and offer.number_of_positions > 1:
                        print(f"   👥 {offer.number_of_positions} postes")
                    print(f"   🔗 {offer.url[:80]}...")
                    print()

            except ValueError as e:
                print(f"❌ {e}")
            except Exception as e:
                print(f"❌ Erreur: {e}")
