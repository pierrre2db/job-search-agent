# Credentials - Guide de Configuration

Ce répertoire contient toutes vos clés API et credentials pour le projet Job Search Agent.

## ⚠️ SÉCURITÉ

**IMPORTANT :** Ne **JAMAIS** commit ces fichiers sur Git ! Le `.gitignore` est configuré pour les ignorer automatiquement.

---

## 📋 Fichiers requis

### 1. **google_credentials.json**
Credentials du Service Account Google Cloud pour accéder à Drive et Sheets.

**Comment l'obtenir :**
- Voir le tutoriel : `../tutorials/setup_google_cloud.md`

### 2. **api_keys.env**
Toutes vos clés API dans un fichier centralisé.

**Format :**
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
INDEED_API_KEY=xxxxx
LINKEDIN_API_KEY=xxxxx
APEC_API_KEY=xxxxx
GLASSDOOR_API_KEY=xxxxx
```

**Comment les obtenir :**
- Anthropic : Voir `../tutorials/setup_anthropic.md`
- Job Boards : Voir `../tutorials/setup_job_boards.md`

### 3. **google_sheets_id.txt** (optionnel)
L'ID de votre Google Sheet pour le dashboard.

**Format :**
```
1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

**Comment l'obtenir :**
L'ID se trouve dans l'URL de votre Google Sheet :
`https://docs.google.com/spreadsheets/d/[VOTRE_ID_ICI]/edit`

---

## 🔄 Chargement des credentials

Le projet charge automatiquement ces credentials depuis ce répertoire.

**Fichier principal :** `src/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Chargé depuis api_keys.env
    anthropic_api_key: str

    # Chargé depuis google_credentials.json
    google_drive_credentials: str = "./config/credentials/google_credentials.json"

    class Config:
        env_file = './config/credentials/api_keys.env'
```

---

## ✅ Checklist de configuration

- [ ] Créer compte Google Cloud
- [ ] Télécharger `google_credentials.json`
- [ ] Créer compte Anthropic
- [ ] Générer API key Anthropic
- [ ] Créer `api_keys.env` avec toutes les clés
- [ ] (Optionnel) Créer Google Sheet et noter l'ID
- [ ] Vérifier que `.gitignore` protège ces fichiers

---

## 🆘 En cas de problème

Si vous avez accidentellement commit des credentials :

1. **Révoquez immédiatement** les clés compromises
2. Générez de nouvelles clés
3. Utilisez `git filter-branch` ou `BFG Repo-Cleaner` pour nettoyer l'historique
4. Vérifiez que `.gitignore` est bien configuré

---
