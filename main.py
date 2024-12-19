from fastapi import FastAPI
from pymongo import MongoClient
from typing import List, Dict

# Initialisation de FastAPI
app = FastAPI()

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]  # Nom de la base de données



# Exemple de KPI : Revenus totaux par produit
@app.get("/kpi/product-performance-by-category")
async def product_performance_by_category():
    pipeline = [
    {
        '$lookup': {
            'from': 'Products',
            'localField': 'Product ID',
            'foreignField': 'Product ID',
            'as': 'ProductsDetail'
        }
    }, {
        '$project': {
            'ProductsDetail': {
                '$arrayElemAt': [
                    '$ProductsDetail', 0
                ]
            },
            'Sales': 1,
            'Quantity': 1
        }
    }, {
        '$group': {
            '_id': '$ProductsDetail.Category',
            'total_revenue': {
                '$sum': {
                    '$ifNull': [
                        '$Sales', 0
                    ]
                }
            },
            'total_units_sold': {
                '$sum': {
                    '$ifNull': [
                        '$Quantity', 0
                    ]
                }
            },
            'average_price_per_unit': {
                '$avg': {
                    '$ifNull': [
                        {
                            '$divide': [
                                {
                                    '$ifNull': [
                                        '$Sales', 0
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$Quantity', 1
                                    ]
                                }
                            ]
                        }, 0
                    ]
                }
            }
        }
    }
]
    # Perform the aggregation query asynchronously
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/orders-per-customer")
async def orders_per_customer():
    pipeline = [
        {"$group": {"_id": "$Customer ID", "total_orders": {"$sum": 1}}},
        {"$sort": {"total_orders": -1}}
    ]
    result = list(db.orders.aggregate(pipeline))
    return {"data": result}

# KPI : Revenus totaux par produit
@app.get("/kpi/revenue-per-product")
async def revenue_per_product():
    pipeline = [
        {"$group": {"_id": "$Product ID", "total_revenue": {"$sum": "$Price"}}},
        {"$sort": {"total_revenue": -1}}
    ]
    result = list(db.orders.aggregate(pipeline))
    return  result


@app.get("/kpi/total_orders")
async def total_orders():
    pipeline =[
        {
            '$lookup': {
                'from': 'Customerustomers',
                'localField': 'Customer ID',
                'foreignField': 'Customer ID',
                'as': 'CustomersDetails'
            }
        }, {
            '$lookup': {
                'from': 'locations',
                'localField': 'Postal Code',
                'foreignField': 'Postal Code',
                'as': 'locationdetails'
            }
        }, {
            '$lookup': {
                'from': 'Products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'ProductsDetail'
            }
        }, {
            '$group': {
                '_id': '$Customer ID',
                'total_order': {
                    '$sum': 1
                }
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    return {"data": result}

@app.get("/kpi/estimated_profit_margin")
async def estimated_profit_margin():
    pipeline = [
    {
        '$lookup': {
            'from': 'Products',
            'localField': 'Product ID',
            'foreignField': 'Product ID',
            'as': 'ProductsDetail'
        }
    }, {
        '$group': {
            '_id': {
                '$ifNull': [
                    '$ProductsDetail.Category', 'Unknown Category'
                ]
            },
            'total_revenue': {
                '$sum': {
                    '$ifNull': [
                        '$Sales', 0
                    ]
                }
            },
            'total_units_sold': {
                '$sum': {
                    '$ifNull': [
                        '$Quantity', 0
                    ]
                }
            },
            'total_profit': {
                '$sum': {
                    '$ifNull': [
                        '$Profit', 0
                    ]
                }
            }
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

