"""
Scraper Indeed avec bypass Cloudflare
Utilise undetected-chromedriver pour éviter la détection

⚠️ AVERTISSEMENT : Le scraping d'Indeed peut violer leurs Terms of Service.
Utilisez cette solution à vos propres risques.
Pour un usage légal, préférez l'API Pole Emploi ou le parsing d'emails.
"""

import logging
import time
import random
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("❌ undetected-chromedriver non installé")
    print("Installez-le avec : pip install undetected-chromedriver")
    raise

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class JobOffer:
    """Représente une offre d'emploi"""
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str = "Indeed"
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    remote: bool = False
    scraped_at: datetime = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()


class IndeedBypassScraper:
    """
    Scraper Indeed avec bypass Cloudflare
    Utilise undetected-chromedriver pour simuler un navigateur réel
    """

    BASE_URL = "https://fr.indeed.com"
    SEARCH_URL = f"{BASE_URL}/jobs"

    def __init__(self, headless: bool = True, verbose: bool = False):
        """
        Initialise le scraper avec bypass Cloudflare

        Args:
            headless: Exécuter Chrome en mode invisible (True recommandé)
            verbose: Activer les logs détaillés
        """
        self.headless = headless
        self.verbose = verbose
        self.driver = None

    def _init_driver(self):
        """Initialise le driver Chrome non détectable"""
        logger.info("Initialisation du driver Chrome...")

        options = uc.ChromeOptions()

        if self.headless:
            options.add_argument('--headless=new')  # Nouveau mode headless

        # Arguments anti-détection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        # Désactiver les logs si pas verbose
        if not self.verbose:
            options.add_argument('--log-level=3')
            options.add_argument('--silent')

        # Créer le driver
        self.driver = uc.Chrome(options=options)
        logger.info("✅ Driver Chrome initialisé")

    def _apply_stealth(self):
        """Applique des techniques de stealth supplémentaires"""
        # Supprimer les traces d'automation
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _human_behavior(self):
        """Simule un comportement humain"""
        # Scroll aléatoire
        scroll_amount = random.randint(100, 500)
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount})")

        # Délai aléatoire
        time.sleep(random.uniform(0.5, 1.5))

    def _accept_cookies(self):
        """Accepte automatiquement les cookies si la bannière apparaît"""
        try:
            # Chercher le bouton "Tout accepter" ou "Autoriser tous les cookies"
            accept_buttons = [
                "//button[contains(text(), 'Tout accepter')]",
                "//button[contains(text(), 'Autoriser tous les cookies')]",
                "//button[@id='onetrust-accept-btn-handler']",
                "//button[contains(@class, 'accept')]"
            ]

            for xpath in accept_buttons:
                try:
                    button = self.driver.find_element(By.XPATH, xpath)
                    button.click()
                    logger.info("✅ Cookies acceptés")
                    time.sleep(1)
                    return
                except:
                    continue

        except Exception as e:
            logger.debug(f"Pas de bannière cookies ou déjà acceptée: {e}")

    def scrape(
        self,
        query: str,
        location: str = "Paris",
        max_pages: int = 3
    ) -> List[JobOffer]:
        """
        Scrape des offres sur Indeed avec bypass Cloudflare

        Args:
            query: Mots-clés de recherche
            location: Localisation
            max_pages: Nombre maximum de pages

        Returns:
            Liste d'offres d'emploi
        """
        logger.info(f"🚀 Démarrage scraping Indeed : '{query}' à {location}")

        if self.driver is None:
            self._init_driver()
            self._apply_stealth()

        all_offers = []

        for page in range(max_pages):
            try:
                # Construire l'URL
                start = page * 10
                url = f"{self.SEARCH_URL}?q={query}&l={location}&start={start}&sort=date"

                logger.info(f"📄 Page {page + 1}/{max_pages} : {url}")

                # Naviguer vers la page
                self.driver.get(url)

                # Attendre le chargement initial
                time.sleep(random.uniform(3, 5))

                # Accepter les cookies (première page seulement)
                if page == 0:
                    self._accept_cookies()

                # Attendre que les offres se chargent
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                    )
                    logger.debug("✅ Offres chargées")
                except TimeoutException:
                    logger.warning("⏱️ Timeout: offres non chargées")

                # Vérifier si Cloudflare nous bloque
                page_text = self.driver.page_source.lower()
                if "cloudflare" in page_text and "challenge" in page_text:
                    logger.warning("⚠️ Cloudflare challenge détecté, attente...")
                    time.sleep(8)  # Attendre que le challenge se résolve

                # Simuler comportement humain
                self._human_behavior()

                # Récupérer le HTML
                html = self.driver.page_source

                # Parser les offres
                offers = self._parse_page(html)

                if not offers:
                    logger.warning(f"Aucune offre trouvée sur la page {page + 1}")
                    # Ne pas break immédiatement, peut être un problème temporaire
                    if page == 0:
                        # Si première page sans résultats, arrêter
                        break

                all_offers.extend(offers)
                logger.info(f"✅ {len(offers)} offres trouvées sur page {page + 1}")

                # Délai entre pages (important !)
                if page < max_pages - 1:
                    delay = random.uniform(4, 8)
                    logger.debug(f"Attente de {delay:.1f}s avant page suivante...")
                    time.sleep(delay)

            except Exception as e:
                logger.error(f"❌ Erreur page {page + 1}: {e}")
                continue

        logger.info(f"🎉 Scraping terminé : {len(all_offers)} offres au total")
        return all_offers

    def _parse_page(self, html: str) -> List[JobOffer]:
        """Parse une page de résultats"""
        soup = BeautifulSoup(html, 'lxml')
        offers = []

        # Chercher les cartes d'offres
        job_cards = soup.find_all('div', class_='job_seen_beacon')

        if not job_cards:
            # Fallback: autre sélecteur
            job_cards = soup.find_all('td', class_='resultContent')

        for card in job_cards:
            try:
                offer = self._parse_job_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.debug(f"Erreur parsing carte: {e}")
                continue

        return offers

    def _parse_job_card(self, card) -> Optional[JobOffer]:
        """Parse une carte d'offre individuelle"""
        try:
            # Titre - plusieurs sélecteurs possibles
            title = None
            title_elem = card.find('h2', class_='jobTitle')
            if title_elem:
                # Le titre peut être dans un <a> ou <span> à l'intérieur
                link_in_title = title_elem.find('a')
                span_in_title = title_elem.find('span')
                title = (link_in_title or span_in_title or title_elem).get_text(strip=True)

            if not title:
                # Fallback
                title_elem = card.find('a', class_='jcs-JobTitle')
                title = title_elem.get_text(strip=True) if title_elem else None

            # URL - chercher le lien dans le titre
            job_url = None
            link_elem = card.find('h2', class_='jobTitle')
            if link_elem:
                link = link_elem.find('a')
                if link and link.get('href'):
                    href = link['href']
                    # Nettoyer l'URL (Indeed ajoute parfois des paramètres)
                    if href.startswith('/'):
                        job_url = f"{self.BASE_URL}{href.split('?')[0]}"
                    elif href.startswith('http'):
                        job_url = href.split('?')[0]

            # Si pas trouvé, chercher autrement
            if not job_url:
                link = card.find('a', href=True)
                if link:
                    href = link['href']
                    if '/rc/clk' in href or '/viewjob' in href or '/company' in href:
                        job_url = f"{self.BASE_URL}{href.split('?')[0]}" if href.startswith('/') else href

            # Entreprise
            company = "N/A"
            company_elem = card.find('span', {'data-testid': 'company-name'})
            if not company_elem:
                company_elem = card.find('span', class_='companyName')
            if company_elem:
                company = company_elem.get_text(strip=True)

            # Localisation
            location = "N/A"
            location_elem = card.find('div', {'data-testid': 'text-location'})
            if not location_elem:
                location_elem = card.find('div', class_='companyLocation')
            if location_elem:
                location = location_elem.get_text(strip=True)

            # Description
            description = ""
            desc_elem = card.find('div', class_='job-snippet')
            if not desc_elem:
                desc_elem = card.find('div', {'class': lambda x: x and 'snippet' in x.lower()})
            if desc_elem:
                # Enlever les <li> et garder le texte
                for li in desc_elem.find_all('li'):
                    li.replace_with(li.get_text() + ' ')
                description = desc_elem.get_text(strip=True)

            # Salaire
            salary = None
            salary_elem = card.find('div', class_='salary-snippet')
            if not salary_elem:
                salary_elem = card.find('div', {'class': lambda x: x and 'salary' in x.lower()})
            if salary_elem:
                salary = salary_elem.get_text(strip=True)

            # Date
            posted_date = None
            date_elem = card.find('span', class_='date')
            if not date_elem:
                date_elem = card.find('span', {'class': lambda x: x and 'date' in x.lower()})
            if date_elem:
                posted_date = date_elem.get_text(strip=True)

            # Remote
            text_to_check = (title + ' ' + description + ' ' + location).lower()
            remote = any(keyword in text_to_check for keyword in ['remote', 'télétravail', 'teletravail', 'distance'])

            # Vérifier qu'on a au moins un titre
            if not title:
                logger.debug("Carte sans titre, ignorée")
                return None

            # Créer une URL par défaut si pas trouvée
            if not job_url:
                logger.debug(f"Pas d'URL pour: {title}, ignorée")
                return None

            return JobOffer(
                title=title,
                company=company,
                location=location,
                description=description[:500],  # Limiter la taille
                url=job_url,
                posted_date=posted_date,
                salary=salary,
                remote=remote
            )

        except Exception as e:
            logger.debug(f"Erreur parsing carte: {e}")
            return None

    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver fermé")

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()


# Exemple d'utilisation
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 80)
    print("🔓 SCRAPER INDEED AVEC BYPASS CLOUDFLARE")
    print("=" * 80)
    print()
    print("⚠️  AVERTISSEMENT :")
    print("   - Le scraping d'Indeed peut violer leurs Terms of Service")
    print("   - Utilisez à vos propres risques")
    print("   - Pour un usage légal, utilisez l'API Pole Emploi")
    print()
    print("=" * 80)
    print()

    # Utiliser le context manager
    with IndeedBypassScraper(headless=True, verbose=True) as scraper:
        offers = scraper.scrape(
            query="Python Developer",
            location="Paris",
            max_pages=2
        )

        print(f"\n✅ {len(offers)} offres trouvées\n")

        for i, offer in enumerate(offers[:5], 1):
            print(f"{i}. {offer.title}")
            print(f"   🏢 {offer.company}")
            print(f"   📍 {offer.location}")
            if offer.salary:
                print(f"   💰 {offer.salary}")
            print(f"   🔗 {offer.url[:80]}...")
            print()
