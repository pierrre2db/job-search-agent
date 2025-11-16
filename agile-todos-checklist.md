# Todo List & Checklist Agile - Job Search Agent

---

## 🚀 Phase Pré-Launch (Semaine 0)

### Infrastructure & Setup
- [ ] Créer repo GitHub `job-search-agent`
- [ ] Inviter développeurs à la repo
- [ ] Setup branch protection (main, develop)
- [ ] Configurer GitHub Actions (CI/CD)
- [ ] Créer tableau Kanban (GitHub Projects)

### Google Cloud Setup
- [ ] Créer projet Google Cloud
- [ ] Activer Google Drive API
- [ ] Activer Google Sheets API
- [ ] Créer Service Account
- [ ] Télécharger `google_credentials.json` → `/config/`
- [ ] Partager le Drive root avec le Service Account

### Anthropic Setup
- [ ] S'inscrire sur Anthropic (https://console.anthropic.com)
- [ ] Générer API key
- [ ] Ajouter clé à `.env`
- [ ] Tester connexion API

### Environment Local
- [ ] Copier `.env.example` → `.env` (sur chaque dev machine)
- [ ] Remplir clés API dans `.env`
- [ ] Tester `make install` & `make test`
- [ ] Documenter setup dans CONTRIBUTING.md

### Project Management
- [ ] Créer épics dans GitHub Issues
- [ ] Créer user stories pour Sprint 1
- [ ] Setup milestones (Sprint 1, 2, 3...)
- [ ] Assigner points d'effort (RICE)

---

## 📋 Sprint 1 (Semaine 1-2) : MVP Detection

### US-001 : Scraper Indeed

**Acceptance Criteria:**
- [ ] Peut récupérer offres depuis Indeed
- [ ] Parse titre, entreprise, description, lien
- [ ] Gère la pagination
- [ ] Rate limiting OK (ne pas ban l'IP)
- [ ] Logs structurés
- [ ] Tests unitaires (>80%)

**Tasks Techniques:**
- [ ] Setup BeautifulSoup + Selenium
- [ ] Implémenter `jobboard_scraper.py`
- [ ] Gestion erreurs & retries
- [ ] Tests avec données mock
- [ ] Documentation dans `/docs/modules/detection.md`

**Code Review Checklist:**
- [ ] Code formaté (black)
- [ ] Linting OK (flake8, mypy)
- [ ] Tests passent (`pytest`)
- [ ] No hardcoded credentials
- [ ] Docstrings complètes

---

### US-002 : Parser Emails Gmail

**Acceptance Criteria:**
- [ ] Connexion OAuth à Gmail
- [ ] Récupère nouveaux emails (depuis 24h)
- [ ] Détecte offres dans emails
- [ ] Parse les liens d'offres
- [ ] Stocke les offres en JSON
- [ ] Tests intégration OK

**Tasks Techniques:**
- [ ] Setup Google Gmail API
- [ ] Implémenter `email_parser.py`
- [ ] Décodage MIME + extraction URLs
- [ ] Tests avec emails mock
- [ ] Gestion des erreurs d'authentification

---

### US-003 : Scoring Engine (Heuristique + Claude)

**Acceptance Criteria:**
- [ ] Score les offres 0-1
- [ ] Combine skill matching + location + level
- [ ] Claude API intégré
- [ ] Caching des réponses Claude (Redis)
- [ ] Scoring threshold configurable
- [ ] Tests unitaires & intégration

**Tasks Techniques:**
- [ ] Implémenter `scoring_engine.py`
- [ ] Integration Claude API avec error handling
- [ ] Setup Redis pour caching
- [ ] Extraction skills avec Claude
- [ ] Benchmark performance

---

### US-004 : Dashboard Détection (Google Sheets)

**Acceptance Criteria:**
- [ ] Offres détectées dans un Google Sheets
- [ ] Colonnes : titre, entreprise, score, source, URL, timestamp
- [ ] Mise à jour automatique (toutes les heures)
- [ ] Filtering & sorting dans Sheets
- [ ] Lien direct vers l'offre

**Tasks Techniques:**
- [ ] Setup gspread integration
- [ ] Créer template Sheets
- [ ] Implémenter `sheets_manager.py`
- [ ] Scheduler CRON
- [ ] Tests E2E

---

### Sprint 1 Definition of Done
- [ ] Toutes user stories complétées
- [ ] Code testé >80% couverture
- [ ] Docs mises à jour
- [ ] Déployable sur develop branch
- [ ] Démo faite à stakeholders

---

## 📋 Sprint 2 (Semaine 3-4) : MVP Adaptation

### US-005 : Claude Matching Engine

**Acceptance Criteria:**
- [ ] Analyse offre + CV → matching score
- [ ] Identifie skill gaps
- [ ] Suggère 5-7 adaptations pour CV
- [ ] Streaming responses (latency < 3s)
- [ ] Caching optimisé
- [ ] Fallback mode (no API key)

**Tasks Techniques:**
- [ ] Implémenter `claude_matcher.py`
- [ ] Tool use setup (parse_requirements, match_skills, etc.)
- [ ] Error handling + rate limiting
- [ ] Caching Redis
- [ ] Tests avec offres réelles
- [ ] Benchmark coûts API

---

### US-006 : CV Generator (Word Format)

**Acceptance Criteria:**
- [ ] Génère .docx adapté
- [ ] Applique suggestions Claude
- [ ] Format professionnel (headers, fonts, spacing)
- [ ] Versioning (horodatage auto)
- [ ] Support caractères spéciaux (accents, etc.)

**Tasks Techniques:**
- [ ] Setup python-docx
- [ ] Créer template Word
- [ ] Implémenter `cv_generator.py`
- [ ] Mise en page (résumé, skills, exp, edu)
- [ ] Tests de formatage

---

### US-007 : Google Drive Upload & Storage

**Acceptance Criteria:**
- [ ] Upload CV généré sur Drive
- [ ] Organisation dossiers (par entreprise/poste)
- [ ] Archive offre + CV + metadata en JSON
- [ ] Versioning des CVs
- [ ] Liens partagés générés

**Tasks Techniques:**
- [ ] Implémenter `drive_manager.py`
- [ ] Créer structure dossiers automatiquement
- [ ] Setup Share settings
- [ ] Archivage offer_data.json
- [ ] Gestion des permissions

---

### US-008 : Intégration Orchestrateur

**Acceptance Criteria:**
- [ ] Offre reçue → CV généré → Drive uploadé
- [ ] Workflow end-to-end fonctionnel
- [ ] Logging détaillé de chaque étape
- [ ] Error recovery (retry logic)
- [ ] Tests E2E complets

**Tasks Techniques:**
- [ ] Implémenter `orchestrator.py`
- [ ] Chaîner les modules
- [ ] Setup error handlers
- [ ] Tests intégration (mock Claude + Drive)
- [ ] Démo live

---

### Sprint 2 Definition of Done
- [ ] MVP complet : detection → adaptation → storage
- [ ] API FastAPI fonctionnelle (endpoints `/process-offer`, etc.)
- [ ] Tests couverture >80%
- [ ] Documentation API complète
- [ ] Démo produit fonctionnel

---

## 📋 Sprint 3 (Semaine 5-6) : Tracking & Dashboard

### US-009 : Application Tracker Database

**Acceptance Criteria:**
- [ ] Stocke chaque candidature
- [ ] Colonnes : offer_id, status, date_applied, cv_version, score, notes
- [ ] Sync automatique depuis Google Drive
- [ ] Historique complète

**Tasks Techniques:**
- [ ] Setup SQLAlchemy models
- [ ] Migrations Alembic
- [ ] CRUD operations
- [ ] Tests unitaires DAO

---

### US-010 : Dashboard Suivi (API)

**Acceptance Criteria:**
- [ ] GET `/applications` → liste avec filtrage
- [ ] GET `/applications/{id}` → détails
- [ ] PATCH `/applications/{id}` → update status
- [ ] Stats : total, conversion rate, etc.

**Tasks Techniques:**
- [ ] Implémenter routes FastAPI
- [ ] Validation Pydantic schemas
- [ ] Tests API (pytest + httpx)

---

### US-011 : Notifications & Relances

**Acceptance Criteria:**
- [ ] Email de confirmation après candidature
- [ ] Relance auto après 3j (configurable)
- [ ] Notifications sur statut change
- [ ] Template personnalisables

**Tasks Techniques:**
- [ ] Setup SMTP (Gmail)
- [ ] Implémenter `notification_service.py`
- [ ] Scheduler relances
- [ ] Template emails

---

### Sprint 3 Definition of Done
- [ ] Dashboard de tracking fonctionnel
- [ ] Notifications envoyées correctement
- [ ] Tests E2E complets

---

## 📋 Sprint 4 (Semaine 7-8) : Growth & Polish

### US-012 : Multi-Board Integration

**Acceptance Criteria:**
- [ ] Support LinkedIn Jobs
- [ ] Support Welcome to the Jungle
- [ ] Support Apec
- [ ] Agrégation centralisée
- [ ] Scraper failover si un board down

**Tasks Techniques:**
- [ ] Ajouter scrapers supplémentaires
- [ ] Adapter scoring engine
- [ ] Tests avec chaque board

---

### US-013 : Portfolio Linking

**Acceptance Criteria:**
- [ ] Détecte projets pertinents du portfolio
- [ ] Ajoute liens auto dans CV adapté
- [ ] Matching contextuel (skills relevants)

**Tasks Techniques:**
- [ ] Implémenter `portfolio_linker.py`
- [ ] Connector portfolio (GitHub, Behance, etc.)
- [ ] Tests de pertinence

---

### US-014 : A/B Testing de CVs

**Acceptance Criteria:**
- [ ] Génère 2-3 variantes de CV
- [ ] Track response rates par variante
- [ ] Analytics dans dashboard

**Tasks Techniques:**
- [ ] Setup A/B test logic
- [ ] Variantes de résumé/skills
- [ ] Analytics tracking

---

### Sprint 4 Definition of Done
- [ ] Multi-board working
- [ ] Portfolio integration live
- [ ] A/B testing setup
- [ ] Performance optimisé

---

## 🎯 Backlog Future (Phase 3+)

- [ ] ATS Integration (Greenhouse, Lever)
- [ ] Recruiter mode (vendre CVs)
- [ ] Interview prep (questions générées par Claude)
- [ ] Career path prediction
- [ ] Skill gap analysis
- [ ] Market intelligence (trending skills, salary)

---

## 📊 Definition of Done Global

Chaque user story DOIT avoir :

### Code
- ✅ Code révisé & approuvé (≥1 reviewer)
- ✅ Tests unitaires (>80% couverture)
- ✅ Tests intégration (si applicable)
- ✅ Formatted (black)
- ✅ Linting OK (flake8, mypy)
- ✅ No credentials hardcodés
- ✅ Error handling complet
- ✅ Logging structuré

### Documentation
- ✅ Docstrings + type hints
- ✅ README mise à jour
- ✅ Module doc dans `/docs/modules/`
- ✅ API endpoints documentés (si applicable)
- ✅ Examples d'usage

### Testing
- ✅ Tests passent (`pytest`)
- ✅ Tests mock Claude/Drive (offline)
- ✅ Tests performance (benchmarks)
- ✅ Coverage report généré

### DevOps
- ✅ CI/CD pipeline vert
- ✅ Dockerfile buildable
- ✅ `.env.example` mis à jour

---

## 🔄 Workflow Git & Commits

### Branching
```bash
# Feature nouvelle
git checkout -b feature/detection-indeed-scraper

# Bug fix
git checkout -b bugfix/scoring-algorithm-edge-case

# Documentation
git checkout -b docs/setup-guide

# Commit
git commit -m "feat(detection): Add Indeed scraper with pagination"

# Push & Open PR
git push origin feature/detection-indeed-scraper
```

### Commit Conventions
```
feat(module): Description courte (imperatif, max 50 chars)
fix(module): ...
docs(module): ...
test(module): ...
chore(deps): ...
refactor(module): ...
perf(module): ...
```

### PR Template
```markdown
## Description
Quoi et pourquoi?

## Type de changement
- [ ] Feature nouvelle
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Checklist
- [ ] Code révisé
- [ ] Tests passent
- [ ] Coverage >80%
- [ ] Docs updated
- [ ] No breaking changes

## Screenshots/Output (si applicable)

## Liés à Issues
Closes #123
```

---

## 📈 Metrics Suivi

### Par Sprint
- Velocity (points complétés)
- Burn-down chart
- Bug count
- Code coverage trend

### Produit
- Offres détectées/jour
- CVs générés/jour
- Taux réponse candidatures
- Performance API (latency, error rate)

---

## 🎉 Release Checklist

**Avant merge sur main:**
- [ ] Tous tests passent
- [ ] Coverage >80%
- [ ] Code review ≥2 approvals
- [ ] Performance benchmarks OK
- [ ] CHANGELOG.md updaté
- [ ] Version bump (semver)
- [ ] Documentation finalisée
- [ ] Hotline support préparé

---

## 📞 Escalation & Support

**Issues de priorité haute:**
- Contact lead dev + PM directement
- Daily standup flagging

**Blockers techniques:**
- Créer issue "🔴 BLOCKER"
- Notify team lead
- Sync call si nécessaire

**Questions produit:**
- Discuter en standup
- Documenter decision dans wiki

---

