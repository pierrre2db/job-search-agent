"""
Module de scraping des job boards (Indeed, LinkedIn, etc.)

Ce module fournit des scrapers pour différentes plateformes d'emploi,
avec gestion de pagination, rate limiting et error handling.
"""

import logging
import time
import random
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode, urljoin
from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@dataclass
class JobOffer:
    """Représente une offre d'emploi scrapée"""

    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    contract_type: Optional[str] = None
    remote: bool = False
    scraped_at: datetime = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'offre en dictionnaire"""
        return {
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
            'scraped_at': self.scraped_at.isoformat()
        }


class BaseJobBoardScraper:
    """Classe de base pour tous les scrapers de job boards"""

    def __init__(
        self,
        user_agent: str = None,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: tuple = (2, 5)
    ):
        """
        Initialise le scraper

        Args:
            user_agent: User agent à utiliser pour les requêtes
            timeout: Timeout des requêtes en secondes
            max_retries: Nombre maximum de tentatives
            rate_limit_delay: Tuple (min, max) pour le délai aléatoire entre requêtes
        """
        self.user_agent = user_agent or self._get_random_user_agent()
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    @staticmethod
    def _get_random_user_agent() -> str:
        """Retourne un User-Agent aléatoire"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        ]
        return random.choice(user_agents)

    def _apply_rate_limit(self):
        """Applique un délai aléatoire pour respecter le rate limiting"""
        delay = random.uniform(*self.rate_limit_delay)
        logger.debug(f"Rate limiting: sleeping for {delay:.2f}s")
        time.sleep(delay)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch_page(self, url: str, params: Dict = None) -> requests.Response:
        """
        Récupère une page web avec retry automatique

        Args:
            url: URL à récupérer
            params: Paramètres de requête

        Returns:
            Response object

        Raises:
            requests.RequestException: En cas d'erreur de requête
        """
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise

    def scrape(self, **kwargs) -> List[JobOffer]:
        """
        Méthode abstraite à implémenter par chaque scraper

        Returns:
            Liste d'offres d'emploi
        """
        raise NotImplementedError("Subclasses must implement scrape()")


class IndeedScraper(BaseJobBoardScraper):
    """Scraper pour Indeed.fr"""

    BASE_URL = "https://fr.indeed.com"
    SEARCH_URL = f"{BASE_URL}/jobs"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Indeed"

    def scrape(
        self,
        query: str,
        location: str = "Paris",
        max_pages: int = 5,
        radius: int = 25
    ) -> List[JobOffer]:
        """
        Scrape des offres sur Indeed

        Args:
            query: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris")
            max_pages: Nombre maximum de pages à scraper
            radius: Rayon de recherche en km

        Returns:
            Liste d'offres d'emploi
        """
        logger.info(f"Starting Indeed scrape: query='{query}', location='{location}'")

        all_offers = []

        for page in range(max_pages):
            try:
                # Construire les paramètres de recherche
                start = page * 10  # Indeed affiche 10 résultats par page
                params = {
                    'q': query,
                    'l': location,
                    'radius': radius,
                    'start': start,
                    'sort': 'date'  # Trier par date
                }

                logger.info(f"Fetching page {page + 1}/{max_pages} (start={start})")

                # Récupérer la page
                response = self._fetch_page(self.SEARCH_URL, params=params)

                # Parser les offres
                offers = self._parse_search_page(response.text)

                if not offers:
                    logger.info(f"No more offers found on page {page + 1}")
                    break

                all_offers.extend(offers)
                logger.info(f"Found {len(offers)} offers on page {page + 1}")

                # Rate limiting entre les pages
                if page < max_pages - 1:
                    self._apply_rate_limit()

            except Exception as e:
                logger.error(f"Error scraping page {page + 1}: {e}")
                continue

        logger.info(f"Scraping complete: {len(all_offers)} total offers found")
        return all_offers

    def _parse_search_page(self, html: str) -> List[JobOffer]:
        """
        Parse une page de résultats de recherche Indeed

        Args:
            html: HTML de la page

        Returns:
            Liste d'offres d'emploi
        """
        soup = BeautifulSoup(html, 'lxml')
        offers = []

        # Indeed utilise des balises avec des classes spécifiques
        # Note: Ces sélecteurs peuvent changer, il faut les adapter si nécessaire
        job_cards = soup.find_all('div', class_='job_seen_beacon')

        if not job_cards:
            # Fallback: essayer un autre sélecteur
            job_cards = soup.find_all('td', class_='resultContent')

        for card in job_cards:
            try:
                offer = self._parse_job_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"Error parsing job card: {e}")
                continue

        return offers

    def _parse_job_card(self, card) -> Optional[JobOffer]:
        """
        Parse une carte d'offre individuelle

        Args:
            card: BeautifulSoup element

        Returns:
            JobOffer ou None si parsing échoue
        """
        try:
            # Titre
            title_elem = card.find('h2', class_='jobTitle')
            if not title_elem:
                title_elem = card.find('a', class_='jcs-JobTitle')
            title = title_elem.get_text(strip=True) if title_elem else None

            # URL
            link_elem = title_elem.find('a') if title_elem else None
            if not link_elem and title_elem.name == 'a':
                link_elem = title_elem
            job_url = urljoin(self.BASE_URL, link_elem['href']) if link_elem else None

            # Entreprise
            company_elem = card.find('span', class_='companyName')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"

            # Localisation
            location_elem = card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            # Description (snippet)
            description_elem = card.find('div', class_='job-snippet')
            description = description_elem.get_text(strip=True) if description_elem else ""

            # Salaire (optionnel)
            salary_elem = card.find('div', class_='salary-snippet')
            salary = salary_elem.get_text(strip=True) if salary_elem else None

            # Date de publication (optionnel)
            date_elem = card.find('span', class_='date')
            posted_date = date_elem.get_text(strip=True) if date_elem else None

            # Remote detection
            remote = 'remote' in description.lower() or 'télétravail' in description.lower()

            if not title or not job_url:
                logger.warning("Missing required fields (title or URL)")
                return None

            return JobOffer(
                title=title,
                company=company,
                location=location,
                description=description,
                url=job_url,
                source=self.source,
                posted_date=posted_date,
                salary=salary,
                remote=remote
            )

        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None

    def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """
        Récupère les détails complets d'une offre

        Args:
            job_url: URL de l'offre

        Returns:
            Dictionnaire avec les détails de l'offre
        """
        try:
            response = self._fetch_page(job_url)
            soup = BeautifulSoup(response.text, 'lxml')

            # Description complète
            description_elem = soup.find('div', id='jobDescriptionText')
            full_description = description_elem.get_text(strip=True) if description_elem else ""

            # Autres détails peuvent être extraits ici

            return {
                'full_description': full_description,
                'url': job_url
            }

        except Exception as e:
            logger.error(f"Error fetching job details from {job_url}: {e}")
            return {}


# Exemple d'usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    scraper = IndeedScraper()
    offers = scraper.scrape(
        query="Python Developer",
        location="Paris",
        max_pages=2
    )

    print(f"\n✅ Found {len(offers)} job offers\n")

    for i, offer in enumerate(offers[:5], 1):
        print(f"{i}. {offer.title} @ {offer.company}")
        print(f"   📍 {offer.location}")
        print(f"   🔗 {offer.url}")
        print()
