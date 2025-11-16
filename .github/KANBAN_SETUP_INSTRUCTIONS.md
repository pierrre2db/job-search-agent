# Configuration du Kanban GitHub Projects

Guide pour configurer le tableau Kanban pour la gestion Agile du projet Job Search Agent.

---

## 🎯 Objectif

Mettre en place un tableau Kanban dans GitHub Projects pour :
- Suivre les user stories et tâches
- Visualiser l'avancement des sprints
- Gérer le backlog
- Tracking des bugs et améliorations

---

## 📋 Étapes de configuration

### 1. Créer un nouveau Project

1. **Aller sur le repo GitHub**
   ```
   https://github.com/pierrre2db/job-search-agent
   ```

2. **Cliquer sur l'onglet "Projects"**

3. **Cliquer sur "New project"**
   - Choisir **"Board"** (vue Kanban)
   - Nom : `Job Search Agent - Agile Board`
   - Description : `Kanban board for sprint planning and tracking`

### 2. Configurer les colonnes

Créer les colonnes suivantes (dans cet ordre) :

#### 📝 Backlog
- **Description :** Issues non planifiées, futures user stories
- **Automation :** Aucune

#### 🎯 Sprint Backlog
- **Description :** Issues sélectionnées pour le sprint actuel
- **Automation :** Aucune

#### 📋 To Do
- **Description :** Tâches prêtes à être commencées
- **Automation :**
  - Auto-add items when status changes to "Todo"

#### 🚧 In Progress
- **Description :** Tâches en cours de développement
- **Automation :**
  - Auto-add items when status changes to "In Progress"
  - Auto-add PRs when opened

#### 👀 In Review
- **Description :** Pull requests en attente de review
- **Automation :**
  - Auto-add PRs when marked as "Ready for review"

#### ✅ Done
- **Description :** Tâches complétées et mergées
- **Automation :**
  - Auto-add when issues closed
  - Auto-add when PRs merged
  - Auto-archive after 7 days

---

## 🏷️ Labels à créer

Créer les labels suivants dans le repo (Settings > Labels) :

### Par type
- `user-story` - 📖 User story Agile (bleu)
- `bug` - 🐛 Bug à corriger (rouge)
- `enhancement` - ✨ Amélioration / nouvelle feature (vert)
- `documentation` - 📚 Documentation (bleu clair)
- `refactoring` - 🔧 Refactoring technique (gris)
- `tests` - ✅ Tests unitaires/intégration (jaune)

### Par priorité
- `priority: high` - 🔴 Priorité haute (rouge foncé)
- `priority: medium` - 🟡 Priorité moyenne (orange)
- `priority: low` - 🟢 Priorité basse (vert clair)

### Par module
- `module: detection` - 🔍 Module Detection
- `module: adaptation` - 📝 Module Adaptation
- `module: tracking` - 📊 Module Tracking
- `module: storage` - 💾 Module Storage
- `module: portfolio` - 🎨 Module Portfolio

### Par sprint
- `sprint-1` - Sprint 1 (violet)
- `sprint-2` - Sprint 2 (violet)
- `sprint-3` - Sprint 3 (violet)
- (etc.)

### Autres
- `good first issue` - 👋 Bon pour débutants (vert clair)
- `help wanted` - 🆘 Aide recherchée (jaune)
- `blocked` - 🚫 Bloqué (rouge)
- `wontfix` - ❌ Ne sera pas corrigé (gris)

---

## 📊 Vues à créer

### Vue 1 : Board (par défaut)
- **Type :** Board
- **Grouper par :** Status
- **Filtrer par :** Aucun
- **Trier par :** Priority (High → Low)

### Vue 2 : Sprint actuel
- **Type :** Board
- **Grouper par :** Status
- **Filtrer par :** Label = `sprint-1` (ou sprint actuel)
- **Trier par :** Priority

### Vue 3 : Par module
- **Type :** Table
- **Grouper par :** Module labels
- **Filtrer par :** Open issues
- **Colonnes :** Title, Status, Priority, Assignee, Sprint

### Vue 4 : Backlog prioritisé
- **Type :** Table
- **Filtrer par :** Status = Backlog
- **Trier par :** Priority, puis RICE score (custom field)
- **Colonnes :** Title, Priority, Module, Effort, RICE score

---

## 🎨 Custom Fields à ajouter

1. **Sprint**
   - Type : Single select
   - Options : Sprint 1, Sprint 2, Sprint 3, Sprint 4

2. **Effort (jours)**
   - Type : Number
   - Unité : jours

3. **RICE Score**
   - Type : Number
   - Formule : (Reach × Impact × Confidence) / Effort

4. **Module**
   - Type : Single select
   - Options : Detection, Adaptation, Tracking, Storage, Portfolio, Admin

---

## 📈 Milestones à créer

Créer les milestones suivants (Settings > Milestones) :

1. **Sprint 1 - MVP Detection**
   - Due date : 2 semaines après le début
   - Description : Scraping Indeed, scoring engine, dashboard Sheets

2. **Sprint 2 - MVP Adaptation**
   - Due date : 4 semaines après le début
   - Description : Claude integration, CV generation, Drive upload

3. **Sprint 3 - MVP Tracking**
   - Due date : 6 semaines après le début
   - Description : Application tracking, notifications, relances

4. **Sprint 4 - Growth**
   - Due date : 8 semaines après le début
   - Description : Multi-board, portfolio linking, A/B testing

5. **v1.0 - Production Ready**
   - Due date : 12 semaines après le début
   - Description : MVP complet, testé, documenté, déployé

---

## 🔄 Workflow recommandé

### Pour créer une nouvelle issue

1. Créer l'issue avec le bon template
2. Ajouter les labels appropriés
3. Assigner au milestone si planifié
4. Remplir les custom fields (Sprint, Effort, Module)
5. L'issue apparaîtra automatiquement dans "Backlog"

### Pour travailler sur une issue

1. Déplacer de "Backlog" → "Sprint Backlog" (planning)
2. Déplacer de "Sprint Backlog" → "To Do" (prêt à commencer)
3. Déplacer de "To Do" → "In Progress" (commencer le travail)
4. Créer une branche : `git checkout -b feature/US-XXX-description`
5. Développer, commiter, pusher
6. Créer PR → apparaît automatiquement dans "In Review"
7. Review et merge → apparaît dans "Done"

---

## 📝 Templates de issues pré-créées

Issues à créer immédiatement pour démarrer :

### Sprint 1

1. **[US-001] Scraper Indeed avec scoring**
   - Labels : `user-story`, `module: detection`, `sprint-1`, `priority: high`
   - Milestone : Sprint 1

2. **[US-002] Parser emails Gmail pour offres**
   - Labels : `user-story`, `module: detection`, `sprint-1`, `priority: high`

3. **[US-003] Scoring engine heuristique + Claude**
   - Labels : `user-story`, `module: detection`, `sprint-1`, `priority: high`

4. **[US-004] Dashboard Google Sheets**
   - Labels : `user-story`, `module: storage`, `sprint-1`, `priority: medium`

### Backlog (futures)

5. **[DOCS] Guide de setup complet**
   - Labels : `documentation`, `good first issue`, `priority: high`
   - (Contenu : voir SETUP_DOCUMENTATION_ISSUE.md)

6. **[US-005] Claude matching engine**
   - Labels : `user-story`, `module: adaptation`, `sprint-2`

7. **[US-006] CV Generator Word**
   - Labels : `user-story`, `module: adaptation`, `sprint-2`

---

## ✅ Vérification finale

Une fois configuré, vérifiez que :

- [ ] Toutes les colonnes sont créées
- [ ] Les automations sont activées
- [ ] Les labels sont créés et colorés
- [ ] Les milestones sont créés avec dates
- [ ] Les custom fields sont ajoutés
- [ ] Au moins 3-5 issues de démarrage sont créées
- [ ] Les vues alternatives sont configurées
- [ ] Le board est partagé avec l'équipe (si applicable)

---

## 🎓 Bonnes pratiques

1. **Daily standup virtuel**
   - Consulter le board chaque jour
   - Mettre à jour le statut des issues

2. **Sprint planning**
   - Déplacer issues du Backlog → Sprint Backlog
   - Réévaluer les priorités
   - Assigner les issues

3. **Sprint review**
   - Vérifier les issues dans "Done"
   - Archiver les issues complétées
   - Démo des features

4. **Sprint retro**
   - Ajouter des notes dans une issue dédiée
   - Identifier les blockers
   - Actions d'amélioration

---

## 📚 Ressources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Agile Best Practices](https://www.atlassian.com/agile/project-management/project-management-intro)

---
