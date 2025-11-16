# Setup Google Cloud Platform - Tutoriel Complet

Guide pas-à-pas pour configurer Google Cloud et obtenir les credentials nécessaires.

---

## 🎯 Objectifs

- Créer un projet Google Cloud
- Activer les APIs nécessaires (Drive, Sheets, Gmail)
- Créer un Service Account
- Télécharger les credentials JSON
- Configurer les permissions

---

## 📋 Étape 1 : Créer un projet Google Cloud

1. **Aller sur Google Cloud Console**
   - URL : https://console.cloud.google.com

2. **Se connecter** avec votre compte Google

3. **Créer un nouveau projet**
   - Cliquer sur le menu déroulant en haut (à côté de "Google Cloud")
   - Cliquer sur "New Project"
   - Nom du projet : `job-search-agent`
   - Cliquer sur "Create"

4. **Sélectionner le projet**
   - Une fois créé, sélectionnez-le dans le menu déroulant

---

## 📋 Étape 2 : Activer les APIs

1. **Aller dans "APIs & Services" > "Library"**
   - Menu hamburger ☰ → APIs & Services → Library

2. **Activer Google Drive API**
   - Chercher "Google Drive API"
   - Cliquer dessus
   - Cliquer sur "ENABLE"

3. **Activer Google Sheets API**
   - Chercher "Google Sheets API"
   - Cliquer dessus
   - Cliquer sur "ENABLE"

4. **Activer Gmail API** (optionnel, si vous utilisez Gmail)
   - Chercher "Gmail API"
   - Cliquer dessus
   - Cliquer sur "ENABLE"

---

## 📋 Étape 3 : Créer un Service Account

1. **Aller dans "APIs & Services" > "Credentials"**

2. **Créer un Service Account**
   - Cliquer sur "+ CREATE CREDENTIALS"
   - Sélectionner "Service account"

3. **Configurer le Service Account**
   - **Nom** : `job-search-agent-service`
   - **ID** : (généré automatiquement)
   - **Description** : "Service account for Job Search Agent automation"
   - Cliquer sur "CREATE AND CONTINUE"

4. **Accorder les permissions**
   - Role : "Editor" (ou "Owner" pour full access)
   - Cliquer sur "CONTINUE"
   - Cliquer sur "DONE"

---

## 📋 Étape 4 : Télécharger les credentials JSON

1. **Dans la liste des Service Accounts**
   - Cliquer sur le service account que vous venez de créer

2. **Créer une clé**
   - Aller dans l'onglet "KEYS"
   - Cliquer sur "ADD KEY" > "Create new key"

3. **Choisir le format JSON**
   - Sélectionner "JSON"
   - Cliquer sur "CREATE"

4. **Téléchargement automatique**
   - Un fichier JSON sera téléchargé automatiquement
   - **NOM TYPIQUE** : `job-search-agent-xxxxx-xxxxxxxxx.json`

5. **Renommer et déplacer le fichier**
   ```bash
   # Renommer le fichier
   mv ~/Downloads/job-search-agent-xxxxx-*.json google_credentials.json

   # Déplacer dans le projet
   mv google_credentials.json /chemin/vers/projet/config/credentials/
   ```

---

## 📋 Étape 5 : Partager Google Drive avec le Service Account

**IMPORTANT** : Pour que le service account puisse écrire sur votre Drive, vous devez lui donner accès.

1. **Trouver l'email du Service Account**
   - Ouvrir le fichier `google_credentials.json`
   - Chercher le champ `"client_email"`
   - Exemple : `job-search-agent-service@job-search-agent.iam.gserviceaccount.com`

2. **Partager un dossier Google Drive**
   - Aller sur https://drive.google.com
   - Créer un dossier "Job Search Agent"
   - Clic droit sur le dossier > "Share"
   - Ajouter l'email du service account
   - Donner les permissions "Editor"
   - Cliquer sur "Send"

---

## 📋 Étape 6 : Créer un Google Sheet pour le dashboard

1. **Créer un nouveau Google Sheet**
   - Aller sur https://sheets.google.com
   - Créer un nouveau spreadsheet
   - Nom : "Job Search Dashboard"

2. **Configurer les colonnes**
   ```
   | Titre | Entreprise | Score | Source | URL | Date | Status |
   ```

3. **Partager avec le Service Account**
   - Clic droit sur le Sheet > "Share"
   - Ajouter l'email du service account
   - Permissions : "Editor"

4. **Noter l'ID du Sheet**
   - L'ID se trouve dans l'URL :
   ```
   https://docs.google.com/spreadsheets/d/[VOTRE_ID_ICI]/edit
   ```
   - Copier cet ID et le sauvegarder dans `config/credentials/google_sheets_id.txt`

---

## ✅ Vérification

Votre configuration est complète si vous avez :

- ✅ Un fichier `config/credentials/google_credentials.json`
- ✅ Les APIs Drive et Sheets activées
- ✅ Un dossier Google Drive partagé avec le service account
- ✅ Un Google Sheet partagé avec le service account
- ✅ L'ID du Sheet sauvegardé

---

## 🧪 Tester la connexion

Créer un script de test :

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Charger credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(
    './config/credentials/google_credentials.json',
    scopes=SCOPES
)

# Tester connexion Drive
drive = build('drive', 'v3', credentials=creds)
results = drive.files().list(pageSize=10).execute()
files = results.get('files', [])

print(f"✅ Connexion réussie ! {len(files)} fichiers trouvés.")
```

---

## 🆘 Problèmes courants

### Erreur : "Permission denied"
- Vérifiez que vous avez bien partagé le dossier Drive avec le service account
- Vérifiez que l'email du service account est correct

### Erreur : "API not enabled"
- Retournez dans Google Cloud Console
- Vérifiez que les APIs sont bien activées

### Erreur : "Invalid credentials"
- Re-téléchargez le fichier JSON
- Vérifiez qu'il n'est pas corrompu

---

## 📚 Ressources

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Google Drive API Guide](https://developers.google.com/drive/api/guides/about-sdk)
- [Service Accounts](https://cloud.google.com/iam/docs/service-accounts)

---
