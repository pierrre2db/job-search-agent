# Job Search & CV Management Agent - Starter Kit

Structure complète pour équipe de développement Agile avec Claude IA.

---

## 📁 Structure du Répertoire

```
job-search-agent/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── docs-deploy.yml
│   │   └── claude-code-review.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── user_story.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── detection_agent.py
│   │   ├── adaptation_agent.py
│   │   ├── tracking_agent.py
│   │   └── portfolio_agent.py
│   ├── modules/
│   │   ├── detection/
│   │   │   ├── __init__.py
│   │   │   ├── jobboard_scraper.py
│   │   │   ├── email_parser.py
│   │   │   ├── scoring_engine.py
│   │   │   └── tests/
│   │   │       └── test_detection.py
│   │   ├── adaptation/
│   │   │   ├── __init__.py
│   │   │   ├── cv_generator.py
│   │   │   ├── claude_matcher.py
│   │   │   ├── word_formatter.py
│   │   │   └── tests/
│   │   │       └── test_adaptation.py
│   │   ├── tracking/
│   │   │   ├── __init__.py
│   │   │   ├── application_tracker.py
│   │   │   ├── notification_service.py
│   │   │   └── tests/
│   │   │       └── test_tracking.py
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── drive_manager.py
│   │   │   ├── sheets_manager.py
│   │   │   └── tests/
│   │   │       └── test_storage.py
│   │   └── portfolio/
│   │       ├── __init__.py
│   │       ├── portfolio_linker.py
│   │       └── tests/
│   │           └── test_portfolio.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   └── validators.py
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       ├── routes.py
│       └── schemas.py
│
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── API_REFERENCE.md
│   ├── CLAUDE_CONFIG.md
│   ├── AGILE_WORKFLOW.md
│   └── modules/
│       ├── detection.md
│       ├── adaptation.md
│       ├── tracking.md
│       ├── storage.md
│       └── portfolio.md
│
├── config/
│   ├── claude_config.json
│   ├── job_preferences.json
│   ├── scoring_rules.json
│   └── integrations.json
│
├── scripts/
│   ├── setup.sh
│   ├── run_local.sh
│   ├── deploy.sh
│   ├── migrate_db.sh
│   └── reset_storage.sh
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   └── test_all_modules.py
│   ├── integration/
│   │   └── test_workflows.py
│   └── e2e/
│       └── test_end_to_end.py
│
├── .env.example
├── .gitignore
├── .flake8
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── Makefile
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🚀 Fichiers clés à créer

### 1. **README.md** (Racine)

```markdown
# Job Search & CV Management Agent

Agent IA modulaire pour automatiser la recherche d'emploi, l'adaptation de CV et le suivi de candidatures.

## 🎯 Objectifs

- Détection multi-source d'offres d'emploi avec scoring intelligent.
- Adaptation automatique de CV via Claude IA.
- Gestion centralisée du suivi de candidatures.
- Intégration Google Drive (stockage), Google Sheets (suivi), Microsoft Word (génération).
- Architecture modulaire, scalable, Agile.

## 📋 Stack technique

- **Langage** : Python 3.10+
- **API IA** : Claude (Anthropic) pour matching et adaptation
- **Cloud** : Google Drive, Google Sheets (APIs)
- **Framework Web** : FastAPI
- **Scraping** : BeautifulSoup, Selenium
- **Tests** : pytest, pytest-cov
- **CI/CD** : GitHub Actions
- **Containerisation** : Docker, Docker Compose

## 🏃 Démarrage rapide

### Installation locale

```bash
# Cloner le repo
git clone https://github.com/your-org/job-search-agent.git
cd job-search-agent

# Créer env virtuel
python -m venv venv
source venv/bin/activate  # ou \venv\Scripts\activate sur Windows

# Installer dépendances
pip install -r requirements.txt

# Configurer variables d'environnement
cp .env.example .env
# Éditer .env avec tes clés API, chemins, etc.

# Lancer tests
pytest

# Lancer l'app localement
python src/api/main.py
```

## 📚 Documentation

- [Architecture système](docs/ARCHITECTURE.md)
- [Configuration Claude](docs/CLAUDE_CONFIG.md)
- [Workflow Agile & Sprints](docs/AGILE_WORKFLOW.md)
- [API Reference](docs/API_REFERENCE.md)
- [Guide setup complet](docs/SETUP.md)

## 🛠️ Pour les contributeurs

- Voir [CONTRIBUTING.md](CONTRIBUTING.md)
- Voir [Agile Workflow](docs/AGILE_WORKFLOW.md) pour les sprints

## 📊 Status du projet

| Phase | Status | Sprint |
|-------|--------|--------|
| MVP - Détection | 🟢 En cours | Sprint 1 |
| MVP - Adaptation | 🟠 Prévu | Sprint 2 |
| MVP - Suivi | 🔴 À venir | Sprint 3 |
| Growth - Analytics | 🔴 Backlog | Sprint 4+ |

---
```

### 2. **.env.example**

```bash
# Claude API Configuration
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=2000
CLAUDE_TEMPERATURE=0.7

# Google APIs
GOOGLE_DRIVE_CREDENTIALS_PATH=./config/google_credentials.json
GOOGLE_SHEETS_ID=your-spreadsheet-id

# Application Configuration
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Scraping & Detection
SCRAPER_USER_AGENT=Mozilla/5.0...
SCRAPER_TIMEOUT=30
JOBBOARD_API_KEYS={}  # JSON avec clés API jobboards

# Email Integration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Database (local/sqlite pour POC)
DATABASE_URL=sqlite:///./test.db

# Notification
NOTIFICATION_EMAIL=your-email@gmail.com

# Feature Flags
ENABLE_CLAUDE_ADAPTATION=true
ENABLE_AUTO_SCRAPING=false
ENABLE_AUTO_RELANCE=false
```

### 3. **requirements.txt**

```
anthropic==0.42.0
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.107.0
gspread==6.0.0
python-docx==0.8.11
beautifulsoup4==4.12.2
requests==2.31.0
selenium==4.15.2
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.23.2
redis==5.0.1
sqlalchemy==2.0.23
alembic==1.13.0
python-multipart==0.0.6
aiofiles==23.2.1
```

### 4. **pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "job-search-agent"
version = "0.1.0"
description = "AI-powered job search and CV management agent"
authors = [{name = "Your Team", email = "team@example.com"}]
requires-python = ">=3.10"
dependencies = [
    "anthropic>=0.42.0",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-dotenv>=1.0.0",
    "google-auth-oauthlib>=1.2.0",
    "google-api-python-client>=2.107.0",
    "gspread>=6.0.0",
    "python-docx>=0.8.11",
    "beautifulsoup4>=4.12.2",
    "requests>=2.31.0",
    "selenium>=4.15.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "redis>=5.0.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "black[jupyter]==23.12.0",
    "ruff==0.1.8",
    "mypy==1.7.1",
    "sphinx==7.2.6",
    "sphinx-rtd-theme==2.0.0",
]

[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
select = ["E", "F", "W", "I"]
line-length = 100

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

### 5. **Dockerfile**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6. **Makefile**

```makefile
.PHONY: help install test lint format run clean docker-up docker-down docs

help:
	@echo "Commandes disponibles:"
	@echo "  make install        - Installer les dépendances"
	@echo "  make test           - Lancer les tests"
	@echo "  make lint           - Vérifier le code (flake8, mypy)"
	@echo "  make format         - Formatter le code (black)"
	@echo "  make run            - Lancer l'app localement"
	@echo "  make clean          - Nettoyer les caches"
	@echo "  make docker-up      - Démarrer Docker Compose"
	@echo "  make docker-down    - Arrêter Docker Compose"
	@echo "  make docs           - Générer la documentation"

install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest -v --cov=src tests/

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

run:
	python src/api/main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docs:
	cd docs && sphinx-build -b html . _build/html
	@echo "Documentation générée dans docs/_build/html"
```

---

## 📋 Fichiers de configuration agile

### 7. **.github/ISSUE_TEMPLATE/user_story.md**

```markdown
---
name: User Story
about: Créer une user story pour le sprint Agile
---

## Titre
[Exemple : En tant que chercheur d'emploi, je veux...]

## Description
En tant que [rôle],
Je veux [fonctionnalité],
Afin que [bénéfice].

## Critères d'acceptation
- [ ] Critère 1
- [ ] Critère 2
- [ ] Critère 3

## Tasks techniques
- [ ] Subtask 1
- [ ] Subtask 2

## Points d'effort (RICE)
- Reach: [1-10]
- Impact: [1-10]
- Confidence: [%]
- Effort: [jours]

## Module concerné
- [ ] Detection
- [ ] Adaptation
- [ ] Tracking
- [ ] Storage
- [ ] Portfolio
- [ ] Admin

## Definition of Done
- Code révisé et approuvé
- Tests unitaires (>80% couverture)
- Tests d'intégration passants
- Documentation mise à jour
- Pas de dégression en performance
```

### 8. **.github/workflows/ci.yml**

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e ".[dev]"
    
    - name: Lint
      run: |
        flake8 src/ tests/
        mypy src/
    
    - name: Run tests
      run: |
        pytest -v --cov=src --cov-report=xml tests/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

---

## 🤖 Configuration Claude

### 9. **config/claude_config.json**

```json
{
  "claude_api": {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 2000,
    "temperature": 0.7,
    "timeout": 30,
    "max_retries": 3
  },
  "agents": {
    "detection": {
      "system_prompt": "Tu es un expert en détection et scraping d'offres d'emploi. Analyse les offres reçues, extrais les informations clés (titre, compétences requises, localisation, etc.) et évalue leur pertinence par rapport au profil du candidat.",
      "tools": ["parse_job_listing", "extract_skills", "score_relevance"]
    },
    "adaptation": {
      "system_prompt": "Tu es un expert en adaptation de CV et en matching candidat-offre. Analyse l'offre d'emploi et le CV existant, identifie les écarts et suggestions, génère une version adaptée du CV avec des wording optimisés.",
      "tools": ["analyze_job_requirements", "extract_candidate_skills", "generate_tailored_cv", "suggest_improvements"]
    },
    "tracking": {
      "system_prompt": "Tu es un gestionnaire de candidatures. Suis le statut des applications, génère des rappels de relance, analyse les taux de conversion et fournis des insights.",
      "tools": ["track_application", "schedule_followup", "analyze_metrics"]
    },
    "portfolio": {
      "system_prompt": "Tu es un expert en valorisation du portfolio. Identifie les projets et liens pertinents à inclure dans chaque version de CV adaptée selon l'offre d'emploi.",
      "tools": ["match_portfolio_items", "generate_links", "score_relevance"]
    }
  },
  "caching": {
    "enabled": true,
    "ttl_seconds": 3600,
    "redis_url": "redis://localhost:6379"
  }
}
```

### 10. **docs/CLAUDE_CONFIG.md**

```markdown
# Configuration Claude API

## Overview

Claude est utilisé pour :
- Matching sémantique entre CV et offres d'emploi
- Adaptation intelligente de CV
- Extraction et scoring des compétences
- Génération de suggestions personnalisées

## API Key Setup

### Option 1 : Variable d'environnement (recommandé)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Option 2 : Fichier .env

```bash
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=2000
CLAUDE_TEMPERATURE=0.7
```

## Tool Use (Appels de fonction)

Claude utilise des outils définis pour chaque agent. Exemple :

```python
from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "extract_skills",
        "description": "Extrait les compétences requises d'une offre d'emploi",
        "input_schema": {
            "type": "object",
            "properties": {
                "job_description": {"type": "string"},
            },
            "required": ["job_description"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    tools=tools,
    messages=[{"role": "user", "content": "Extrait les compétences de cette offre..."}]
)
```

## Prompt Engineering

Chaque agent a un system prompt bien défini (voir config/claude_config.json) :

- **Detection Agent** : Identifie et analyse les offres.
- **Adaptation Agent** : Personnalise et optimise les CV.
- **Tracking Agent** : Gère le suivi et la stratégie de relance.
- **Portfolio Agent** : Valorise les projets pertinents.

## Streaming & Async

Pour optimiser la latence, utiliser le streaming :

```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Rate Limits & Cost Optimization

- Claude Sonnet 4 : 50 req/min, 40k tokens/min
- Implémenter caching Redis pour réduire les appels API redondants
- Utiliser models.claude-haiku pour tâches simples (plus rapide, moins cher)

## Testing

Mock Claude pour les tests unitaires :

```python
from unittest.mock import patch

@patch('src.modules.adaptation.claude_client.messages.create')
def test_cv_adaptation(mock_claude):
    mock_claude.return_value = {...}
    # Test ton agent
```

---
```

### 11. **docs/AGILE_WORKFLOW.md**

```markdown
# Workflow Agile - Job Search Agent

## Méthodologie

Scrum + Kanban, avec sprints de 2 semaines, daily standups et rétros.

## Structure des Sprints

### Sprint Planning (Lundi 10h)
- Affiner les user stories du backlog
- Évaluer points d'effort (RICE framework)
- S'engager sur les stories pour le sprint

### Daily Standup (Lundi-Vendredi 09h30)
- 15 min max
- Blocker? Progression? À faire aujourd'hui?

### Sprint Review (Vendredi 16h)
- Démo des features complétées
- Feedback stakeholders
- Préparation des prochaines priorités

### Sprint Retro (Vendredi 16h30)
- Qu'est-ce qui a bien fonctionné?
- Où avons-nous buté?
- Actions d'amélioration

## Naming Conventions

### Branches Git
```
feature/detection-jobboard-api     # Feature nouvelle
bugfix/scoring-algorithm           # Bug fix
docs/setup-guide                   # Documentation
hotfix/critical-auth-issue         # Hotfix urgent
```

### Commits
```
feat(detection): Add Indeed API integration
fix(adaptation): Resolve CV generation encoding issue
docs(setup): Update installation guide
test(tracking): Add application status test
chore(deps): Upgrade anthropic to 0.43.0
```

### User Stories
```
[US-001] Detection: Scrape Indeed offers with scoring
[US-002] Adaptation: Generate tailored CV with Claude
[US-003] Tracking: Dashboard with application status
```

## Definition of Done

- ✅ Code écrit et peer-reviewé
- ✅ Tests unitaires (>80% couverture)
- ✅ Tests d'intégration passants
- ✅ Documentation mise à jour
- ✅ Pas de régression en performance (benchmark)
- ✅ Merge sur develop (prêt pour release)

## Backlog (Priorité)

### Phase 1 - MVP (Sprints 1-2)
- [x] Detection : Scraper Indeed + scoring
- [ ] Adaptation : CV generator + Claude matching
- [ ] Tracking : Dashboard + application status
- [ ] Storage : Google Drive + Sheets integration

### Phase 2 - Growth (Sprints 3-4)
- [ ] Multi-board : LinkedIn Jobs, Welcome to the Jungle
- [ ] AI Resume Optimization : A/B testing
- [ ] Notifications : Email + relances automatiques
- [ ] Portfolio : Link injection

### Phase 3 - Scale (Sprints 5+)
- [ ] ATS Integration : Greenhouse, Lever
- [ ] Advanced Analytics : Conversion rates, heat maps
- [ ] Recruiter Outreach : Automation, templating
- [ ] Admin Dashboard : Monitoring, audit logs

---
```

---

## 🎯 Templates de modules Python

### 12. **src/config.py**

```python
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Claude Configuration
    anthropic_api_key: str = Field(..., env='ANTHROPIC_API_KEY')
    claude_model: str = Field(default='claude-sonnet-4-20250514', env='CLAUDE_MODEL')
    claude_max_tokens: int = Field(default=2000, env='CLAUDE_MAX_TOKENS')
    claude_temperature: float = Field(default=0.7, env='CLAUDE_TEMPERATURE')
    
    # Google APIs
    google_drive_credentials: str = Field(default='./config/google_credentials.json')
    google_sheets_id: str = Field(..., env='GOOGLE_SHEETS_ID')
    
    # Application
    app_env: str = Field(default='development', env='APP_ENV')
    debug: bool = Field(default=True, env='DEBUG')
    log_level: str = Field(default='INFO', env='LOG_LEVEL')
    
    # Database
    database_url: str = Field(default='sqlite:///./test.db', env='DATABASE_URL')
    
    class Config:
        env_file = '.env'
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### 13. **src/agents/orchestrator.py**

```python
"""
Orchestrateur principal pour coordonner les agents spécialisés.
Dispatche les tâches aux modules appropriés selon le workflow.
"""

import logging
from typing import Optional, Dict, Any
from src.config import settings
from src.modules.detection import detection_agent
from src.modules.adaptation import adaptation_agent
from src.modules.tracking import tracking_agent

logger = logging.getLogger(__name__)

class JobSearchOrchestrator:
    """Agent orchestrateur principal"""
    
    def __init__(self):
        self.detection = detection_agent
        self.adaptation = adaptation_agent
        self.tracking = tracking_agent
        
    async def process_new_job_offer(self, offer_url: str) -> Dict[str, Any]:
        """
        Workflow complet : détection -> analyse -> adaptation -> archivage
        """
        try:
            logger.info(f"Processing new offer: {offer_url}")
            
            # 1. Détection et parsing
            offer_data = await self.detection.parse_offer(offer_url)
            logger.info(f"Parsed offer: {offer_data['title']}")
            
            # 2. Scoring de pertinence
            score = await self.detection.score_offer(offer_data)
            
            if score < 0.6:
                logger.info(f"Offer score too low: {score}. Skipping.")
                return {"status": "skipped", "reason": "low_score"}
            
            # 3. Adaptation du CV
            tailored_cv = await self.adaptation.generate_tailored_cv(
                offer_data=offer_data
            )
            
            # 4. Archivage et suivi
            application = await self.tracking.create_application(
                offer_data=offer_data,
                cv_variant=tailored_cv
            )
            
            logger.info(f"Application created: {application['id']}")
            return {
                "status": "success",
                "application_id": application['id'],
                "score": score,
                "cv_location": tailored_cv['drive_url']
            }
            
        except Exception as e:
            logger.error(f"Error processing offer: {e}")
            raise

orchestrator = JobSearchOrchestrator()
```

### 14. **src/modules/detection/scoring_engine.py**

```python
"""
Engine de scoring pour évaluer la pertinence des offres.
Intégre Claude pour analyse sémantique + règles heuristiques.
"""

import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Évalue la pertinence d'une offre selon le profil candidat"""
    
    def __init__(self):
        self.client = Anthropic()
        self.required_skills = ["Python", "API", "AI"]
        self.preferred_locations = ["Remote", "Paris", "Berlin"]
        
    async def score_offer(self, offer: dict) -> float:
        """
        Combine multiple facteurs de scoring :
        - Skills match (via Claude)
        - Location match
        - Seniority level
        - Company reputation (future)
        """
        
        # 1. Skills matching avec Claude
        skills_score = await self._claude_skill_match(offer)
        
        # 2. Location matching
        location_score = self._location_match(offer.get('location', ''))
        
        # 3. Seniority matching
        seniority_score = self._seniority_match(offer.get('level', 'mid'))
        
        # Weighted average
        final_score = (
            skills_score * 0.5 +
            location_score * 0.3 +
            seniority_score * 0.2
        )
        
        logger.info(f"Offer score: {final_score:.2f} (skills: {skills_score}, location: {location_score})")
        return final_score
    
    async def _claude_skill_match(self, offer: dict) -> float:
        """Use Claude for semantic skill matching"""
        
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"""
                Compare these required skills with my profile:
                My skills: {', '.join(self.required_skills)}
                Required: {offer.get('required_skills', 'N/A')}
                
                Return a score from 0 to 1 (float).
                """
            }]
        )
        
        # Parse Claude response
        score_text = message.content[0].text
        try:
            return float(score_text.strip())
        except ValueError:
            return 0.5  # Default if parsing fails
    
    def _location_match(self, offer_location: str) -> float:
        """Simple location matching"""
        if any(pref.lower() in offer_location.lower() for pref in self.preferred_locations):
            return 1.0
        return 0.3
    
    def _seniority_match(self, level: str) -> float:
        """Match seniority level"""
        seniority_map = {"junior": 0.5, "mid": 1.0, "senior": 0.8}
        return seniority_map.get(level.lower(), 0.5)

scoring_engine = ScoringEngine()
```

---

## 📋 ToDo Checklist Setup Initial

```markdown
## Phase 0 - Infrastructure Setup (Semaine 1)

- [ ] Créer repo GitHub avec cette structure
- [ ] Configurer GitHub Actions (CI/CD)
- [ ] Setup Google Cloud Project (Drive, Sheets APIs)
- [ ] Générer Google Service Account credentials
- [ ] Setup Anthropic API key
- [ ] Créer tableau Kanban (GitHub Projects ou Jira)

## Phase 1 - Sprint 1 (Semaine 2-3)

### Detection Agent
- [ ] Implémenter scraper Indeed (BeautifulSoup)
- [ ] Parser offres en format structuré
- [ ] Setup scoring engine (heuristique + Claude)
- [ ] Tests unitaires (>80%)
- [ ] Integration tests avec API réelle

### Infrastructure
- [ ] Logger centralisé (Python logging)
- [ ] Error handling robuste
- [ ] Rate limiting

## Phase 1 - Sprint 2 (Semaine 4-5)

### Adaptation Agent
- [ ] Intégration Claude API (tool use)
- [ ] Générateur CV (python-docx)
- [ ] Upload automatique Google Drive
- [ ] Tests end-to-end

### Tracking
- [ ] Google Sheets integration
- [ ] Dashboard minimal (statut candidatures)

## Phase 2 - Growth (Semaines 6+)

- [ ] Multi-board integration
- [ ] Notifications email
- [ ] Portfolio linking
- [ ] Analytics dashboard

---
```

