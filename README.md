# events-api API (Serverless)

API REST Serverless de gestion d'événements, développée en **Python 3.9** sur AWS.
Ce projet a été conçu avec une approche **"FinOps First"** pour respecter strictement le Free Tier AWS et les bonnes pratiques de sécurité.

## 📋 Architecture & Choix Techniques

* **Compute** : AWS Lambda (Python 3.9 sur architecture ARM64/Graviton2 pour performance/coût).
* **API** : API Gateway (HTTP API).
* [cite_start]**Base de données** : DynamoDB configurée en mode **Provisioned** (5 RCU/WCU) pour rester sous la limite gratuite des 25 unités[cite: 11, 81].
* [cite_start]**Stockage** : S3 avec chiffrement **SSE-S3** (AES256) et **Block Public Access** activé[cite: 55, 57].
* **IaC** : Template AWS SAM (`template.yaml`).

## 🚀 Runbook : Installation & Déploiement

### Prérequis
* AWS CLI configuré (`aws configure`)
* SAM CLI installé
* Python 3.9+

### 1. Build & Déploiement
```bash
# Compiler le projet
sam build

# Déployer (guidé la première fois)
sam deploy --guided
```

### 2. Utiliser l'API

#### Obtenir tous les évènements :
https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events

<img width="748" height="645" alt="Capture d&#39;écran 2026-01-27 154900" src="https://github.com/user-attachments/assets/3e472d25-fc63-4a7c-8617-e7cbf5f15e4c" />

#### Obtenir un évènement
https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events/726acb77-1a49-4cb7-ac3e-c44012740055

<img width="817" height="495" alt="Capture d&#39;écran 2026-01-27 154924" src="https://github.com/user-attachments/assets/a9b84e79-7780-4e11-aac0-d9fba0f05562" />

#### Creer un évènement
https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events

Exemple de corp de requête :
```json
{
  "title": "Hackathon Serverless",
  "date": "2026-03-15T09:00:00Z",
  "description": "Initiation AWS Lambda",
  "location": "Campus Numérique"
}
```

<img width="599" height="524" alt="Capture d&#39;écran 2026-01-27 154918" src="https://github.com/user-attachments/assets/456623a2-25bd-480e-9516-1c1f35cb6a46" />

#### Uploader une URL d'image
https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events/726acb77-1a49-4cb7-ac3e-c44012740055/upload-url

<img width="1461" height="514" alt="Capture d&#39;écran 2026-01-27 154931" src="https://github.com/user-attachments/assets/66149a54-4d01-44d7-88fe-7fd7a890b278" />

### 3. Lancer les tests
```bash
# Installer les dépendances de test
pip install -r tests/requirements.txt

# Lancer les tests
export PYTHONPATH=$PYTHONPATH:.
pytest tests/unit/test_handlers.py -v
```

### 4. Nettoyage
```bash
sam delete
```

### 5. Exemple de logs via CloudWatch
<img width="1686" height="681" alt="image" src="https://github.com/user-attachments/assets/f4af7b61-10d2-46d9-8c15-44a0d48ee4c1" />
