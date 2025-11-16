# Fichiers de Configuration & Code - Prêts à Copy-Paste

---

## 1️⃣ **src/utils/logger.py**

```python
import logging
import json
from datetime import datetime
from pathlib import Path

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Setup centralisé du logging avec format structuré"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    
    # Format structuré
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Handler fichier (optionnel)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / f"{name}.log")
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage
logger = setup_logger(__name__)
```

---

## 2️⃣ **src/api/main.py**

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.agents.orchestrator import orchestrator
from src.config import settings

app = FastAPI(
    title="Job Search Agent API",
    version="0.1.0",
    description="API pour agent de gestion de recherche d'emploi"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# Routes de base
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "environment": settings.app_env}

@app.post("/process-offer")
async def process_job_offer(offer_url: str):
    """
    Endpoint pour traiter une nouvelle offre d'emploi
    - Détecte & scrape l'offre
    - Évalue la pertinence (scoring)
    - Adapte le CV automatiquement
    - Archive et crée le suivi
    """
    try:
        result = await orchestrator.process_new_job_offer(offer_url)
        return result
    except Exception as e:
        logger.error(f"Error processing offer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications")
async def list_applications(status: str = None):
    """Liste les candidatures avec filtrage optionnel"""
    try:
        applications = await orchestrator.tracking.list_applications(status)
        return {"count": len(applications), "applications": applications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications/{app_id}")
async def get_application_details(app_id: str):
    """Détails d'une candidature spécifique"""
    try:
        app_data = await orchestrator.tracking.get_application(app_id)
        return app_data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Application not found")

@app.post("/applications/{app_id}/follow-up")
async def trigger_follow_up(app_id: str):
    """Déclenche une relance pour une candidature"""
    try:
        result = await orchestrator.tracking.schedule_followup(app_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
```

---

## 3️⃣ **src/modules/adaptation/claude_matcher.py**

```python
"""
Adaptation module : utilise Claude pour matcher offre d'emploi avec CV
et générer des suggestions d'optimisation
"""

import logging
from anthropic import Anthropic
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ClaudeMatcher:
    """Utilise Claude pour matching intelligent CV <-> Offre"""
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    async def analyze_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """
        Extrait les exigences clés d'une offre d'emploi
        Retour: {skills: [], responsibilities: [], nice_to_have: [], ...]
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""
                Analyze this job description and extract:
                1. Required technical skills
                2. Required soft skills
                3. Main responsibilities (top 3)
                4. Nice-to-have qualifications
                5. Seniority level
                
                Job Description:
                {job_description}
                
                Return as JSON.
                """
            }]
        )
        
        response_text = message.content[0].text
        logger.info(f"Analyzed job requirements: {response_text[:100]}...")
        
        # Parse JSON response
        import json
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error("Failed to parse Claude response as JSON")
            return {"error": "parsing_failed"}
    
    async def match_cv_to_job(self, cv_content: str, job_reqs: Dict) -> Dict[str, Any]:
        """
        Compare CV avec exigences du job
        Retour: {match_score: 0.85, gaps: [], strengths: [], suggestions: []}
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""
                Compare this CV with job requirements and provide:
                1. Overall match percentage (0-100)
                2. Skill gaps (what's missing)
                3. Candidate strengths for this role (top 3)
                4. Specific suggestions to improve CV for this job (5-7 suggestions)
                5. Recommended key phrases to add
                
                CV Content:
                {cv_content}
                
                Job Requirements:
                {str(job_reqs)}
                
                Return as JSON with structure: {
                    "match_score": 85,
                    "gaps": [...],
                    "strengths": [...],
                    "suggestions": [...],
                    "key_phrases": [...]
                }
                """
            }]
        )
        
        response_text = message.content[0].text
        import json
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error("Failed to parse matching response")
            return {"error": "parsing_failed"}
    
    async def generate_tailored_summary(
        self, 
        original_summary: str, 
        job_title: str, 
        key_phrases: List[str]
    ) -> str:
        """
        Génère un résumé professionnel adapté au job spécifique
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"""
                Rewrite this professional summary to specifically target a {job_title} role.
                Incorporate these key concepts naturally: {', '.join(key_phrases)}
                
                Keep it concise (2-3 sentences, max 150 words).
                Original summary: {original_summary}
                
                Return ONLY the rewritten summary, no preamble.
                """
            }]
        )
        
        tailored = message.content[0].text
        logger.info(f"Generated tailored summary for {job_title}")
        return tailored.strip()
    
    async def suggest_skill_additions(
        self,
        cv_skills: List[str],
        job_required_skills: List[str]
    ) -> List[str]:
        """
        Suggère des compétences à ajouter au CV pour matcher le job
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": f"""
                CV Skills: {', '.join(cv_skills)}
                Job Required Skills: {', '.join(job_required_skills)}
                
                Suggest 3-5 skills from the job requirements that would improve the CV match.
                Return as JSON array: ["skill1", "skill2", ...]
                """
            }]
        )
        
        response_text = message.content[0].text
        import json
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return []

# Usage
claude_matcher = ClaudeMatcher(api_key="your-api-key")
```

---

## 4️⃣ **src/modules/adaptation/cv_generator.py**

```python
"""
CV Generator : crée une version Word adaptée d'un CV basé sur l'offre
"""

import logging
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class CVGenerator:
    """Génère des fichiers Word de CV adaptés"""
    
    def __init__(self, template_path: str = "templates/cv_template.docx"):
        self.template_path = Path(template_path)
    
    async def generate_tailored_cv(
        self,
        candidate_data: Dict[str, Any],
        job_data: Dict[str, Any],
        adaptations: Dict[str, str]
    ) -> str:
        """
        Crée une version adaptée du CV
        
        Args:
            candidate_data: Infos du candidat (nom, email, expérience, etc.)
            job_data: Données du job (titre, compétences requises, etc.)
            adaptations: Modifications spécifiques (résumé adapté, compétences, etc.)
        
        Returns:
            Chemin du fichier généré
        """
        
        try:
            # Charger template
            if self.template_path.exists():
                doc = Document(self.template_path)
            else:
                doc = Document()  # Créer document vierge
            
            # Ajouter contenu au doc
            self._add_header(doc, candidate_data)
            self._add_summary(doc, adaptations.get('summary', ''))
            self._add_skills(doc, adaptations.get('skills', []))
            self._add_experience(doc, candidate_data, adaptations.get('highlighted_experience', []))
            self._add_education(doc, candidate_data)
            
            # Sauvegarder
            output_path = self._generate_filename(candidate_data, job_data)
            doc.save(output_path)
            
            logger.info(f"CV generated: {output_path}")
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Error generating CV: {e}")
            raise
    
    def _add_header(self, doc: Document, candidate_data: Dict):
        """Ajoute l'en-tête avec infos personnelles"""
        
        # Nom
        name_para = doc.add_paragraph(candidate_data.get('name', ''))
        name_para.style = 'Heading 1'
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Infos de contact
        contact_para = doc.add_paragraph()
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_para.add_run(
            f"{candidate_data.get('email', '')} | "
            f"{candidate_data.get('phone', '')} | "
            f"{candidate_data.get('location', '')}"
        ).font.size = Pt(10)
        
        # Liens (portfolio, LinkedIn, etc.)
        if candidate_data.get('portfolio_url'):
            links_para = doc.add_paragraph()
            links_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            links_para.add_run(candidate_data['portfolio_url']).font.size = Pt(9)
        
        doc.add_paragraph()  # Espacement
    
    def _add_summary(self, doc: Document, summary: str):
        """Ajoute le résumé professionnel"""
        
        if not summary:
            return
        
        doc.add_heading('Professional Summary', level=2)
        doc.add_paragraph(summary)
        doc.add_paragraph()
    
    def _add_skills(self, doc: Document, skills: list):
        """Ajoute la section compétences"""
        
        if not skills:
            return
        
        doc.add_heading('Skills', level=2)
        skills_para = doc.add_paragraph(', '.join(skills))
        skills_para.runs[0].font.size = Pt(11)
        doc.add_paragraph()
    
    def _add_experience(self, doc: Document, candidate_data: Dict, highlighted: list):
        """Ajoute l'expérience professionnelle"""
        
        doc.add_heading('Experience', level=2)
        
        for job in candidate_data.get('experience', []):
            # Titre et entreprise
            exp_para = doc.add_paragraph()
            exp_para.add_run(f"{job['title']} - {job['company']}").bold = True
            
            # Dates
            date_para = doc.add_paragraph(
                f"{job.get('start_date', '')} - {job.get('end_date', '')}",
                style='List Bullet'
            )
            date_para.runs[0].font.italic = True
            date_para.runs[0].font.size = Pt(9)
            
            # Descriptions (mettre en avant celles pertinentes)
            for desc in job.get('descriptions', []):
                if desc in highlighted or not highlighted:
                    doc.add_paragraph(desc, style='List Bullet')
        
        doc.add_paragraph()
    
    def _add_education(self, doc: Document, candidate_data: Dict):
        """Ajoute l'éducation"""
        
        doc.add_heading('Education', level=2)
        
        for edu in candidate_data.get('education', []):
            edu_para = doc.add_paragraph()
            edu_para.add_run(f"{edu['degree']} - {edu['institution']}").bold = True
            edu_para.add_run(f"\n{edu.get('field', '')}")
            doc.add_paragraph()
    
    def _generate_filename(self, candidate_data: Dict, job_data: Dict) -> str:
        """Génère un nom de fichier unique pour chaque version adaptée"""
        
        name = candidate_data['name'].replace(' ', '_')
        job_title = job_data.get('title', 'generic').replace(' ', '_')
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        
        filename = f"CV_{name}_{job_title}_{timestamp}.docx"
        return f"outputs/{filename}"

# Usage
cv_generator = CVGenerator()
```

---

## 5️⃣ **src/modules/storage/drive_manager.py**

```python
"""
Google Drive Manager : upload et gère les fichiers CV et offres
"""

import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveManager:
    """Gère l'upload et l'organisation des fichiers sur Google Drive"""
    
    def __init__(self, credentials_path: str):
        """
        Initialise la connexion à Google Drive
        
        Args:
            credentials_path: Chemin vers le fichier JSON des credentials
                             (obtenu via Google Cloud Console)
        """
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=SCOPES
        )
        self.drive = build('drive', 'v3', credentials=self.creds)
        self.root_folder_id = self._get_or_create_root_folder()
    
    def _get_or_create_root_folder(self) -> str:
        """Crée ou récupère le dossier racine 'Job Search Agent'"""
        
        query = "name='Job Search Agent' and mimeType='application/vnd.google-apps.folder'"
        results = self.drive.files().list(q=query, spaces='drive', pageSize=1).execute()
        
        if results['files']:
            return results['files'][0]['id']
        
        # Créer le dossier
        file_metadata = {
            'name': 'Job Search Agent',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive.files().create(body=file_metadata).execute()
        logger.info(f"Created root folder: {folder['id']}")
        return folder['id']
    
    async def upload_cv(
        self,
        local_path: str,
        job_title: str,
        company_name: str
    ) -> Dict[str, str]:
        """
        Upload un CV adapté dans un dossier organisé par offre
        
        Returns:
            {
                'file_id': 'google-file-id',
                'file_name': 'CV_Name_JobTitle.docx',
                'folder_id': 'google-folder-id',
                'web_url': 'https://drive.google.com/file/d/...'
            }
        """
        
        try:
            # Créer dossier offre si nécessaire
            offer_folder_id = self._get_or_create_offer_folder(
                job_title, 
                company_name
            )
            
            # Upload fichier
            file_metadata = {
                'name': Path(local_path).name,
                'parents': [offer_folder_id]
            }
            
            media = MediaFileUpload(local_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            file = self.drive.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            logger.info(f"Uploaded CV: {file['id']}")
            
            return {
                'file_id': file['id'],
                'file_name': file_metadata['name'],
                'folder_id': offer_folder_id,
                'web_url': file.get('webViewLink', '')
            }
        
        except Exception as e:
            logger.error(f"Error uploading CV: {e}")
            raise
    
    def _get_or_create_offer_folder(self, job_title: str, company_name: str) -> str:
        """Crée ou récupère un dossier pour une offre spécifique"""
        
        folder_name = f"{company_name} - {job_title}"
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and parents='{self.root_folder_id}'"
        
        results = self.drive.files().list(q=query, spaces='drive', pageSize=1).execute()
        
        if results['files']:
            return results['files'][0]['id']
        
        # Créer le dossier
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.root_folder_id]
        }
        folder = self.drive.files().create(body=file_metadata).execute()
        logger.info(f"Created offer folder: {folder['id']}")
        return folder['id']
    
    async def upload_job_offer(
        self,
        offer_data: Dict,
        job_title: str,
        company_name: str
    ) -> str:
        """Sauvegarde les données d'offre en JSON"""
        
        import json
        from tempfile import NamedTemporaryFile
        
        offer_folder_id = self._get_or_create_offer_folder(job_title, company_name)
        
        # Créer fichier JSON temporaire
        with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(offer_data, f, indent=2)
            temp_path = f.name
        
        try:
            file_metadata = {
                'name': f"offer_{job_title.replace(' ', '_')}.json",
                'parents': [offer_folder_id]
            }
            
            media = MediaFileUpload(temp_path, mimetype='application/json')
            file = self.drive.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            
            logger.info(f"Uploaded offer data: {file['id']}")
            return file['id']
        
        finally:
            Path(temp_path).unlink()  # Supprimer fichier temp

# Usage
drive_manager = GoogleDriveManager(credentials_path="./config/google_credentials.json")
```

---

## 6️⃣ **Makefile (complet)**

```makefile
.PHONY: help install test lint format run clean docker-up docker-down docs setup

help:
	@echo "📦 Job Search Agent - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              - Setup complet (venv + dépendances + config)"
	@echo "  make install            - Installer les dépendances"
	@echo ""
	@echo "Development:"
	@echo "  make run                - Lancer l'API localement"
	@echo "  make run-dev            - Lancer avec hot-reload"
	@echo "  make lint               - Vérifier code (flake8, mypy, black)"
	@echo "  make format             - Formatter le code (black)"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - Lancer tous les tests"
	@echo "  make test-unit          - Tests unitaires seulement"
	@echo "  make test-integration   - Tests intégration seulement"
	@echo "  make test-coverage      - Tests avec couverture"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - Builder l'image Docker"
	@echo "  make docker-up          - Démarrer Docker Compose"
	@echo "  make docker-down        - Arrêter Docker Compose"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs               - Générer la documentation"
	@echo "  make docs-serve         - Servir docs localement"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean              - Nettoyer les caches"
	@echo "  make reset-db           - Réinitialiser la base de données"

setup:
	@echo "Setting up Job Search Agent..."
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools wheel
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -e ".[dev]"
	cp .env.example .env
	@echo "✅ Setup complete! Edit .env and run 'make run'"

install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

run:
	python src/api/main.py

run-dev:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v --cov=src --cov-report=html tests/
	@echo "Coverage report: htmlcov/index.html"

test-unit:
	pytest -v tests/unit/

test-integration:
	pytest -v tests/integration/

test-coverage:
	pytest -v --cov=src --cov-report=term-missing tests/

lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null
	rm -f .coverage
	@echo "✅ Cleaned up!"

docker-build:
	docker build -t job-search-agent:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docs:
	cd docs && sphinx-build -b html . _build/html
	@echo "📚 Documentation built: docs/_build/html/index.html"

docs-serve:
	cd docs/_build/html && python -m http.server 8001
	@echo "📖 Docs available at http://localhost:8001"

reset-db:
	rm -f ./test.db
	@echo "✅ Database reset"
```

---

## 7️⃣ **.env.example (complet)**

```bash
# ===== CLAUDE API =====
ANTHROPIC_API_KEY=sk-ant-your-key-here
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=2000
CLAUDE_TEMPERATURE=0.7
CLAUDE_TIMEOUT=30
CLAUDE_MAX_RETRIES=3

# ===== GOOGLE APIS =====
GOOGLE_DRIVE_CREDENTIALS_PATH=./config/google_credentials.json
GOOGLE_SHEETS_ID=your-spreadsheet-id
GOOGLE_SHEETS_RANGE=A1:Z1000

# ===== APPLICATION =====
APP_ENV=development
APP_NAME=job-search-agent
DEBUG=True
LOG_LEVEL=INFO

# ===== DATABASE =====
DATABASE_URL=sqlite:///./test.db
# Pour PostgreSQL: postgresql://user:password@localhost/job_search_db

# ===== SCRAPING =====
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_HEADLESS=True

# ===== JOB BOARDS API KEYS =====
INDEED_API_KEY=your-key
LINKEDIN_API_KEY=your-key
GLASS DOOR_API_KEY=your-key

# ===== EMAIL INTEGRATION =====
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
NOTIFICATION_EMAIL=notifications@example.com

# ===== REDIS (pour caching) =====
REDIS_URL=redis://localhost:6379/0

# ===== FEATURE FLAGS =====
ENABLE_CLAUDE_ADAPTATION=true
ENABLE_AUTO_SCRAPING=false
ENABLE_AUTO_RELANCE=false
ENABLE_PORTFOLIO_LINKING=true

# ===== SECURITY =====
SECRET_KEY=your-super-secret-key-change-in-production
API_KEY_REQUIRED=false

# ===== WORKFLOW =====
SCORING_THRESHOLD=0.6
AUTO_APPLY_MIN_SCORE=0.8
FOLLOWUP_DAYS=3
FOLLOWUP_MESSAGE_TEMPLATE=templates/followup.txt
```

---

## 8️⃣ **pytest.ini**

```ini
[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
    skip_ci: Skip in CI/CD
```

---

## 9️⃣ **docker-compose.yml**

```yaml
version: '3.9'

services:
  app:
    build: .
    container_name: job-search-agent-api
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/job_search
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./outputs:/app/outputs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    networks:
      - job-search-network

  db:
    image: postgres:15-alpine
    container_name: job-search-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: job_search
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - job-search-network

  redis:
    image: redis:7-alpine
    container_name: job-search-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - job-search-network

volumes:
  db_data:
  redis_data:

networks:
  job-search-network:
    driver: bridge
```

