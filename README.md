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
[https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events](https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events)

<img width="1127" height="1038" alt="image" src="https://github.com/user-attachments/assets/e752ad2f-b2fc-459a-92f4-f9b2c3126f73" />

#### Obtenir un évènement
[https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events/{id}](https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events/{id})

<img width="1093" height="454" alt="image" src="https://github.com/user-attachments/assets/8aa6a52c-b99b-4aa6-80ce-16e6e0e2a25d" />

#### Creer un évènement
[https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events
](https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events)
Exemple de corp de requête :
```json
{
  "title": "Hackathon Serverless",
  "date": "2026-03-15T09:00:00Z",
  "description": "Initiation AWS Lambda",
  "location": "Campus Numérique"
}
```
<img width="1101" height="575" alt="image" src="https://github.com/user-attachments/assets/18b1c029-d044-4727-b80c-0974bb205d18" />

#### Uploader une URL d'imag

Part 1 : Récupération du lien temporaire 

[https://6u6er7turb.execute-api.eu-north-1.amazonaws.com/events/{id}/upload-url
](https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events/{id}/upload-url)

<img width="1103" height="594" alt="image" src="https://github.com/user-attachments/assets/79f0e7db-0e5a-46b8-bd21-9bd2d6fb7a13" />


Part 2 : Envoi de l'image via l'url récupéré


<img width="1063" height="311" alt="image" src="https://github.com/user-attachments/assets/85e9455f-bbfb-4f80-b3ae-0c02438d3a20" />

<img width="1067" height="235" alt="image" src="https://github.com/user-attachments/assets/31c40ed0-fd1b-4f86-a801-59abda5390f7" />



#### Modifier un évènement

https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events/{id}

Exemple de corp de requête :
```json
{
  "title": "Titre Modifié via Postman",
  "date": "2026-12-25T20:00:00Z",
  "location": "Salle des fêtes",
  "description": "Mise à jour réussie !"
}
```

<img width="1072" height="637" alt="image" src="https://github.com/user-attachments/assets/0113774a-1e51-475e-8721-928b2963c518" />


### Supprimer un évènement

https://hpgp4jvrm4.execute-api.eu-north-1.amazonaws.com/events/{id}

<img width="1093" height="483" alt="image" src="https://github.com/user-attachments/assets/68014a38-928b-433b-bd3e-b9ca84e88115" />


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

### Budget
<img width="1642" height="900" alt="image" src="https://github.com/user-attachments/assets/26f4fa69-3927-4f88-b5c7-79160d4db09c" />

