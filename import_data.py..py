from pymongo import MongoClient
import pandas as pd

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']  


def load_collection_to_dataframe(collection_name):
    """Charge une collection MongoDB en DataFrame."""
    collection = db[collection_name]
    data = pd.DataFrame(list(collection.find()))
    return data


if __name__ == "__main__":
    orders_df = load_collection_to_dataframe("orders")
    print("Aperçu des commandes :")
    print(orders_df.head())

    customers_df = load_collection_to_dataframe("customers")
    print("Aperçu des clients :")
    print(customers_df.head())

