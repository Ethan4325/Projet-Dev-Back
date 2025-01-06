from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db["your_collection_name"]


pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
        }
    },
    {
        '$lookup': {
            'from': 'locations',
            'localField': 'Postal Code',
            'foreignField': 'Postal Code',
            'as': 'locationdetails'
        }
    },
    {
        '$lookup': {
            'from': 'Products',
            'localField': 'Products ID',
            'foreignField': 'Products ID',
            'as': 'ProductsDetail'
        }
    }
]

# Exécution de l'agrégation
try:
    results = collection.aggregate(pipeline)
    for document in results:
        print(document)  
except Exception as e:
    print(f"An error occurred: {e}")
