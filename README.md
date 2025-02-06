# 📌 Projet de Récupération et Analyse des Restaurants Yelp avec AWS Amplify

## 📝 Description

Ce projet permet de récupérer des restaurants depuis l'API Yelp, stocker leurs informations dans **DynamoDB**, scraper les avis à l'aide de **Selenium**, et générer un **nuage de mots** basé sur les avis collectés.  
Il utilise **AWS Amplify**, **DynamoDB**, **S3**, **Lambda**, et **Selenium** pour l'analyse des avis.  

---

## 🚀 Fonctionnalités

- 📡 **Récupération des restaurants** via l'API Yelp et stockage dans DynamoDB.
- 🔍 **Scraping des avis Yelp** à l'aide de **Selenium**.
- 💾 **Stockage des avis** dans une table DynamoDB liée aux restaurants.
- 📊 **Génération d'un nuage de mots** basé sur les avis des restaurants.
- ☁️ **Sauvegarde des données** dans S3 pour analyse.

---

## 🏗️ Installation et Configuration

### 1️⃣ **Cloner le projet**
```sh
git clone https://github.com/ton-repo/ton-projet.git
cd ton-projet
```

### 2️⃣ Configurer AWS Amplify
```sh
npm install -g @aws-amplify/cli
amplify configure
amplify init
amplify push
```

### 3️⃣ Installer les dépendances
```
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
venv\Scripts\activate  # Sur Windows
pip install -r requirements.txt
```

### 4️⃣ Configurer les variables d'environnement
```
YELP_API_KEY=CLE API YELP
```
