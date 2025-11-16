# Module Detection - Documentation

Le module **Detection** est responsable du scraping, parsing et scoring des offres d'emploi provenant de multiples sources.

---

## 📋 Vue d'ensemble

### Responsabilités

1. **Scraping multi-source** : Indeed, LinkedIn, Pole Emploi, etc.
2. **Parsing intelligent** : Extraction d'informations structurées
3. **Scoring** : Évaluation de la pertinence des offres
4. **Rate limiting** : Respect des limitations des plateformes

### Architecture

```
src/modules/detection/
├── __init__.py
├── jobboard_scraper.py      # Scrapers pour job boards
├── email_parser.py           # Parser d'emails (à venir)
├── scoring_engine.py         # Moteur de scoring (à venir)
└── tests/
    └── test_jobboard_scraper.py
```

---

## 🔍 Jobboard Scraper

### Classes principales

#### `JobOffer`

Dataclass représentant une offre d'emploi.

**Attributs :**
```python
@dataclass
class JobOffer:
    title: str                    # Titre du poste
    company: str                  # Nom de l'entreprise
    location: str                 # Localisation
    description: str              # Description (snippet)
    url: str                      # URL de l'offre
    source: str                   # Source (Indeed, LinkedIn, etc.)
    posted_date: Optional[str]    # Date de publication
    salary: Optional[str]         # Fourchette salariale
    contract_type: Optional[str]  # Type de contrat
    remote: bool                  # Travail à distance
    scraped_at: datetime          # Date du scraping
```

**Méthodes :**
- `to_dict()` : Convertit l'offre en dictionnaire

#### `BaseJobBoardScraper`

Classe de base pour tous les scrapers.

**Features :**
- User-Agent rotation automatique
- Rate limiting configurable
- Retry automatique avec exponential backoff
- Session HTTP persistante

**Initialisation :**
```python
scraper = BaseJobBoardScraper(
    user_agent="Mozilla/5.0 ...",  # Optionnel
    timeout=30,                     # Timeout des requêtes (s)
    max_retries=3,                  # Nombre de tentatives
    rate_limit_delay=(2, 5)         # Délai aléatoire (min, max)
)
```

#### `IndeedScraper`

Scraper spécialisé pour Indeed.fr

**Utilisation de base :**
```python
from src.modules.detection.jobboard_scraper import IndeedScraper

# Initialiser le scraper
scraper = IndeedScraper()

# Scraper des offres
offers = scraper.scrape(
    query="Python Developer",
    location="Paris",
    max_pages=5,
    radius=25  # Rayon en km
)

# Afficher les résultats
for offer in offers:
    print(f"{offer.title} @ {offer.company}")
    print(f"URL: {offer.url}")
```

**Paramètres de `scrape()` :**

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `query` | str | *requis* | Mots-clés de recherche |
| `location` | str | "Paris" | Localisation |
| `max_pages` | int | 5 | Nombre de pages à scraper |
| `radius` | int | 25 | Rayon de recherche (km) |

**Méthodes avancées :**

```python
# Récupérer les détails complets d'une offre
details = scraper.get_job_details("https://fr.indeed.com/job/abc123")
print(details['full_description'])
```

---

## 🎯 Exemples d'utilisation

### Exemple 1 : Scraping simple

```python
from src.modules.detection.jobboard_scraper import IndeedScraper

scraper = IndeedScraper()

offers = scraper.scrape(
    query="Data Scientist",
    location="Lyon",
    max_pages=3
)

print(f"Trouvé {len(offers)} offres")

# Filtrer les offres remote
remote_offers = [o for o in offers if o.remote]
print(f"{len(remote_offers)} offres en remote")
```

### Exemple 2 : Scraping avec configuration personnalisée

```python
scraper = IndeedScraper(
    timeout=60,
    max_retries=5,
    rate_limit_delay=(3, 7)  # Plus prudent
)

offers = scraper.scrape(
    query="DevOps Engineer",
    location="Remote",
    max_pages=10
)

# Sauvegarder en JSON
import json

offers_data = [o.to_dict() for o in offers]
with open('offers.json', 'w') as f:
    json.dump(offers_data, f, indent=2, ensure_ascii=False)
```

### Exemple 3 : Récupération des détails

```python
scraper = IndeedScraper()

# Scraper les offres
offers = scraper.scrape("Full Stack Developer", "Paris", max_pages=1)

# Récupérer les détails de la première offre
if offers:
    details = scraper.get_job_details(offers[0].url)
    print(f"Description complète:\n{details['full_description']}")
```

---

## ⚙️ Configuration

### Rate Limiting

Le rate limiting est essentiel pour éviter d'être banni.

**Configuration recommandée :**

| Plateforme | Délai (s) | Max pages | Notes |
|------------|-----------|-----------|-------|
| Indeed | 2-5 | 10 | Strict sur rate limiting |
| LinkedIn | 3-7 | 5 | Très strict |
| Pole Emploi | 1-3 | 20 | Plus permissif (API) |

**Personnalisation :**
```python
# Très prudent (éviter ban)
scraper = IndeedScraper(rate_limit_delay=(5, 10))

# Rapide (risque de ban)
scraper = IndeedScraper(rate_limit_delay=(0.5, 1))
```

### User-Agent Rotation

Le scraper utilise automatiquement une liste de User-Agents réalistes.

**User-Agents inclus :**
- Chrome (Windows, macOS, Linux)
- Firefox (Windows, macOS)
- Safari (macOS)

**Personnalisation :**
```python
scraper = IndeedScraper(
    user_agent="Mozilla/5.0 (Custom) ..."
)
```

---

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest src/modules/detection/tests/ -v

# Avec couverture
pytest src/modules/detection/tests/ --cov=src.modules.detection

# Tests unitaires uniquement (rapide)
pytest src/modules/detection/tests/ -v -m "not integration"

# Tests d'intégration (nécessite réseau)
pytest src/modules/detection/tests/ -v -m integration
```

### Tests disponibles

| Test | Type | Description |
|------|------|-------------|
| `test_job_offer_creation` | Unit | Création d'objet JobOffer |
| `test_parse_search_page` | Unit | Parsing HTML |
| `test_scrape_with_mock` | Unit | Scraping avec mock |
| `test_scrape_pagination` | Unit | Pagination |
| `test_real_indeed_scrape` | Integration | Scraping réel (skip par défaut) |

---

## 🐛 Troubleshooting

### Problème : Aucune offre trouvée

**Causes possibles :**
1. Sélecteurs HTML changés (Indeed modifie régulièrement sa structure)
2. Blocage IP (trop de requêtes)
3. Query trop spécifique

**Solutions :**
```python
# 1. Activer le logging pour debug
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. Augmenter le délai
scraper = IndeedScraper(rate_limit_delay=(5, 10))

# 3. Essayer une query plus générale
offers = scraper.scrape("Developer", "Paris", max_pages=1)
```

### Problème : Erreur 403 Forbidden

**Cause :** Indeed détecte le scraping.

**Solutions :**
1. Augmenter `rate_limit_delay`
2. Utiliser un proxy
3. Attendre quelques heures avant de recommencer

```python
# Avec proxy (à implémenter)
scraper.session.proxies = {
    'http': 'http://proxy.com:8080',
    'https': 'http://proxy.com:8080'
}
```

### Problème : Timeout

**Cause :** Connexion lente ou serveur surchargé.

**Solution :**
```python
scraper = IndeedScraper(timeout=60)
```

---

## 📊 Performance

### Benchmarks

Tests effectués sur une connexion 100 Mbps :

| Pages | Offres | Temps | Offres/s |
|-------|--------|-------|----------|
| 1 | 10 | 5s | 2.0 |
| 5 | 50 | 35s | 1.4 |
| 10 | 100 | 80s | 1.25 |

**Note :** Le temps inclut le rate limiting (2-5s entre pages).

### Optimisations possibles

1. **Scraping parallèle** : Utiliser asyncio pour scraper plusieurs pages en parallèle
2. **Caching** : Mettre en cache les résultats pour éviter de re-scraper
3. **Proxies** : Utiliser un pool de proxies pour augmenter le débit

---

## 🔜 Prochaines évolutions

- [ ] Support de LinkedIn scraping
- [ ] Support de Pole Emploi API
- [ ] Support de Welcome to the Jungle
- [ ] Scraping asynchrone (asyncio)
- [ ] Pool de proxies automatique
- [ ] Détection automatique de changements HTML
- [ ] Export vers base de données

---

## 📚 Ressources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Tenacity (Retry) Documentation](https://tenacity.readthedocs.io/)

---
