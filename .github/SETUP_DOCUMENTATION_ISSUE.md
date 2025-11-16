# Issue à créer sur GitHub : Documentation du Setup Complet

Copiez le contenu ci-dessous pour créer une issue sur GitHub.

---

**Titre :** [DOCS] Guide de setup complet et configuration initiale

**Labels :** documentation, good first issue

**Assignees :** (vous-même)

---

## 📚 Objectif

Créer une documentation complète pour permettre à n'importe quel développeur de configurer et lancer le projet Job Search Agent de A à Z.

## 📋 Contenu à documenter

### 1. README.md principal (racine)

- [ ] Vue d'ensemble du projet
- [ ] Architecture système
- [ ] Stack technique détaillée
- [ ] Prérequis (Python 3.10+, comptes requis)
- [ ] Démarrage rapide (Quick Start)
- [ ] Liens vers la documentation détaillée
- [ ] Badges (CI/CD, coverage, license)
- [ ] Contribution guidelines

### 2. docs/SETUP.md

- [ ] **Prérequis détaillés**
  - Installation Python 3.10+
  - Installation Git
  - Création des comptes nécessaires (Google Cloud, Anthropic)

- [ ] **Installation locale**
  - Clone du repo
  - Création de l'environnement virtuel
  - Installation des dépendances
  - Configuration des variables d'environnement

- [ ] **Configuration des APIs**
  - Google Cloud Platform
    - Création projet
    - Activation APIs (Drive, Sheets, Gmail)
    - Service Account
    - Téléchargement credentials
    - Partage des ressources
  - Anthropic Claude
    - Création compte
    - Génération API key
    - Configuration dans .env
  - Job Boards (optionnel)
    - Indeed, LinkedIn, Pole Emploi, etc.

- [ ] **Configuration des fichiers**
  - `config/credentials/api_keys.env`
  - `config/settings/job_preferences.json` (personnalisation)
  - `config/settings/scoring_rules.json` (ajustement des poids)

- [ ] **Premier lancement**
  - Tests de connexion
  - Vérification de la config
  - Premier scraping test
  - Génération d'un CV test

### 3. docs/ARCHITECTURE.md

- [ ] Diagrammes d'architecture
  - Vue d'ensemble du système
  - Flow de données
  - Modules et leurs interactions
- [ ] Description de chaque module
  - Detection (scraping, scoring)
  - Adaptation (Claude, CV generation)
  - Tracking (applications, followups)
  - Storage (Drive, Sheets)
  - Portfolio (linking)
- [ ] Technologies utilisées par module
- [ ] Décisions d'architecture

### 4. docs/API_REFERENCE.md

- [ ] Endpoints FastAPI
  - `/health`
  - `/process-offer`
  - `/applications`
  - `/applications/{id}`
  - `/applications/{id}/follow-up`
- [ ] Schémas Pydantic
- [ ] Exemples de requêtes/réponses
- [ ] Codes d'erreur

### 5. docs/DEVELOPMENT.md

- [ ] Setup environnement de dev
- [ ] Standards de code
  - Formatting (Black)
  - Linting (flake8, mypy)
  - Type hints
  - Docstrings
- [ ] Tests
  - Tests unitaires
  - Tests d'intégration
  - Mocking Claude et Google APIs
  - Coverage requirements (>80%)
- [ ] Workflow Git
  - Branching strategy
  - Commit conventions
  - Pull requests
  - Code review process
- [ ] CI/CD
  - GitHub Actions workflows
  - Tests automatisés
  - Déploiement

### 6. docs/DEPLOYMENT.md

- [ ] Déploiement local
- [ ] Déploiement Docker
  - Build de l'image
  - docker-compose
  - Variables d'environnement
- [ ] Déploiement cloud (futur)
  - AWS / GCP / Azure
  - Kubernetes (optionnel)
- [ ] Monitoring et logs
- [ ] Backup et restauration

### 7. docs/TROUBLESHOOTING.md

- [ ] Problèmes courants
  - Erreurs de credentials
  - Problèmes de connexion API
  - Erreurs de scraping
  - Problèmes de génération CV
- [ ] Solutions
- [ ] FAQ
- [ ] Où obtenir de l'aide

## 📊 Critères d'acceptation

- [ ] Toutes les sections documentées
- [ ] Documentation testée par un nouveau développeur
- [ ] Captures d'écran et exemples inclus
- [ ] Liens internes fonctionnels
- [ ] Formatage Markdown correct
- [ ] Grammaire et orthographe vérifiées

## 🎯 Priorité

**HAUTE** - Bloque l'onboarding de nouveaux contributeurs

## ⏱️ Estimation

3-4 jours de travail

## 📝 Notes

- Utiliser les tutoriels existants dans `config/tutorials/` comme base
- Ajouter des diagrammes avec Mermaid ou draw.io
- Inclure des exemples de code
- Tester la documentation en suivant les instructions depuis zéro

## 🔗 Ressources

- Tutoriels existants : `config/tutorials/`
- Starter kit : `job-search-agent-kit.md`
- Checklist Agile : `agile-todos-checklist.md`

---

## ✅ Definition of Done

- [ ] README.md complet et informatif
- [ ] Tous les fichiers docs/ créés
- [ ] Documentation validée par test pratique
- [ ] Screenshots et diagrammes ajoutés
- [ ] Revue et approbation
- [ ] Mergé sur main
