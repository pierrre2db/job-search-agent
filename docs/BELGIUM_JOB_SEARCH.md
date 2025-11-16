# Recherche d'Emploi en Belgique 🇧🇪

Guide complet des sources d'offres d'emploi en Belgique et leur intégration dans le projet.

---

## 🎯 Sites d'emploi belges

### 1. Indeed Belgique (✅ IMPLÉMENTÉ)

**URL:** https://be.indeed.com

**Status:** ✅ Scraper fonctionnel avec bypass Cloudflare

**Utilisation:**
```python
from src.modules.detection.indeed_bypass import IndeedBypassScraper

# Mode non-headless (recommandé)
with IndeedBypassScraper(headless=False, country='be') as scraper:
    offers = scraper.scrape(
        query="Python Developer",
        location="Bruxelles",  # ou "Liège", "Anvers", "Belgique"
        max_pages=3
    )
```

**Villes principales:**
- Bruxelles (Brussels/Brussel)
- Liège
- Anvers (Antwerpen)
- Gand (Gent)
- Charleroi
- Namur
- Louvain (Leuven)

**Résultats tests:**
- ✅ 16 offres extraites à Bruxelles
- ✅ Détection remote/télétravail fonctionnelle
- ✅ Bypass Cloudflare réussi

**Limitations:**
- Salaires rarement affichés (0% dans nos tests)
- Mode headless problématique
- Nécessite environnement graphique

---

### 2. StepStone Belgium

**URL:** https://www.stepstone.be

**Avantages:**
- Grand volume d'offres IT
- Bonne couverture Belgique et pays voisins
- Interface propre, facile à scraper

**API:** Pas d'API publique connue

**Scraping:** À implémenter (structure HTML similaire à Indeed)

**Priorité:** 🔸 Moyenne (alternative solide à Indeed)

---

### 3. Jobat.be

**URL:** https://www.jobat.be

**Avantages:**
- Site belge populaire
- Bonne couverture des grandes entreprises
- Filtres par région/langue

**API:** Pas d'API publique

**Scraping:** À implémenter

**Priorité:** 🔸 Moyenne

---

### 4. Services publics d'emploi

#### 4.1 VDAB (Flandre) 🔴 Priorité haute

**URL:** https://www.vdab.be

**Avantages:**
- ✅ **API publique disponible!**
- Service officiel flamand
- Gratuit et légal
- Données structurées

**API Documentation:**
- https://www.vdab.be/vdab/developers
- Endpoint: https://api.vdab.be/v1/jobs

**Inscription:**
1. Créer un compte sur https://www.vdab.be/vdab/developers
2. Obtenir une clé API
3. Quota: ~1000 requêtes/jour (gratuit)

**À implémenter en priorité pour usage légal!**

#### 4.2 Forem (Wallonie)

**URL:** https://www.leforem.be

**API:** Limitée, principalement pour partenaires

**Priorité:** 🔸 Moyenne (si on trouve une API)

#### 4.3 Actiris (Bruxelles)

**URL:** https://www.actiris.brussels

**API:** Pas d'API publique grand public

**Priorité:** 🔹 Basse

---

### 5. LinkedIn Jobs Belgium

**URL:** https://www.linkedin.com/jobs/search/?location=Belgium

**Avantages:**
- Très populaire en Belgique
- Réseau professionnel intégré
- Offres de qualité

**Limitations:**
- Scraping très difficile (protection forte)
- Risque de ban élevé
- Nécessite compte LinkedIn

**Priorité:** 🔹 Basse (trop risqué)

---

### 6. Glassdoor Belgium

**URL:** https://www.glassdoor.be

**Avantages:**
- Avis entreprises + salaires
- Utile pour scoring des offres

**Limitations:**
- Scraping difficile
- Volume d'offres limité

**Priorité:** 🔹 Basse

---

## 🚀 Stratégie recommandée pour la Belgique

### Phase 1: Solution immédiate (actuelle)

```
✅ Indeed BE (be.indeed.com) via scraper avec bypass
   - Mode non-headless
   - 3-5 pages/jour max
   - Villes: Bruxelles, Liège, Anvers
```

### Phase 2: Solution légale (à implémenter - Sprint 2)

```
1. API VDAB (Flandre) - PRIORITÉ HAUTE
   └─ Gratuit, légal, ~1000 req/jour

2. Parser emails Gmail Indeed
   └─ Vos propres alertes emploi

3. StepStone scraper (si besoin)
   └─ Alternative à Indeed
```

### Phase 3: Optimisations (Sprint 3)

```
1. Agrégation multi-sources
2. Déduplication des offres
3. Scoring adapté au marché belge
```

---

## 📝 Configuration pour la Belgique

### Localisation et langue

**Belgique = 3 régions linguistiques:**

| Région | Langue | Ville principale |
|--------|--------|------------------|
| Flandre | Néerlandais | Anvers, Gand |
| Wallonie | Français | Liège, Charleroi |
| Bruxelles | Bilingue FR/NL | Bruxelles |

**Impact sur la recherche:**
- Indeed BE: Offres en FR et NL mélangées
- VDAB: Principalement NL
- Forem: Principalement FR

**Configuration recommandée:**
```python
# Pour couvrir toute la Belgique
locations = [
    "Bruxelles",    # Centre, bilingue
    "Belgique",     # Recherche nationale
    "Liège",        # Wallonie
    "Anvers"        # Flandre
]
```

### Salaires en Belgique (IT)

**Fourchettes indicatives:**

| Poste | Junior | Médian | Senior |
|-------|--------|--------|--------|
| Python Dev | 35-45k€ | 50-65k€ | 70-90k€ |
| Full Stack | 40-50k€ | 55-70k€ | 75-95k€ |
| DevOps | 45-55k€ | 60-75k€ | 80-100k€ |
| Data Scientist | 45-55k€ | 65-80k€ | 85-110k€ |

**Note:** Salaires nets car charges sociales élevées en Belgique

### Télétravail en Belgique

**Tendances post-COVID:**
- Hybride très répandu (2-3 jours remote)
- Full remote: ~15-20% des offres IT
- Secteur public: moins flexible
- Startups/scale-ups: plus flexible

---

## 🔧 Implémentation VDAB API (TODO - Sprint 2)

### Exemple de code (à créer)

```python
# src/modules/detection/vdab_api.py

import requests
from typing import List
from dataclasses import dataclass

@dataclass
class VDABJobOffer:
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str = "VDAB"

class VDABScraper:
    BASE_URL = "https://api.vdab.be/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def search(
        self,
        query: str,
        location: str = "Vlaanderen",
        max_results: int = 50
    ) -> List[VDABJobOffer]:
        """
        Recherche d'offres via l'API VDAB

        Args:
            query: Mots-clés (ex: "Python Developer")
            location: Région ("Vlaanderen", "Brussel", etc.)
            max_results: Nombre max de résultats

        Returns:
            Liste d'offres VDAB
        """
        endpoint = f"{self.BASE_URL}/jobs"
        params = {
            'q': query,
            'location': location,
            'limit': max_results
        }

        response = requests.get(
            endpoint,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()

        data = response.json()

        offers = []
        for job in data.get('jobs', []):
            offers.append(VDABJobOffer(
                title=job['title'],
                company=job.get('company', 'N/A'),
                location=job.get('location', 'N/A'),
                description=job.get('description', ''),
                url=job.get('url', '')
            ))

        return offers
```

**Usage:**
```python
from src.modules.detection.vdab_api import VDABScraper

scraper = VDABScraper(api_key="votre_clé_vdab")
offers = scraper.search("Python Developer", location="Brussel")

for offer in offers:
    print(f"{offer.title} @ {offer.company}")
```

---

## 📊 Comparaison des sources belges

| Source | API | Gratuit | Légal | Volume | Qualité | Priorité |
|--------|-----|---------|-------|--------|---------|----------|
| **Indeed BE** | ❌ | ✅ | ⚠️ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🔴 Haute |
| **VDAB** | ✅ | ✅ | ✅ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🔴 Haute |
| **StepStone BE** | ❌ | ✅ | ⚠️ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🔸 Moyenne |
| **Jobat** | ❌ | ✅ | ⚠️ | ⭐⭐⭐ | ⭐⭐⭐ | 🔸 Moyenne |
| **Gmail parsing** | ✅ | ✅ | ✅ | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 Haute |
| **LinkedIn** | ❌ | ✅ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🔹 Basse |

**Légende:**
- 🔴 Haute: À implémenter maintenant
- 🔸 Moyenne: À considérer si besoin
- 🔹 Basse: Nice to have

---

## 🎯 Roadmap Belgique

### Sprint 1 (Actuel) ✅
- [x] Indeed BE scraper opérationnel
- [x] Test sur Bruxelles, Liège, Anvers
- [x] Documentation marché belge

### Sprint 2 (Prochain)
- [ ] Implémenter VDAB API (Flandre)
- [ ] Parser emails Gmail Indeed
- [ ] Tester StepStone BE scraping
- [ ] Système de fallback automatique

### Sprint 3 (Futur)
- [ ] Agrégateur multi-sources
- [ ] Déduplication intelligente
- [ ] Scoring adapté marché belge
- [ ] Support Forem API (si disponible)

---

## 💡 Recommandations finales

**Pour un usage quotidien en Belgique:**

1. **Court terme (maintenant):**
   ```python
   # Indeed BE en mode visible, limité
   scraper = IndeedBypassScraper(headless=False, country='be')
   offers = scraper.scrape("Python", "Bruxelles", max_pages=3)
   ```

2. **Moyen terme (Sprint 2):**
   ```python
   # Combiner VDAB API + Gmail parsing
   vdab_offers = vdab_scraper.search("Python", "Brussel")
   gmail_offers = gmail_parser.parse_indeed_emails()
   all_offers = vdab_offers + gmail_offers
   ```

3. **Long terme (Sprint 3):**
   ```python
   # Agrégateur intelligent
   aggregator = BelgianJobAggregator()
   offers = aggregator.search(
       query="Python Developer",
       sources=['indeed', 'vdab', 'stepstone', 'gmail'],
       location="Bruxelles"
   )
   ```

---

## 📞 Ressources

### APIs officielles
- VDAB Developers: https://www.vdab.be/vdab/developers
- Forem: https://www.leforem.be (contacter support)
- Actiris: https://www.actiris.brussels (pas d'API publique)

### Documentation
- Marché IT belge: https://www.stepstone.be/salary-report
- Télétravail en Belgique: https://emploi.belgique.be/fr/themes/contrats-de-travail/teletravail

### Support
- Email: pierre2db@gmail.com
- Tel: 0499/45 54 45

---

**Dernière mise à jour:** 2025-11-16
**Status:** ✅ Indeed BE opérationnel, VDAB API à implémenter
