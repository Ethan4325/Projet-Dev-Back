# 🧪 Projet-Dev-Back: Data Analysis & Visualization with MongoDB, FastAPI & Streamlit

Welcome to Projet-Dev-Back, a full-stack data pipeline project that combines MongoDB, FastAPI, and Streamlit to demonstrate modern data storage, API creation, and real-time visualization. This project simulates an end-to-end workflow — from data ingestion to interactive dashboards — ideal for data science and backend development practice.

## 📘 Project Overview

Core Components:

MongoDB – Flexible NoSQL database for storing structured and semi-structured data
FastAPI – Lightweight, fast web framework for creating robust RESTful APIs
Streamlit – Python framework for building intuitive, interactive web apps
The objective is to store, retrieve, and visualize data in an efficient and scalable way, ideal for exploratory analysis or backend dashboards.

### 🎯 Objectives

This project walks through the key stages of backend data handling:

MongoDB Setup – Configure a local or remote MongoDB instance to store sample data
Data Import – Use Python to populate the database with structured datasets
API Development – Create RESTful API endpoints using FastAPI for querying and filtering
Visualization – Build a clean, interactive dashboard with Streamlit
#### 🛠️ Tech Stack

Python 3.8+
MongoDB
FastAPI
Streamlit
Uvicorn
Pymongo
#### 🚀 Getting Started

#### 🧰 Clone the Repository
git clone https://github.com/Ethan4325/Projet-Dev-Back.git
cd Projet-Dev-Back
#### 🐍 Set Up Virtual Environment
python -m venv venv
source venv/bin/activate     # For Windows: venv\Scripts\activate
#### 📦 Install Dependencies
pip install -r requirements.txt
#### ▶️ Run the Applications
Start FastAPI backend:

uvicorn app:app --reload
Launch Streamlit dashboard:

streamlit run app.py
#### 🌐 Application URLs

FastAPI Docs: http://127.0.0.1:8000/docs
Streamlit Dashboard: http://localhost:8501
#### 📂 Project Structure

Projet-Dev-Back/
├── app.py              # FastAPI application logic
├── main.py             # Data logic / utilities
├── import_data.py      # MongoDB data importer
├── requirements.txt    # Python packages
└── README.md           # Documentation
#### 🧪 Sample Data

Sample datasets are included (or referenced) for demo purposes. You can populate the MongoDB database using:

python import_data.py
Make sure your MongoDB instance is running and accessible locally (e.g., mongodb://localhost:27017).

#### 📈 Streamlit Dashboard

The dashboard allows users to:

View summary stats and trends
Filter data by parameters
Visualize patterns through bar charts, line graphs, etc.
Add screenshots or GIF previews here for visual appeal.

#### 🤝 Contributing

Contributions are welcome! If you want to add new features, optimize queries, or improve the UI:

Fork this repo
Create a new branch
Submit a pull request
