"""
Tests unitaires pour le module jobboard_scraper
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.modules.detection.jobboard_scraper import (
    JobOffer,
    BaseJobBoardScraper,
    IndeedScraper
)


class TestJobOffer:
    """Tests pour la classe JobOffer"""

    def test_job_offer_creation(self):
        """Test de création d'une offre d'emploi"""
        offer = JobOffer(
            title="Python Developer",
            company="TechCorp",
            location="Paris",
            description="Great opportunity",
            url="https://example.com/job/123",
            source="Indeed"
        )

        assert offer.title == "Python Developer"
        assert offer.company == "TechCorp"
        assert offer.location == "Paris"
        assert offer.source == "Indeed"
        assert isinstance(offer.scraped_at, datetime)

    def test_job_offer_to_dict(self):
        """Test de conversion en dictionnaire"""
        offer = JobOffer(
            title="Backend Engineer",
            company="StartupXYZ",
            location="Remote",
            description="Work from anywhere",
            url="https://example.com/job/456",
            source="LinkedIn",
            salary="50-60k€",
            remote=True
        )

        offer_dict = offer.to_dict()

        assert offer_dict['title'] == "Backend Engineer"
        assert offer_dict['remote'] is True
        assert offer_dict['salary'] == "50-60k€"
        assert 'scraped_at' in offer_dict

    def test_remote_detection(self):
        """Test de détection du travail à distance"""
        offer = JobOffer(
            title="Developer",
            company="Company",
            location="Paris",
            description="Remote work available",
            url="https://example.com/job",
            source="Indeed",
            remote=True
        )

        assert offer.remote is True


class TestBaseJobBoardScraper:
    """Tests pour la classe de base BaseJobBoardScraper"""

    def test_initialization(self):
        """Test d'initialisation du scraper"""
        scraper = BaseJobBoardScraper(
            timeout=20,
            max_retries=5
        )

        assert scraper.timeout == 20
        assert scraper.max_retries == 5
        assert scraper.session is not None

    def test_random_user_agent(self):
        """Test de génération d'user agent aléatoire"""
        ua1 = BaseJobBoardScraper._get_random_user_agent()
        ua2 = BaseJobBoardScraper._get_random_user_agent()

        assert isinstance(ua1, str)
        assert len(ua1) > 0
        # Les user agents peuvent être différents (aléatoire)

    def test_rate_limit(self):
        """Test du rate limiting"""
        scraper = BaseJobBoardScraper(rate_limit_delay=(0.1, 0.2))

        import time
        start = time.time()
        scraper._apply_rate_limit()
        duration = time.time() - start

        # Le délai devrait être entre 0.1 et 0.2 secondes
        assert 0.1 <= duration <= 0.3  # Petite marge pour l'exécution

    def test_scrape_not_implemented(self):
        """Test que scrape() doit être implémenté"""
        scraper = BaseJobBoardScraper()

        with pytest.raises(NotImplementedError):
            scraper.scrape()


class TestIndeedScraper:
    """Tests pour le scraper Indeed"""

    @pytest.fixture
    def scraper(self):
        """Fixture pour créer un scraper Indeed"""
        return IndeedScraper(rate_limit_delay=(0.01, 0.02))

    @pytest.fixture
    def mock_html(self):
        """HTML de test simulant une page Indeed"""
        return """
        <html>
            <body>
                <div class="job_seen_beacon">
                    <h2 class="jobTitle">
                        <a href="/rc/clk?jk=123abc">Python Developer</a>
                    </h2>
                    <span class="companyName">TechCorp</span>
                    <div class="companyLocation">Paris, France</div>
                    <div class="job-snippet">
                        Looking for a Python developer with 3+ years experience.
                        Remote work available.
                    </div>
                    <div class="salary-snippet">45-55k€</div>
                    <span class="date">Il y a 2 jours</span>
                </div>
                <div class="job_seen_beacon">
                    <h2 class="jobTitle">
                        <a href="/rc/clk?jk=456def">Senior Backend Engineer</a>
                    </h2>
                    <span class="companyName">StartupXYZ</span>
                    <div class="companyLocation">Lyon, France</div>
                    <div class="job-snippet">
                        We are looking for a senior backend engineer.
                    </div>
                </div>
            </body>
        </html>
        """

    def test_scraper_initialization(self, scraper):
        """Test d'initialisation du scraper Indeed"""
        assert scraper.source == "Indeed"
        assert scraper.BASE_URL == "https://fr.indeed.com"

    def test_parse_search_page(self, scraper, mock_html):
        """Test du parsing d'une page de résultats"""
        offers = scraper._parse_search_page(mock_html)

        assert len(offers) == 2
        assert offers[0].title == "Python Developer"
        assert offers[0].company == "TechCorp"
        assert offers[0].location == "Paris, France"
        assert offers[0].salary == "45-55k€"
        assert offers[0].posted_date == "Il y a 2 jours"
        assert offers[0].remote is True  # Détecté dans la description

        assert offers[1].title == "Senior Backend Engineer"
        assert offers[1].company == "StartupXYZ"

    def test_parse_empty_page(self, scraper):
        """Test du parsing d'une page vide"""
        empty_html = "<html><body></body></html>"
        offers = scraper._parse_search_page(empty_html)

        assert len(offers) == 0

    @patch('src.modules.detection.jobboard_scraper.IndeedScraper._fetch_page')
    def test_scrape_with_mock(self, mock_fetch, scraper, mock_html):
        """Test du scraping complet avec mock"""
        # Simuler la réponse HTTP
        mock_response = Mock()
        mock_response.text = mock_html
        mock_fetch.return_value = mock_response

        # Scraper avec 1 page seulement
        offers = scraper.scrape(
            query="Python",
            location="Paris",
            max_pages=1
        )

        assert len(offers) == 2
        assert mock_fetch.called
        assert mock_fetch.call_count == 1

    @patch('src.modules.detection.jobboard_scraper.IndeedScraper._fetch_page')
    def test_scrape_pagination(self, mock_fetch, scraper, mock_html):
        """Test de la pagination"""
        mock_response = Mock()
        mock_response.text = mock_html
        mock_fetch.return_value = mock_response

        # Scraper avec 3 pages
        offers = scraper.scrape(
            query="Python",
            location="Paris",
            max_pages=3
        )

        # Should have called _fetch_page 3 times
        assert mock_fetch.call_count == 3

        # Vérifier les paramètres de pagination
        calls = mock_fetch.call_args_list
        assert calls[0][1]['params']['start'] == 0
        assert calls[1][1]['params']['start'] == 10
        assert calls[2][1]['params']['start'] == 20

    def test_parse_job_card_missing_fields(self, scraper):
        """Test du parsing avec champs manquants"""
        from bs4 import BeautifulSoup

        incomplete_html = """
        <div class="job_seen_beacon">
            <span class="companyName">Company</span>
        </div>
        """

        soup = BeautifulSoup(incomplete_html, 'lxml')
        card = soup.find('div', class_='job_seen_beacon')

        offer = scraper._parse_job_card(card)

        # Should return None if missing required fields
        assert offer is None

    @patch('src.modules.detection.jobboard_scraper.IndeedScraper._fetch_page')
    def test_get_job_details(self, mock_fetch, scraper):
        """Test de récupération des détails d'une offre"""
        detail_html = """
        <html>
            <div id="jobDescriptionText">
                <p>Full job description here...</p>
                <p>Requirements: Python, Django, PostgreSQL</p>
            </div>
        </html>
        """

        mock_response = Mock()
        mock_response.text = detail_html
        mock_fetch.return_value = mock_response

        details = scraper.get_job_details("https://fr.indeed.com/job/123")

        assert 'full_description' in details
        assert 'Python' in details['full_description']
        assert details['url'] == "https://fr.indeed.com/job/123"

    @patch('src.modules.detection.jobboard_scraper.IndeedScraper._fetch_page')
    def test_scrape_handles_errors(self, mock_fetch, scraper):
        """Test de gestion d'erreurs lors du scraping"""
        # Simuler une erreur réseau
        mock_fetch.side_effect = Exception("Network error")

        # Le scraping devrait continuer malgré l'erreur
        offers = scraper.scrape(
            query="Python",
            location="Paris",
            max_pages=2
        )

        # Should return empty list without crashing
        assert offers == []


class TestIntegration:
    """Tests d'intégration (nécessitent une connexion réseau)"""

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires network and may be slow")
    def test_real_indeed_scrape(self):
        """Test de scraping réel sur Indeed (à exécuter manuellement)"""
        scraper = IndeedScraper()

        offers = scraper.scrape(
            query="Python Developer",
            location="Paris",
            max_pages=1
        )

        assert len(offers) > 0
        assert all(isinstance(o, JobOffer) for o in offers)
        assert all(o.source == "Indeed" for o in offers)
