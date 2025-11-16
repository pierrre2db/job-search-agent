# Setup Anthropic Claude API - Tutoriel Complet

Guide pour créer un compte Anthropic et obtenir votre clé API Claude.

---

## 🎯 Objectifs

- Créer un compte Anthropic
- Générer une clé API
- Configurer la clé dans le projet
- Tester la connexion
- Comprendre les limites et coûts

---

## 📋 Étape 1 : Créer un compte Anthropic

1. **Aller sur le site Anthropic Console**
   - URL : https://console.anthropic.com

2. **S'inscrire**
   - Cliquer sur "Sign Up"
   - Options :
     - Email + mot de passe
     - Google account
     - GitHub account

3. **Vérifier votre email**
   - Vérifiez votre boîte mail
   - Cliquez sur le lien de confirmation

4. **Compléter votre profil**
   - Nom d'organisation (optionnel)
   - Cas d'usage : "Job search automation with CV adaptation"

---

## 📋 Étape 2 : Ajouter un moyen de paiement

**IMPORTANT** : Claude API est payant à l'usage. Vous devez ajouter une carte de crédit.

1. **Aller dans "Settings" > "Billing"**

2. **Ajouter une carte de crédit**
   - Cliquer sur "Add payment method"
   - Entrer vos informations de carte

3. **Configurer les limites de dépenses** (recommandé)
   - Définir une limite mensuelle (ex: $50)
   - Vous recevrez des alertes si vous approchez de la limite

---

## 📋 Étape 3 : Générer une clé API

1. **Aller dans "API Keys"**
   - Menu : Settings > API Keys

2. **Créer une nouvelle clé**
   - Cliquer sur "+ Create Key"
   - **Nom** : `job-search-agent-production`
   - **Description** : "Key for job search agent application"
   - Cliquer sur "Create Key"

3. **IMPORTANT : Copier la clé immédiatement**
   - La clé commence par `sk-ant-`
   - **Elle ne sera affichée qu'une seule fois !**
   - Exemple : `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

4. **Sauvegarder la clé**
   ```bash
   # Dans le fichier api_keys.env
   echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxx" >> config/credentials/api_keys.env
   ```

---

## 📋 Étape 4 : Configurer dans le projet

1. **Éditer `config/credentials/api_keys.env`**
   ```bash
   # Claude API
   ANTHROPIC_API_KEY=sk-ant-votre-cle-ici
   CLAUDE_MODEL=claude-sonnet-4-20250514
   CLAUDE_MAX_TOKENS=2000
   CLAUDE_TEMPERATURE=0.7
   ```

2. **Le projet chargera automatiquement cette clé**
   - Via `src/config.py`
   - Utilisation dans `src/modules/adaptation/claude_matcher.py`

---

## 📋 Étape 5 : Tester la connexion

Créer un script de test simple :

```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv('./config/credentials/api_keys.env')

# Initialiser le client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Test simple
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    messages=[{
        "role": "user",
        "content": "Dis bonjour en une phrase."
    }]
)

print("✅ Connexion réussie !")
print(f"Réponse de Claude : {message.content[0].text}")
```

**Exécuter le test :**
```bash
python test_claude.py
```

**Résultat attendu :**
```
✅ Connexion réussie !
Réponse de Claude : Bonjour, comment puis-je vous aider aujourd'hui ?
```

---

## 💰 Coûts et Limites

### Modèles disponibles

| Modèle | Coût Input | Coût Output | Usage recommandé |
|--------|-----------|-------------|------------------|
| **Claude Sonnet 4** | $3 / 1M tokens | $15 / 1M tokens | Production, matching CV |
| Claude Haiku 3.5 | $0.80 / 1M tokens | $4 / 1M tokens | Tâches simples, parsing |
| Claude Opus 4 | $15 / 1M tokens | $75 / 1M tokens | Tâches complexes |

### Estimation de coûts pour ce projet

**Scénario typique :**
- 100 offres analysées par mois
- 50 CVs générés par mois
- Tokens moyens : ~2000 tokens/requête

**Calcul :**
```
Input : 150 requêtes × 2000 tokens = 300k tokens
Output : 150 requêtes × 1000 tokens = 150k tokens

Coût mensuel (Sonnet 4) :
- Input : 300k × $3/1M = $0.90
- Output : 150k × $15/1M = $2.25
Total : ~$3.15/mois
```

### Rate Limits

| Plan | Requêtes/min | Tokens/min |
|------|--------------|------------|
| Free Tier | 5 | 20,000 |
| Tier 1 | 50 | 40,000 |
| Tier 2 | 1,000 | 80,000 |

**Pour ce projet :** Le free tier suffit pour démarrer.

---

## 🔧 Optimisation des coûts

### 1. **Caching des réponses**
```python
# Utiliser Redis pour cacher les réponses
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_cached_or_call_claude(prompt):
    # Vérifier cache
    cached = cache.get(prompt)
    if cached:
        return cached.decode()

    # Appeler Claude
    response = client.messages.create(...)
    result = response.content[0].text

    # Mettre en cache (1 heure)
    cache.setex(prompt, 3600, result)
    return result
```

### 2. **Utiliser Haiku pour tâches simples**
```python
# Pour du parsing simple, utiliser Haiku (moins cher)
if task_type == "simple_extraction":
    model = "claude-haiku-3-5-20250514"
else:
    model = "claude-sonnet-4-20250514"
```

### 3. **Batch processing**
```python
# Traiter plusieurs offres en une seule requête
batch_prompt = f"""
Analyse ces 5 offres et retourne un JSON :
Offre 1: {offer1}
Offre 2: {offer2}
...
"""
```

---

## 🛡️ Sécurité

### ✅ Bonnes pratiques

- **Ne jamais** commit la clé API sur Git
- Utiliser des variables d'environnement
- Révoquer les clés compromises immédiatement
- Utiliser des clés différentes pour dev/prod

### ❌ À éviter

```python
# ❌ MAUVAIS : Hardcoder la clé
api_key = "sk-ant-xxxxx"

# ✅ BON : Utiliser les env vars
api_key = os.getenv('ANTHROPIC_API_KEY')
```

---

## 🆘 Problèmes courants

### Erreur : "Invalid API Key"
- Vérifiez que la clé commence par `sk-ant-`
- Vérifiez qu'il n'y a pas d'espaces avant/après
- Re-générez une nouvelle clé

### Erreur : "Rate limit exceeded"
- Vous dépassez les limites de votre tier
- Attendez quelques minutes
- Ou ajoutez un système de retry avec backoff

### Erreur : "Insufficient credits"
- Ajoutez un moyen de paiement
- Rechargez votre compte

---

## 📚 Ressources

- [Anthropic Documentation](https://docs.anthropic.com)
- [Claude API Reference](https://docs.anthropic.com/en/api/messages)
- [Pricing](https://www.anthropic.com/pricing)
- [Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

---

## 🎓 Tutoriels avancés

### Streaming responses
```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Tool use (fonction calling)
```python
tools = [{
    "name": "extract_skills",
    "description": "Extract skills from job description",
    "input_schema": {
        "type": "object",
        "properties": {
            "job_description": {"type": "string"}
        },
        "required": ["job_description"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[...]
)
```

---
