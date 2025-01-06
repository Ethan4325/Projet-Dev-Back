from fastapi import FastAPI
from pymongo import MongoClient

# Initialisation de FastAPI
app = FastAPI()

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]  # Nom de la base de données



# Exemple de KPI : Revenus totaux par produit
@app.get("/kpi/performance_des_produits_par_catégorie")
async def performance_des_produits_par_catégorie():
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



@app.get("/kpi/produits-les-plus-vendus")
async def produits_les_plus_vendus():
    pipeline = [
    {
        "$lookup": {
            "from": "Products",
            "localField": "Product ID",
            "foreignField": "Product ID",
            "as": "ProductsDetail"
        }
    },
    {
        "$unwind": {
            "path": "$ProductsDetail"
        }
    },
    {
        "$group": {
            "_id": "$ProductsDetail.Product Name",  # Utilisation du nom du produit
            "total_units_sold": {
                "$sum": {
                    "$ifNull": [
                        "$Quantity", 0  # Si la quantité est nulle, utiliser 0
                    ]
                }
            }
        }
    },
    {
        "$sort": {
            "total_units_sold": -1  # Trier par unités vendues décroissantes
        }
    },
    {
        "$limit": 5  # Limiter aux 5 produits les plus vendus
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result



@app.get("/kpi/Ventes_Totales_par_Produit")
async def Ventes_Totales_par_Produit():
    pipeline = [
    {
        '$lookup': {
            'from': 'Products',
            'localField': 'Product ID',
            'foreignField': 'Product ID',
            'as': 'ProductsDetail'
        }
    }, {
        '$unwind': {
            'path': '$ProductsDetail'
        }
    }, {
        '$project': {
            'Product Name': '$ProductsDetail.Product Name',
            'Sales_after_discount': {
                '$multiply': [
                    {
                        '$ifNull': [
                            '$Sales', 0
                        ]
                    }, {
                        '$subtract': [
                            1, {
                                '$ifNull': [
                                    '$Discount', 0
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$Product Name',
            'total_sales': {
                '$sum': '$Sales_after_discount'
            }
        }
    }, {
        '$sort': {
            'total_sales': -1
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/Profit_Total_par_Produit")
async def Profit_Total_par_Produit():
    pipeline = [
            {
                '$lookup': {
                    'from': 'Products',
                    'localField': 'Product ID',
                    'foreignField': 'Product ID',
                    'as': 'ProductsDetail'
                }
            }, {
            '$unwind': {
                'path': '$ProductsDetail'
            }
        }, {
            '$group': {
                '_id': '$ProductsDetail.Product Name',
                'total_profit': {
                    '$sum': {
                        '$ifNull': [
                            '$Profit', 0
                        ]
                    }
                }
            }
        }, {
            '$sort': {
                'total_profit': -1
            }
        }
]
    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/Valeur_des_Ventes_par_Produit")
async def Valeur_des_Ventes_par_Produit():
    pipeline = [
    {
        "$lookup": {
            "from": "Products",
            "localField": "Product ID",
            "foreignField": "Product ID",
            "as": "ProductsDetail"
        }
    },
    {
        "$unwind": {
            "path": "$ProductsDetail"
        }
    },
    {
        "$group": {
            "_id": "$ProductsDetail.Product Name",  # Utilisation du nom du produit
            "total_sales": {
                "$sum": {
                    "$ifNull": [
                        "$Sales", 0  # Si la valeur des ventes est nulle, utiliser 0
                    ]
                }
            },
            "total_units_sold": {
                "$sum": {
                    "$ifNull": [
                        "$Quantity", 0  # Si la quantité est nulle, utiliser 0
                    ]
                }
            }
        }
    },
    {
        "$project": {
            "total_sales": 1,
            "total_units_sold": 1,
            "average_sales_value": {
                "$cond": {
                    "if": { "$eq": ["$total_units_sold", 0] },  # Vérifier pour éviter une division par 0
                    "then": 0,
                    "else": {
                        "$divide": ["$total_sales", "$total_units_sold"]
                    }
                }
            }
        }
    },
    {
        "$sort": {
            "average_sales_value": -1  # Trier par valeur moyenne des ventes décroissante
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/total-revenue")
async def total_revenue():
    pipeline = [
    {
        '$lookup': {
            'from': 'customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
        }
    }, {
        '$lookup': {
            'from': 'products',
            'localField': 'Products ID',
            'foreignField': 'Products ID',
            'as': 'ProductsDetails'
        }
    }, {
        '$lookup': {
            'from': 'location',
            'localField': 'Postal Code',
            'foreignField': 'Postal Code',
            'as': 'LocationsDetails'
        }
    }, {
        '$group': {
            '_id': None,
            'totalProfit': {
                '$sum': '$Profit'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'totalProfit': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/top_3_region")
async def top_3_region():
    pipeline = [
        {
            '$lookup': {
                'from': 'locations',
                'localField': 'Postal Code',
                'foreignField': 'Postal Code',
                'as': 'locationdetails'
            }
        },
        {
            '$addFields': {
                'region': {
                    '$arrayElemAt': ['$locationdetails.Region', 0]
                }
            }
        },
        {
            '$group': {
                '_id': '$region',
                'totalSales': {
                    '$sum': '$Sales'
                }
            }
        },
        {
            '$sort': {
                'totalSales': -1  # Trier par ventes totales décroissantes
            }
        },
        {
            '$limit': 3  # Limiter à 3 régions
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/top_5_villes")
async def top_5_villes():
    pipeline = [
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
        '$addFields': {
            'City': {
                '$arrayElemAt': [
                    '$locationdetails.City', 0
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$City',
            'totalSales': {
                '$sum': '$Sales'
            }
        }
    }, {
        '$sort': {
            'totalSales': -1
        }
    }, {
        '$limit': 5
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/chiffre_daffaire")
async def chiffre_daffaire():
    pipeline = [
        {
            "$group": {
                "_id": None,  # Pas de regroupement spécifique, on veut un total global
                "totalSales": { "$sum": "$Sales" }  # Additionne toutes les valeurs de 'Sales' pour le chiffre d'affaire
            }
        },
        {
            "$project": {
                "_id": 0,  # Supprime l'ID de la sortie
                "totalRevenue": "$totalSales"  # Renomme 'totalSales' en 'totalRevenue'
            }
        }
    ]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/total_order")
def total_order():
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
        }
    }, {
        '$lookup': {
            'from': 'Products',
            'localField': 'Product ID',
            'foreignField': 'Product ID',
            'as': 'ProductsDetails'
        }
    }, {
        '$lookup': {
            'from': 'Location',
            'localField': 'Postal Code',
            'foreignField': 'Postal Code',
            'as': 'LocationsDetails'
        }
    }, {
        '$group': {
            '_id': '$Order ID'
        }
    }, {
        '$count': 'total_orders'
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Average_sales_per_order")
def Average_sales_per_order():
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
        }
    }, {
        '$lookup': {
            'from': 'Products',
            'localField': 'Products ID',
            'foreignField': 'Products ID',
            'as': 'ProductsDetails'
        }
    }, {
        '$lookup': {
            'from': 'Location',
            'localField': 'Postal Code',
            'foreignField': 'Postal Code',
            'as': 'LocationsDetails'
        }
    }, {
        '$group': {
            '_id': '$Order ID',
            'totalSales': {
                '$sum': {
                    '$multiply': [
                        '$Sales', {
                            '$subtract': [
                                1, '$Discount'
                            ]
                        }
                    ]
                }
            }
        }
    }, {
        '$group': {
            '_id': None,
            'avgSales': {
                '$avg': '$totalSales'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'avgSales': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/nombre_de_commandes_par_mois")
def nombre_de_commandes_par_mois():
    pipeline = [
    {
        '$group': {
            '_id': {
                'year': {
                    '$year': '$Order Date'
                },
                'month': {
                    '$month': '$Order Date'
                },
                'orderId': '$Order ID'
            }
        }
    }, {
        '$group': {
            '_id': {
                'year': '$_id.year',
                'month': '$_id.month'
            },
            'orderCount': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'year': '$_id.year',
            'month': '$_id.month',
            'orderCount': 1
        }
    }, {
        '$sort': {
            'year': 1,
            'month': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/Nombre_de_Nouveaux_Clients_par_Mois")
def Nombre_de_Nouveaux_Clients_par_Mois():
    pipeline = [
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
            '_id': {
                'yearMonth': {
                    '$dateToString': {
                        'format': '%Y-%m',
                        'date': '$Order Date'
                    }
                },
                'customerId': '$Customer ID'
            }
        }
    }, {
        '$group': {
            '_id': '$_id.yearMonth',
            'newCustomerCount': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Pourcentage_de_clients_rÃ_currents")
def Pourcentage_de_clients_rÃ_currents():
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
            'orderCount': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': None,
            'totalCustomers': {
                '$sum': 1
            },
            'recurrentCustomers': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                '$orderCount', 1
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'pourcentRecurrentClients': {
                '$multiply': [
                    {
                        '$divide': [
                            '$recurrentCustomers', '$totalCustomers'
                        ]
                    }, 100
                ]
            }
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Les_segments_de_clients")
def Les_segments_de_clients():
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
            '_id': '$Segment',
            'totalSales': {
                '$sum': '$Sales'
            }
        }
    }, {
        '$sort': {
            'totalSales': -1
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/total_orders_by_customer_name")
def total_orders_by_customer_name():
    pipeline =[
    {
        '$lookup': {
            'from': 'Customers',
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
        '$unwind': {
            'path': '$CustomersDetails'
        }
    }, {
        '$group': {
            '_id': '$CustomersDetails.Customer Name',
            'totalOrders': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'customerName': '$_id',
            'totalOrders': 1
        }
    }, {
        '$sort': {
            'totalOrders': -1
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Classement des 5 meilleurs clients")
async def Classement_des_5_meilleurs_clients():
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
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
            '_id': '$CustomersDetails.Customer Name',
            'totalPurchased': {
                '$sum': '$Sales'
            }
        }
    }, {
        '$sort': {
            'totalPurchased': -1
        }
    }, {
        '$limit': 5
    }, {
        '$project': {
            '_id': 0,
            'customerId': '$_id',
            'totalPurchased': 1
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/nombre_total_des_commandes_par_state")
async def nombre_total_des_commandes_par_state():
    pipeline= [
    {
        '$lookup': {
            'from': 'Customers',
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
        '$unwind': {
            'path': '$locationdetails',
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$addFields': {
            'state': {
                '$ifNull': [
                    '$locationdetails.State', 'Unknown'
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$state',
            'totalOrders': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'totalOrders': -1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/temps_moyen_de_livraison_par_région_par_jour")
async def temps_moyen_de_livraison_par_région_par_jour():
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
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
        '$addFields': {
            'state': {
                '$ifNull': [
                    {
                        '$arrayElemAt': [
                            '$locationdetails.State', 0
                        ]
                    }, 'Unknown'
                ]
            },
            'deliveryTime': {
                '$cond': {
                    'if': {
                        '$and': [
                            '$Order Date', '$Ship Date'
                        ]
                    },
                    'then': {
                        '$dateDiff': {
                            'startDate': '$Order Date',
                            'endDate': '$Ship Date',
                            'unit': 'day'
                        }
                    },
                    'else': None
                }
            }
        }
    }, {
        '$match': {
            'state': {
                '$ne': 'Unknown'
            },
            'deliveryTime': {
                '$ne': None
            }
        }
    }, {
        '$group': {
            '_id': '$state',
            'avgDeliveryTime': {
                '$avg': '$deliveryTime'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'state': '$_id',
            'avgDeliveryTime': {
                '$round': [
                    '$avgDeliveryTime', 2
                ]
            }
        }
    }, {
        '$sort': {
            'avgDeliveryTime': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/répartition_des_revenus_par_state")
async def répartition_des_revenus_par_state():
    pipeline =[
    {
        '$lookup': {
            'from': 'Customers',
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
        '$addFields': {
            'state': {
                '$ifNull': [
                    {
                        '$arrayElemAt': [
                            '$locationdetails.State', 0
                        ]
                    }, 'Unknown'
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$state',
            'totalRevenue': {
                '$sum': '$Sales'
            }
        }
    }, {
        '$sort': {
            'totalRevenue': -1
        }
    }, {
        '$project': {
            '_id': 0,
            'state': '$_id',
            'totalRevenue': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result


@app.get("/kpi/Répartition_géographique_des_commandes_par_état")
async def Répartition_géographique_des_commandes_par_état():
 pipeline = [
         {
             '$lookup': {
                 'from': 'Customers',
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
         '$addFields': {
             'State': {
                 '$arrayElemAt': [
                     '$locationdetails.State', 0
                 ]
             }
         }
     }, {
         '$group': {
             '_id': '$State',
             'totalOrders': {
                 '$sum': 1
             }
         }
     }, {
         '$project': {
             '_id': 0,
             'state': '$_id',
             'totalOrders': 1
         }
     }
]
 result = list(db.orders.aggregate(pipeline))
 return result

@app.get("/kpi/Nombre moyen de produits par commande")
def Nombre_moyen_de_produits_par_commande():
    pipeline = [
    {
        '$lookup': {
            'from': 'Products',
            'localField': 'Products ID',
            'foreignField': 'Products ID',
            'as': 'ProductsDetails'
        }
    }, {
        '$group': {
            '_id': '$Order ID',
            'totalProducts': {
                '$sum': '$Quantity'
            }
        }
    }, {
        '$group': {
            '_id': None,
            'averageProductsPerOrder': {
                '$avg': '$totalProducts'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'averageProductsPerOrder': 1
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Durée moyenne entre deux commandes du même client")
def Durée_moyenne_entre_deux_commandes_du_même_client():
    pipeline = [
    {
        '$sort': {
            'Customer ID': 1,
            'Order Date': 1
        }
    }, {
        '$group': {
            '_id': '$Customer ID',
            'orderDates': {
                '$push': '$Order Date'
            }
        }
    }, {
        '$project': {
            'timeDiffs': {
                '$map': {
                    'input': {
                        '$zip': {
                            'inputs': [
                                {
                                    '$slice': [
                                        '$orderDates', 1, {
                                            '$size': '$orderDates'
                                        }
                                    ]
                                }, {
                                    '$slice': [
                                        '$orderDates', {
                                            '$subtract': [
                                                {
                                                    '$size': '$orderDates'
                                                }, 1
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    'as': 'pair',
                    'in': {
                        '$subtract': [
                            {
                                '$arrayElemAt': [
                                    '$$pair', 0
                                ]
                            }, {
                                '$arrayElemAt': [
                                    '$$pair', 1
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$unwind': '$timeDiffs'
    }, {
        '$group': {
            '_id': None,
            'avgTimeBetweenOrders': {
                '$avg': '$timeDiffs'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'avgTimeBetweenOrdersInDays': {
                '$divide': [
                    {
                        '$toLong': '$avgTimeBetweenOrders'
                    }, 1000 * 60 * 60 * 24
                ]
            }
        }
    }
]
    result = list(db.orders.aggregate(pipeline))
    return result

@app.get("/kpi/Valeur_Moyenne_Par_Commandes")
def Valeur_Moyenne_Par_Commandes():
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomersDetails'
        }
    }, {
        '$lookup': {
            'from': 'Products',
            'localField': 'Products ID',
            'foreignField': 'Products ID',
            'as': 'ProductsDetails'
        }
    }, {
        '$lookup': {
            'from': 'Location',
            'localField': 'Postal Code',
            'foreignField': 'Postal Code',
            'as': 'LocationsDetails'
        }
    }, {
        '$group': {
            '_id': '$Order ID',
            'totalSales': {
                '$sum': {
                    '$multiply': [
                        '$Sales', {
                            '$subtract': [
                                1, '$Discount'
                            ]
                        }
                    ]
                }
            }
        }
    }, {
        '$group': {
            '_id': None,
            'avgSales': {
                '$avg': '$totalSales'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'avgSales': 1
        }
    }
]

    result = list(db.orders.aggregate(pipeline))
    return result