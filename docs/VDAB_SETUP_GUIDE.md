# Guide de Configuration VDAB API 🇧🇪

Guide complet pour configurer l'accès à l'API VDAB (Service officiel d'emploi flamand).

---

## ℹ️ À propos de VDAB

**VDAB** (Vlaamse Dienst voor Arbeidsbemiddeling) est le service public flamand pour l'emploi et la formation professionnelle.

**Avantages de l'API VDAB:**
- ✅ **Gratuit** - Aucun coût
- ✅ **Légal** - API officielle du gouvernement flamand
- ✅ **Fiable** - Données structurées et à jour
- ✅ **Généreux** - ~1000 requêtes/jour
- ✅ **Complet** - Accès à toutes les offres de Flandre

**Couverture géographique:**
- Flandre (Vlaanderen) - Région flamande
- Bruxelles (partiellement - bilingue)

---

## 📋 Étape 1: Créer un compte développeur

### 1.1 Accéder au portail développeur

Rendez-vous sur: **https://developer.vdab.be/openservices/**

![VDAB Developer Portal](https://developer.vdab.be/openservices/)

### 1.2 Créer un compte

1. Cliquez sur **"Create a new account"** (en haut à droite)
2. Remplissez le formulaire d'inscription:
   - Prénom et nom
   - Email (professionnel de préférence)
   - Mot de passe
   - Organisation (optionnel)
3. Acceptez les conditions d'utilisation
4. Cliquez sur **"Register"**

### 1.3 Confirmer votre email

1. Vérifiez votre boîte mail
2. Cliquez sur le lien de confirmation
3. Votre compte est maintenant actif

**Temps estimé:** ~5 minutes

---

## 🔑 Étape 2: Obtenir votre Client ID

### 2.1 Se connecter

1. Retournez sur https://developer.vdab.be/openservices/
2. Cliquez sur **"Sign in"**
3. Entrez vos identifiants

### 2.2 Créer une application

1. Une fois connecté, allez dans **"Apps"** (menu en haut)
2. Cliquez sur **"Create new app"** ou **"Register a new application"**
3. Remplissez les informations:
   - **Application Name:** "Job Search Agent" (ou votre nom)
   - **Description:** "Personal job search automation"
   - **Callback URL:** http://localhost (pas nécessaire pour notre usage)

4. Cliquez sur **"Submit"** ou **"Create"**

### 2.3 Souscrire aux APIs

1. Dans votre application, cherchez la section **"API Products"** ou **"Subscribe to APIs"**
2. Trouvez et sélectionnez **"Vacature"** (v4.x.x)
3. Cliquez sur **"Subscribe"**
4. Le plan gratuit devrait suffire (généralement nommé "Default Plan" ou "Free Plan")

### 2.4 Récupérer votre Client ID

1. Dans votre application, cherchez la section **"Credentials"** ou **"Keys"**
2. Vous devriez voir:
   - **Client ID** (aussi appelé "API Key" ou "X-IBM-Client-Id")
   - Éventuellement un Client Secret (non nécessaire pour notre usage)

3. **Copiez le Client ID** - il ressemble à ceci:
   ```
   a1b2c3d4-e5f6-7890-abcd-ef1234567890
   ```

**Temps estimé:** ~10 minutes

---

## ⚙️ Étape 3: Configurer le projet

### 3.1 Créer le fichier de credentials

1. Naviguez vers le dossier du projet:
   ```bash
   cd "/Users/pierre2db/Documents/Projets/Jobs agents"
   ```

2. Copiez le fichier d'exemple:
   ```bash
   cp config/credentials/vdab_credentials.env.example \
      config/credentials/vdab_credentials.env
   ```

3. Ouvrez le fichier:
   ```bash
   nano config/credentials/vdab_credentials.env
   # ou utilisez votre éditeur préféré
   ```

### 3.2 Ajouter votre Client ID

Modifiez le fichier pour qu'il contienne:

```env
# VDAB API Credentials
VDAB_CLIENT_ID=votre_vrai_client_id_ici
```

**Remplacez** `votre_vrai_client_id_ici` par le Client ID que vous avez copié.

Exemple:
```env
VDAB_CLIENT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### 3.3 Vérifier la configuration

Le fichier doit être ignoré par git (.gitignore):

```bash
# Vérifier que vdab_credentials.env ne sera pas commité
git status | grep vdab_credentials.env
# Ne devrait rien afficher (fichier ignoré)
```

**Temps estimé:** ~5 minutes

---

## 🧪 Étape 4: Tester l'API

### 4.1 Test simple

```bash
source venv/bin/activate
python -m src.modules.detection.vdab_api
```

**Sortie attendue:**
```
================================================================================
🇧🇪 VDAB API SCRAPER - SERVICE OFFICIEL FLAMAND
================================================================================

✅ Client ID trouvé: a1b2c3d4e5...

✅ 10 offres trouvées

1. Python Developer
   🏢 Acme Corporation
   📍 Brussel
   🔗 https://www.vdab.be/vindeenjob/vacatures/123456...

2. Full Stack Developer
   ...
```

### 4.2 Test programmatique

Créez un fichier `test_vdab.py`:

```python
from src.modules.detection.vdab_api import VDABScraper

# Test de base
with VDABScraper() as scraper:
    offers = scraper.search(
        query="Python Developer",
        location="Brussel",
        max_results=5
    )

    print(f"✅ {len(offers)} offres trouvées")

    for offer in offers:
        print(f"- {offer.title} @ {offer.company}")
```

Exécutez:
```bash
python test_vdab.py
```

### 4.3 Codes d'erreur courants

| Erreur | Cause | Solution |
|--------|-------|----------|
| `401 Unauthorized` | Client ID invalide | Vérifiez votre Client ID |
| `403 Forbidden` | Pas souscrit à l'API Vacature | Souscrivez dans le portail |
| `429 Too Many Requests` | Quota dépassé | Attendez ou réduisez la fréquence |
| `ValueError: Client ID manquant` | Fichier .env pas chargé | Vérifiez le chemin du fichier |

**Temps estimé:** ~5 minutes

---

## 📚 Utilisation avancée

### Recherche avec filtres

```python
from src.modules.detection.vdab_api import VDABScraper

scraper = VDABScraper()

# Recherche avancée
offers = scraper.search(
    query="Python",
    location="Antwerpen",
    max_results=20,
    sort_by="date",  # ou "relevance"
    filters={
        'contractType': 'CDI',  # Contrat à durée indéterminée
        'taal': 'nl'  # Néerlandais
    }
)

for offer in offers:
    print(f"{offer.title} - {offer.company}")
    if offer.study_level:
        print(f"  Niveau requis: {offer.study_level}")
    if offer.experience_required:
        print(f"  Expérience: {offer.experience_required}")
```

### Récupérer une offre spécifique

```python
scraper = VDABScraper()

# Par ID
offer = scraper.get_vacancy_by_id("12345678")

if offer:
    print(f"Titre: {offer.title}")
    print(f"Description: {offer.description}")
    print(f"URL: {offer.url}")
```

### Intégration avec le système

```python
from src.modules.detection.vdab_api import VDABScraper
from src.modules.detection.indeed_bypass import IndeedBypassScraper

# Combiner VDAB + Indeed
vdab_scraper = VDABScraper()
indeed_scraper = IndeedBypassScraper(headless=False, country='be')

# Récupérer des offres de sources multiples
vdab_offers = vdab_scraper.search("Python Developer", "Brussel")
indeed_offers = indeed_scraper.scrape("Python Developer", "Bruxelles", max_pages=2)

all_offers = vdab_offers + indeed_offers
print(f"Total: {len(all_offers)} offres")

# Dédupliquer par titre/entreprise
unique_offers = []
seen = set()

for offer in all_offers:
    key = (offer.title.lower(), offer.company.lower())
    if key not in seen:
        seen.add(key)
        unique_offers.append(offer)

print(f"Uniques: {len(unique_offers)} offres")
```

---

## 🔧 Dépannage

### Problème: "Client ID manquant"

**Cause:** Le fichier `vdab_credentials.env` n'est pas trouvé ou mal configuré

**Solution:**
1. Vérifiez que le fichier existe:
   ```bash
   ls config/credentials/vdab_credentials.env
   ```

2. Vérifiez le contenu:
   ```bash
   cat config/credentials/vdab_credentials.env
   ```

3. Le fichier doit contenir:
   ```
   VDAB_CLIENT_ID=votre_id_ici
   ```

### Problème: "401 Unauthorized"

**Cause:** Client ID invalide ou expiré

**Solutions:**
1. Reconnectez-vous sur https://developer.vdab.be/openservices/
2. Vérifiez votre application
3. Régénérez le Client ID si nécessaire
4. Mettez à jour `vdab_credentials.env`

### Problème: Aucune offre trouvée

**Causes possibles:**
1. Requête trop spécifique
2. Localisation incorrecte
3. API en maintenance

**Solutions:**
1. Essayez une recherche plus générale:
   ```python
   offers = scraper.search(query="Developer", location="Vlaanderen")
   ```

2. Vérifiez le statut de l'API:
   - https://developer.vdab.be/openservices/ (annonces)
   - Forums VDAB

3. Testez avec l'environnement de test:
   ```python
   scraper = VDABScraper(use_test_env=True)
   ```

### Problème: "429 Too Many Requests"

**Cause:** Quota dépassé (~1000 req/jour)

**Solutions:**
1. Attendez 24h pour le reset du quota
2. Réduisez `max_results` par requête
3. Implémentez un cache:
   ```python
   import pickle
   from datetime import datetime, timedelta

   # Sauvegarder les résultats
   with open('cache_vdab.pkl', 'wb') as f:
       pickle.dump({
           'timestamp': datetime.now(),
           'offers': offers
       }, f)

   # Charger depuis le cache
   with open('cache_vdab.pkl', 'rb') as f:
       cache = pickle.load(f)
       if datetime.now() - cache['timestamp'] < timedelta(hours=6):
           offers = cache['offers']  # Utiliser le cache
   ```

---

## 📊 Limites de l'API

### Quotas

| Type | Limite | Reset |
|------|--------|-------|
| Requêtes/jour | ~1000 | 00:00 CET |
| Résultats/requête | 100 | - |
| Taille réponse | ~5 MB | - |

### Restrictions géographiques

- **Couverture:** Principalement Flandre
- **Langue:** Néerlandais majoritaire
- **Bruxelles:** Partiel (bilingue)
- **Wallonie:** Non couvert (utilisez Forem ou Indeed)

### Données disponibles

| Champ | Toujours présent | Fréquence |
|-------|------------------|-----------|
| Titre | ✅ | 100% |
| Entreprise | ✅ | ~95% |
| Localisation | ✅ | ~98% |
| Description | ✅ | 100% |
| Salaire | ❌ | ~5% |
| Remote | ⚠️ | Détecté via description |

---

## 💡 Bonnes pratiques

### 1. Gestion des credentials

**À FAIRE:**
- ✅ Stocker le Client ID dans `.env`
- ✅ Ajouter `.env` au `.gitignore`
- ✅ Ne jamais commit de credentials
- ✅ Utiliser `python-dotenv` pour charger

**À NE PAS FAIRE:**
- ❌ Hardcoder le Client ID dans le code
- ❌ Partager votre Client ID
- ❌ Commit le fichier de credentials

### 2. Respect des quotas

```python
import time

# Ajouter un délai entre requêtes
for location in ["Brussel", "Antwerpen", "Gent"]:
    offers = scraper.search(query="Python", location=location)
    process_offers(offers)
    time.sleep(2)  # 2 secondes entre requêtes
```

### 3. Gestion des erreurs

```python
from requests.exceptions import RequestException

try:
    offers = scraper.search("Python Developer", "Brussel")
except ValueError as e:
    print(f"Configuration incorrecte: {e}")
except RequestException as e:
    print(f"Erreur réseau: {e}")
    # Fallback vers Indeed
    offers = indeed_scraper.scrape("Python Developer", "Bruxelles")
```

### 4. Logging

```python
import logging

# Activer les logs détaillés
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

scraper = VDABScraper()
offers = scraper.search("Python", "Brussel")
```

---

## 📞 Support et ressources

### Documentation officielle

- **Portail développeur:** https://developer.vdab.be/openservices/
- **Forums:** https://developer.vdab.be/openservices/forum
- **Extranet (docs techniques):** https://extranet.vdab.be/api-center-excellence-coe/

### Contact VDAB

- **Support API:** Via les forums du portail développeur
- **Email général:** info@vdab.be
- **Support technique:** Créer un ticket dans le portail

### Support projet

- **Email:** pierre2db@gmail.com
- **Tel:** 0499/45 54 45
- **GitHub Issues:** https://github.com/pierrre2db/job-search-agent/issues

---

## ✅ Checklist complète

- [ ] Compte créé sur developer.vdab.be
- [ ] Email confirmé
- [ ] Application créée
- [ ] Souscrit à l'API "Vacature"
- [ ] Client ID récupéré
- [ ] Fichier `vdab_credentials.env` créé
- [ ] Client ID ajouté au fichier
- [ ] Test de l'API réussi
- [ ] Script de test fonctionne
- [ ] Intégration dans le projet

---

**Date de création:** 2025-11-16
**Version:** 1.0
**Status:** ✅ Prêt pour utilisation
