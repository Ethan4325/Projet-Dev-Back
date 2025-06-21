# 🧪 Projet-Dev-Back: Data Analysis & Visualization with MongoDB, FastAPI, and Streamlit

## 📘 Project Overview

Welcome to Projet-Dev-Back! This project demonstrates how to build a modern data analysis and visualization pipeline using:

MongoDB: A NoSQL database for flexible and scalable data storage.
FastAPI: A high-performance web framework for building APIs.
Streamlit: A tool for creating interactive web applications for data science.
The goal is to explore and understand data by leveraging these technologies to store, process, and visualize information in an intuitive and efficient manner.

### 🎯 Objectives

The project aims to cover the following key steps in data management and visualization:

MongoDB Setup: Configure MongoDB to store data flexibly.
Data Import: Import data into MongoDB for processing.
API Development: Use FastAPI to create APIs for data extraction and analysis.
Data Visualization: Utilize Streamlit to build an interactive dashboard for data presentation.
🛠️ Technologies Used

MongoDB: NoSQL database for data storage.
FastAPI: Web framework for building APIs.
Streamlit: Framework for creating interactive web applications.
Python: Programming language for scripting and development.
### 🚀 Getting Started

#### To run the project locally, follow these steps 📝:

Clone the Repository:
git clone https://github.com/Ethan4325/Projet-Dev-Back.git
cd Projet-Dev-Back
Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:
pip install -r requirements.txt
Run the Application:
To start the FastAPI server:
uvicorn app:app --reload
To launch the Streamlit dashboard:
streamlit run app.py
Access the Application:
FastAPI docs: http://127.0.0.1:8000/docs
Streamlit dashboard: http://localhost:8501
📂 Project Structure

Projet-Dev-Back/
│
├── app.py              # FastAPI application
├── import_data.py      # Script for importing data into MongoDB
├── main.py             # Main script for data processing
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
#### 🧪 Sample Data

The project includes sample data to demonstrate the functionality. You can import this data into MongoDB using the provided import_data.py script.

#### 📈 Visualizations

The Streamlit dashboard provides interactive visualizations of the data. You can filter and explore the data through various charts and graphs.
