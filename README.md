# Analyse et Visualisation de données avec MongoDB,FastAPI et Streamlit

### Description du projet :
Ce projet a pour but d'explorer et comprendre les données en utilisant des outils modernes tels que MongoDB, logiciel dans lequel nous stockons et manipulons les informations. Par ailleurs, FastAPI nous permet de créer des API performantes pour extraire et analyser ces données, tandis que Streamlit offre une interface visuelle simple et intuitive pour présenter de manière claire et interactive.


### Objectifs : 
L'objectif de ce projet est d'explorer différentes étapes clés de la gestion et de la visualisation de données :

- Configurer MongoDB : pour stocker des données de manière flexible.
- Importer des données CSV : pour les organiser efficacement dans la base.
- Créer une API performante avec FastAPI : pour extraire et manipuler les données en temps réel.
- Visualiser les résultats via Streamlit : un outil interactif qui rend les données compréhensibles et accessibles.


### Prérequis et Installation :
Les prérequis, c'est-à-dire les outils nécessaires au bon fonctionnement du projet sont les suivants :

- Python 3 : c'est le langage de programmation utilisé pour le projet.
- MongoDB Community Edition : c'est la base de données NoSQL pour stocker les données.
- Streamlit : c'est une bibliothèque python qui permet de créer des interfaces web interactives.
- FastAPI : c'est un framework python utiliser pour la création d'API rapides et performantes.

### Description des fichiers du projet
Voici une brève description des fichiers qui se situent au sein de notre dépôt : 

- app.py : Ce fichier gère l'application Streamlit. Il permet d'afficher les données de manière visuelle et interactive, permettant d'explorer les KPI et comprendre les résultats.
- main.py : Ce fichier est le cœur de l'API FastAPI. Il définit les différentes routes permettant de récupérer et manipuler les données stockées dans MongoDB. C'est ce fichier qui permet d'exposer les données via des requêtes web.
- import_data.py : Ce fichier est un script Python utilisé pour importer les fichiers CSV dans MongoDB. Il facilite la préparation et l'intégration des données afin qu'elles soient prêtes à être utilisées dans l'application.
- mongodb_aggregation.py : Dans ce fichier, on trouve des requêtes d'agrégation MongoDB. Il sert à effectuer des calculs et des analyses avancées sur les données, comme la génération de statistiques et d'indicateurs clés.
- requirements.txt : Ce fichier contient la liste complète des bibliothèques Python nécessaires pour faire fonctionner le projet. Pour les installer, il suffit d'utiliser la commande suivante : pip install -r requirements.txt.




