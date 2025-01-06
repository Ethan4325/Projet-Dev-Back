# Analyse et Visualisation de données avec MongoDB,FastAPI et Streamlit

## Description du projet :
Ce projet a pour but d'explorer et comprendre les données en utilisant des outils modernes tels que MongoDB, logiciel dans lequel nous stockons et manipulons les informations. Par ailleurs, FastAPI nous permet de créer des API performantes pour extraire et analyser ces données, tandis que Streamlit offre une interface visuelle simple et intuitive pour présenter de manière claire et interactive.


## Objectifs : 
L'objectif de ce projet est d'explorer différentes étapes clés de la gestion et de la visualisation de données :

- Configurer MongoDB : pour stocker des données de manière flexible.
- Importer des données CSV : pour les organiser efficacement dans la base.
- Créer une API performante avec FastAPI : pour extraire et manipuler les données en temps réel.
- Visualiser les résultats via Streamlit : un outil interactif qui rend les données compréhensibles et accessibles.

## Technologies utilisées : 
- Pourquoi MongoDB ?

On a choisi MongoDB parce qu'il est simple et flexible. C'est une base de données NoSQL, parfaite pour gérer des fichiers CSV et des données sous forme de documents JSON, ce qui correspond parfaitement au projet. Sa structure permet de stocker, organiser et manipuler les données sans avoir à définir un schéma.

À quoi ça sert dans le projet ?

MongoDB sert à stocker toutes les données utilisées dans le projet (exemple : produits, commandes, clients...). Il permet de conserver l'ensemble des informations et de les rendre accessibles pour les requêtes et l'analyse.

- Pourquoi FastAPI ?

On a opté pour FastAPI car il est rapide et moderne pour développer des API. En effet nous avons pu créer des routes web qui ont permi d'interagir avec les données stockées dans MongoDB en quelques lignes de code. Ce que nous avons apprécie, c'est sa documentation automatique via Swagger UI, qui simplifie les tests des requêtes directement depuis le navigateur.

À quoi ça sert dans le projet ?

FastAPI est utilisé pour exposer les données via une API web. Il permet de créer des points d'accès pour récupérer des indicateurs clés de performance (KPI) à partir de la base de données MongoDB.

- Pourquoi Streamlit ?

On a choisi Streamlit car il permet de créer des interfaces web interactives en toute simplicité, sans avoir besoin de coder. En effet grâce à Streamlit, nous avons pu afficher des graphiques, tableaux et indicateurs visuels.

À quoi ça sert dans le projet ?

Streamlit est utilisé pour visualiser les données et KPI de manière claire. Il offre une interface utilisateur interactive qui permet de mieux comprendre les résultats d'analyse et de rendre la présentation plus parlante.

## Prérequis :
Les prérequis, c'est-à-dire les outils nécessaires au bon fonctionnement du projet sont les suivants :

- Python 3 : c'est le langage de programmation utilisé pour le projet.
- MongoDB Community Edition : c'est la base de données NoSQL pour stocker les données.
- Streamlit : c'est une bibliothèque python qui permet de créer des interfaces web interactives.
- FastAPI : c'est un framework python utiliser pour la création d'API rapides et performantes.

## Installation

Voici les différentes étapes d'installation permettant de faire fonctionner le projet : 

- Etape 1 : Récupérer le projet depuis le dépôt GitHub
- Etape 2 : Créer un environnement virtuel:
  python -m venv env
source env/bin/activate  # Sous Linux/Mac
env\Scripts\activate     # Sous Windows

- Etape 3 : Installer toutes les bibliothèques nécessaires listées dans le fichier requirements.txt. Ainsi, cela va automatiquement installer pymongo pour interagir avec MongoDB, fastapi pour gérer l'API et streamlit pour l'interface de visualisation.
  pip install -r requirements.txt

- Etape 4 : Lancer le serveur MongoDB
- Etape 5 : Importer les données dans MongoDB
  python import_data.py

- Etape 6 : Démarrer l'API FastAPI, qui permettra de récupérer les KPI depuis la base de données:
  uvicorn main:app --reload

- Etape 7 : Lancer l'interface Streamlit, pour visualiser les KPI et graphiques:
  streamlit run app.py

## Description des fichiers du projet : 
Voici une brève description des fichiers qui se situent au sein de notre dépôt : 

- app.py : Ce fichier gère l'application Streamlit. Il permet d'afficher les données de manière visuelle et interactive, permettant d'explorer les KPI et comprendre les résultats.
- main.py : Ce fichier est le cœur de l'API FastAPI. Il définit les différentes routes permettant de récupérer et manipuler les données stockées dans MongoDB. C'est ce fichier qui permet d'exposer les données via des requêtes web.
- import_data.py : Ce fichier est un script Python utilisé pour importer les fichiers CSV dans MongoDB. Il facilite la préparation et l'intégration des données afin qu'elles soient prêtes à être utilisées dans l'application.
- mongodb_aggregation.py : Dans ce fichier, on trouve des requêtes d'agrégation MongoDB. Il sert à effectuer des calculs et des analyses avancées sur les données, comme la génération de statistiques et d'indicateurs clés.
- requirements.txt : Ce fichier contient la liste complète des bibliothèques Python nécessaires pour faire fonctionner le projet. Pour les installer, il suffit d'utiliser la commande suivante : pip install -r requirements.txt.

## Etapes d'exécution du code : 
- Lancer l'API :Exécutez la commande uvicorn main:app --reload pour démarrer le backend FastAPI.
- Démarrer Streamlit : Lancer l'application Streamlit avec la commande streamlit run app.py pour la visualisation.

