# Setup Job Boards APIs - Tutoriel Complet

Guide pour obtenir les clés API des différents sites d'emploi.

---

## 🎯 Plateformes supportées

1. **Indeed** - Leader mondial
2. **LinkedIn Jobs** - Réseau professionnel
3. **Welcome to the Jungle** - Startups et scale-ups
4. **Apec** - Cadres (France)
5. **Glassdoor** - Avis entreprises + offres

---

## 📋 1. Indeed API

### Inscription

**⚠️ Note :** Indeed a fermé son API publique en 2023. Alternatives :

#### Option A : Scraping (recommandé)
```python
# Utiliser BeautifulSoup + Selenium pour scraper
# Voir : src/modules/detection/jobboard_scraper.py
```

#### Option B : Partenariat Indeed
- Contactez Indeed pour un accès partenaire
- URL : https://indeed.com/partnerships
- Réservé aux entreprises avec volume important

### Configuration (si vous avez accès)
```bash
# Dans config/credentials/api_keys.env
INDEED_API_KEY=votre-cle-ici
INDEED_PUBLISHER_ID=votre-publisher-id
```

---

## 📋 2. LinkedIn Jobs API

### Pré-requis
- Compte LinkedIn Developer
- Application LinkedIn créée

### Étapes

1. **Créer une application LinkedIn**
   - URL : https://www.linkedin.com/developers/apps
   - Cliquer sur "Create app"
   - Remplir les informations :
     - App name : "Job Search Agent"
     - LinkedIn Page : Votre page entreprise
     - App logo : (optionnel)

2. **Demander l'accès à Jobs API**
   - Dans votre app, aller dans "Products"
   - Demander accès à "Jobs API"
   - **⚠️ Attention :** Nécessite validation LinkedIn (peut prendre plusieurs semaines)

3. **Obtenir les credentials OAuth**
   - Onglet "Auth"
   - Noter :
     - **Client ID**
     - **Client Secret**

4. **Configurer les Redirect URLs**
   - Ajouter : `http://localhost:8000/auth/linkedin/callback`

### Configuration
```bash
# Dans config/credentials/api_keys.env
LINKEDIN_CLIENT_ID=votre-client-id
LINKEDIN_CLIENT_SECRET=votre-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
```

### Alternative : Scraping LinkedIn
```python
# ⚠️ LinkedIn détecte et bloque les scrapers
# Utiliser avec prudence, respecter les ToS
# Alternative : RapidAPI LinkedIn scraper (payant)
```

---

## 📋 3. Welcome to the Jungle API

### Étapes

1. **Vérifier la disponibilité**
   - Welcome to the Jungle n'a pas d'API publique officielle
   - Contacter : partners@welcometothejungle.com

2. **Alternative : Scraping**
   ```python
   # API non-officielle (peut changer)
   url = "https://www.welcometothejungle.com/api/v1/jobs"
   params = {
       "query": "Python Developer",
       "location": "Paris",
       "contract_type": "full_time"
   }
   ```

3. **RapidAPI**
   - Rechercher "Welcome to the Jungle" sur RapidAPI
   - URL : https://rapidapi.com
   - Abonnement payant requis

### Configuration
```bash
# Si vous utilisez RapidAPI
WTTJ_RAPIDAPI_KEY=votre-cle-rapidapi
WTTJ_RAPIDAPI_HOST=welcome-to-the-jungle1.p.rapidapi.com
```

---

## 📋 4. Apec API (France - Cadres)

### Étapes

1. **S'inscrire sur le portail développeurs Apec**
   - URL : https://api.apec.fr (vérifier disponibilité)
   - **Note :** L'Apec n'a pas d'API grand public

2. **Alternative : Scraping Apec**
   ```python
   # Scraping du site Apec
   # URL de recherche : https://www.apec.fr/candidat/recherche-emploi.html
   ```

3. **API Pole Emploi (alternative)**
   - URL : https://pole-emploi.io/login
   - Créer un compte développeur
   - API gratuite pour offres d'emploi françaises

### Configuration Pole Emploi (alternative)
```bash
# Pole Emploi API
POLE_EMPLOI_CLIENT_ID=votre-client-id
POLE_EMPLOI_CLIENT_SECRET=votre-client-secret
```

**Tutoriel Pole Emploi API :**
1. S'inscrire sur https://pole-emploi.io
2. Créer une application
3. Sélectionner "Offres d'emploi v2"
4. Obtenir client_id et client_secret

---

## 📋 5. Glassdoor API

### Situation actuelle
- Glassdoor a fermé son API publique en 2020
- Pas d'accès public disponible

### Alternatives

#### Option A : Scraping Glassdoor
```python
# ⚠️ Glassdoor bloque activement les scrapers
# Utiliser avec prudence, risque de ban IP
```

#### Option B : RapidAPI
- Chercher "Glassdoor" sur RapidAPI
- Services tiers payants disponibles

#### Option C : Partenariat entreprise
- Contacter Glassdoor directement
- Réservé aux grandes entreprises

---

## 🔧 Configuration centralisée

### Fichier `config/credentials/api_keys.env`

```bash
# ===== JOB BOARDS =====

# Indeed (scraping ou API si disponible)
INDEED_API_KEY=
INDEED_PUBLISHER_ID=

# LinkedIn
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback

# Welcome to the Jungle (RapidAPI)
WTTJ_RAPIDAPI_KEY=
WTTJ_RAPIDAPI_HOST=

# Pole Emploi (alternative Apec)
POLE_EMPLOI_CLIENT_ID=
POLE_EMPLOI_CLIENT_SECRET=

# Glassdoor (RapidAPI)
GLASSDOOR_RAPIDAPI_KEY=

# Autres
MONSTER_API_KEY=
JOBTEASER_API_KEY=
```

---

## 🤖 Scraping : Bonnes pratiques

### Rate Limiting
```python
import time
import random

def scrape_with_delay(url):
    # Délai aléatoire entre requêtes (2-5 secondes)
    time.sleep(random.uniform(2, 5))

    # Faire la requête
    response = requests.get(url, headers=headers)
    return response
```

### User-Agent rotation
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
]

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}
```

### Proxy rotation (optionnel)
```python
# Utiliser des proxies pour éviter le ban IP
PROXIES = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
]

response = requests.get(url, proxies={'http': random.choice(PROXIES)})
```

---

## 📊 Comparaison des sources

| Plateforme | API Publique | Scraping | Coût | Couverture |
|------------|--------------|----------|------|------------|
| Indeed | ❌ | ✅ Facile | Gratuit | 🌍 Mondiale |
| LinkedIn | ⚠️ Restreint | ⚠️ Difficile | Gratuit/Payant | 🌍 Mondiale |
| WTTJ | ❌ | ✅ Moyen | RapidAPI ($) | 🇫🇷 France/Europe |
| Pole Emploi | ✅ | ✅ | Gratuit | 🇫🇷 France |
| Glassdoor | ❌ | ⚠️ Difficile | RapidAPI ($) | 🌍 Mondiale |

---

## 🎯 Recommandations pour démarrer

### Phase 1 : MVP (gratuit)
1. **Indeed** - Scraping simple
2. **Pole Emploi** - API gratuite (France)
3. **Apec** - Scraping (France, cadres)

### Phase 2 : Scale
1. Ajouter **LinkedIn** (si accès API obtenu)
2. Ajouter **WTTJ** via RapidAPI
3. Ajouter d'autres sources selon besoins

---

## 🛡️ Légalité et Ethics

### ⚠️ Important

- **Respecter les Terms of Service** de chaque plateforme
- **Scraping :** Zone grise légale, vérifier les CGU
- **Rate limiting :** Ne pas surcharger les serveurs
- **Usage personnel :** OK. Usage commercial : vérifier licences

### Bonnes pratiques

```python
# Ajouter un robots.txt checker
from urllib.robotparser import RobotFileParser

def can_scrape(url):
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)
```

---

## 🧪 Tester vos credentials

```python
# Script de test : test_job_boards.py

import os
from dotenv import load_dotenv

load_dotenv('./config/credentials/api_keys.env')

# Test Pole Emploi
def test_pole_emploi():
    client_id = os.getenv('POLE_EMPLOI_CLIENT_ID')
    client_secret = os.getenv('POLE_EMPLOI_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("❌ Pole Emploi credentials manquants")
        return False

    # Obtenir token
    import requests
    auth_url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token"
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'api_offresdemploiv2 o2dsoffre'
    }

    response = requests.post(auth_url, params=params)

    if response.status_code == 200:
        print("✅ Pole Emploi API : OK")
        return True
    else:
        print(f"❌ Pole Emploi API : {response.status_code}")
        return False

# Lancer les tests
test_pole_emploi()
```

---

## 📚 Ressources

- [Pole Emploi API Docs](https://pole-emploi.io/data/api/offres-emploi)
- [RapidAPI Hub](https://rapidapi.com/hub)
- [LinkedIn Developer](https://www.linkedin.com/developers)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

---
