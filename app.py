import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import plotly.express as px
import numpy as np

# URL de base pour les API FastAPI
BASE_URL = "http://localhost:8000/kpi"


# Fonction pour récupérer les données depuis FastAPI
def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return []


# Configuration de la page
st.set_page_config(page_title="Tableau de bord KPI", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    .main { background-color: #1a202c; } /* Bleu nuit */
    .sidebar .sidebar-content { background-color: #e9ecef; color: #000000; } /* Sidebar remains with default text color */
    .card {
        text-align: center; 
        padding: 40px; /* Augmentation de la taille des cartes */
        border-radius: 15px; 
        margin-bottom: 20px;
        height: 180px; /* Taille uniforme pour toutes les cartes */
        display: flex; 
        flex-direction: column;
        justify-content: center; /* Contenu centré verticalement */
        color: #ffffff; /* Texte blanc uniquement pour les cartes */
    }
    .card-green { background-color: #2d6a4f; } /* Vert foncé */
    .card-blue { background-color: #1d3557; } /* Bleu foncé */
    .card-gray { background-color: #6c757d; } /* Gris foncé */
    </style>
    """,
    unsafe_allow_html=True,
)

# Titre de la page
st.title("📊 Tableau de bord KPI")

# Ajouter une barre de sélection pour filtrer les collections
collections = ["Page d'accueil", "produit", "commandes", "localisation", "client"]
selected_collection = st.sidebar.selectbox("Choisissez une collection pour filtrer les KPI :", collections)




# Afficher les KPI de la page d'accueil si aucune collection n'est sélectionnée
if selected_collection == "Page d'accueil":
    st.markdown("## Page d'accueil - Résumé des KPI Global 2020-2023")

    col1, col2, col3 = st.columns(3, gap="large")  # Ajusté pour 3 colonnes uniformes

    # Profit Total
    total_profit_data = fetch_data("total-revenue")
    total_profit = total_profit_data[0]["totalProfit"] if total_profit_data else 0
    with col1:
        st.markdown(
            f"""
            <div class="card card-green">
                <h3>Profit Total</h3>
                <p style="font-size: 28px; font-weight: bold;">${total_profit:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Chiffre d'affaires
    chiffre_affaire_data = fetch_data("chiffre_daffaire")
    total_revenue = chiffre_affaire_data[0]["totalRevenue"] if chiffre_affaire_data else 0
    with col2:
        st.markdown(
            f"""
            <div class="card card-blue">
                <h3>Chiffre d'Affaires</h3>
                <p style="font-size: 28px; font-weight: bold;">${total_revenue:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Nombre total de commandes
    total_orders_data = fetch_data("total_order")
    total_orders = total_orders_data[0]["total_orders"] if total_orders_data else 0
    with col3:
        st.markdown(
            f"""
            <div class="card card-gray">
                <h3>Total des Commandes</h3>
                <p style="font-size: 28px; font-weight: bold;">{total_orders:,}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
# Section pour les Top 5 Villes par Ventes
if selected_collection == "localisation" and st.sidebar.checkbox("Afficher les Top 5 Villes par ventes"):
    st.markdown("### Top 5 des Villes par Ventes")
    top_cities = fetch_data("top_5_villes")
    if top_cities:
        # Conversion des données en DataFrame
        df_cities = pd.DataFrame(top_cities)

        # Renommer les colonnes pour une meilleure lisibilité
        df_cities.rename(columns={"_id": "Ville", "totalSales": "Ventes Totales ($)"}, inplace=True)

        # Trier les données par Ventes Totales décroissantes
        df_cities = df_cities.sort_values(by="Ventes Totales ($)", ascending=False)

        # Ajouter un index à partir de 1
        df_cities.reset_index(drop=True, inplace=True)
        df_cities.index = df_cities.index + 1  # Start index at 1

        # Afficher un tableau interactif
        st.dataframe(df_cities.style.format({"Ventes Totales ($)": "${:,.2f}"}), use_container_width=True)
    else:
        st.write("Aucune donnée disponible.")

# Logique pour les collections spécifiques
else:
    st.markdown(f"## Collection sélectionnée : {selected_collection.capitalize()}")

# 6. Afficher les ventes totales par produit
    if selected_collection == "produit":
        if st.sidebar.checkbox("Afficher les ventes totales par produit (Top 10)"):
            st.subheader("Ventes Totales par Produit (Top 10)")
            total_sales_data = fetch_data("Ventes_Totales_par_Produit")
            if total_sales_data:
                # Conversion des données en DataFrame
                df_sales = pd.DataFrame(total_sales_data)

                # Truncate long product names for better display
                df_sales["_id"] = df_sales["_id"].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)

                # Rename columns for better readability
                df_sales.rename(columns={"_id": "Nom du Produit", "total_sales": "Ventes Totales ($)"}, inplace=True)

                # Trier par "Ventes Totales ($)" en ordre décroissant
                df_sales = df_sales.sort_values(by="Ventes Totales ($)", ascending=False).head(10)

                # Ajouter un index qui commence à 1
                df_sales.reset_index(drop=True, inplace=True)
                df_sales.index = df_sales.index + 1  # Index commence maintenant à 1

                # Afficher le tableau avec un formatage des chiffres
                st.dataframe(df_sales.style.format({"Ventes Totales ($)": "${:,.2f}"}), use_container_width=True)
            else:
                st.write("Aucune donnée disponible pour les ventes totales par produit.")

# 7. Camembert pour le Profit Total par Produit (dans products)
if selected_collection == "produit" and st.sidebar.checkbox("Afficher le profit total par produit"):
    st.subheader("Profit Total par Produit")
    total_profit_data = fetch_data("Profit_Total_par_Produit")  # Appeler l'API pour obtenir les données de profit
    if total_profit_data:
        # Conversion des données en DataFrame
        df_profit = pd.DataFrame(total_profit_data)

        # Renommer les colonnes pour une meilleure lisibilité
        df_profit.rename(columns={'_id': 'Product Name', 'total_profit': 'Total Profit'}, inplace=True)

        # Trier les produits par profit total décroissant et afficher les 10 premiers
        df_profit = df_profit.sort_values(by="Total Profit", ascending=False).head(10)

        # Création du camembert
        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax.pie(
            df_profit["Total Profit"],
            labels=df_profit["Product Name"],
            autopct="%1.1f%%",  # Afficher les pourcentages
            startangle=90,  # Démarrer à 90° pour un meilleur positionnement
            colors=sns.color_palette("pastel"),  # Palette pastel pour des couleurs harmonieuses
        )


        # Titre du graphique
        ax.set_title("Répartition des Profits Totaux par Produit (Top 10)", fontsize=16)

        # Affichage du camembert dans Streamlit
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")

# 8. Pie Chart pour la Performance des Produits par Catégorie (dans products)
if selected_collection == "produit" and st.sidebar.checkbox("Afficher la performance des produits par catégorie"):
    st.subheader("Performance des Produits par Catégorie")
    performance_data = fetch_data("performance_des_produits_par_catégorie")
    if performance_data:
        df_performance = pd.DataFrame(performance_data).groupby("_id")["total_revenue"].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(
            df_performance,
            labels=df_performance.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("pastel"),
        )
        ax.set_title("Répartition des Ventes par Catégorie", fontsize=16)
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")

# 9. Barplot horizontal pour les Produits les Plus Vendus (dans products)
if selected_collection == "produit" and st.sidebar.checkbox("Afficher les produits les plus vendus"):
    st.subheader("Produits les Plus Vendus")
    top_products = fetch_data("produits-les-plus-vendus")
    if top_products:
        df_top_products = pd.DataFrame(top_products)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_top_products, x="total_units_sold", y="_id", palette="crest", ax=ax, orient="h")

        # Ajouter le nombre d'unités vendues à côté de chaque barre
        for i, p in enumerate(ax.patches):
            width = p.get_width()  # Longueur de la barre
            ax.text(
                width + 1,  # Décalage légèrement à droite de la barre
                p.get_y() + p.get_height() / 2,  # Position centrée verticalement
                f"{int(width):,}",  # Nombre formaté avec séparateur de milliers
                ha="left",  # Aligné à gauche de la barre
                va="center",  # Centré verticalement
                fontsize=10,  # Taille de la police
                color="black",  # Couleur du texte
            )

        # Personnalisation des axes et des labels
        ax.set_xlabel("Unités Vendues", fontsize=12)
        ax.set_ylabel("Produit", fontsize=12)
        ax.set_title("Produits les Plus Vendus", fontsize=16)
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")


# 10. Valeur des Ventes par Produit
if selected_collection == "produit" and st.sidebar.checkbox("Afficher la valeur moyenne des ventes par produit"):
    st.subheader("Valeur Moyenne des Ventes par Produit")
    sales_value_data = fetch_data("Valeur_des_Ventes_par_Produit")
    if sales_value_data:
        # Conversion des données en DataFrame
        df_sales_value = pd.DataFrame(sales_value_data)

        # Trier les produits par valeur moyenne décroissante et afficher les 10 premiers
        df_sales_value = df_sales_value.sort_values(by="average_sales_value", ascending=False).head(10)

        # Création du graphique à barres
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_sales_value, x="average_sales_value", y="_id", palette="Blues_d", ax=ax, orient="h")

        # Ajouter les annotations (valeur moyenne des ventes) à côté de chaque barre
        for i, p in enumerate(ax.patches):
            width = p.get_width()  # Longueur de la barre
            ax.text(
                width + 1,  # Décalage légèrement à droite de la barre
                p.get_y() + p.get_height() / 2,  # Position centrée verticalement
                f"${width:,.2f}",  # Format en dollars avec deux décimales
                ha="left",  # Alignement horizontal
                va="center",  # Alignement vertical
                fontsize=10,  # Taille de police
                color="black",  # Couleur du texte
            )

        # Personnalisation des axes et des labels
        ax.set_xlabel("Valeur Moyenne des Ventes ($)", fontsize=12)
        ax.set_ylabel("Produit", fontsize=12)
        ax.set_title("Valeur Moyenne des Ventes par Produit (Top 10)", fontsize=16)

        # Rotation des labels pour les rendre lisibles
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', labelsize=10)

        # Affichage du graphique
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")

# 11. Heatmap pour les Top Régions par Ventes (dans location)
if selected_collection == "localisation" and st.sidebar.checkbox("Afficher les top 3 régions par ventes"):
    st.subheader("Top 3 Régions par Ventes")
    top_regions = fetch_data("top_3_region")
    if top_regions:
        df_regions = pd.DataFrame(top_regions)
        fig = px.imshow(df_regions.pivot(index="_id", columns="totalSales", values="totalSales"),
                        labels=dict(x="Région", y="Ventes", color="Total"),
                        title="Top 3 Régions par Ventes")
        st.plotly_chart(fig)
    else:
        st.write("Aucune donnée disponible.")


# 12. Section Customers : Nouveaux clients par mois
if selected_collection == "client" and st.sidebar.checkbox("Afficher le nombre de nouveaux clients par mois"):
    st.subheader("Nombre de Nouveaux Clients par Mois")
    new_customers_data = fetch_data("Nombre_de_Nouveaux_Clients_par_Mois")
    if new_customers_data:
        # Conversion des données en DataFrame
        df_new_customers = pd.DataFrame(new_customers_data)
        df_new_customers['Mois'] = pd.to_datetime(df_new_customers['_id'])

        # Visualisation avec Plotly
        fig = px.line(
            df_new_customers,
            x='Mois',
            y='newCustomerCount',
            title="Évolution du Nombre de Nouveaux Clients par Mois",
            labels={"Mois": "Mois", "newCustomerCount": "Nouveaux Clients"},
            markers=True
        )
        fig.update_layout(xaxis_title="Mois", yaxis_title="Nombre de Nouveaux Clients", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Aucune donnée disponible.")

# 13. Section Customers : Pourcentage de Clients Récurrents
if selected_collection == "client" and st.sidebar.checkbox("Afficher le pourcentage de clients récurrents"):
    st.subheader("Pourcentage de Clients Récurrents")
    recurrent_clients_data = fetch_data("Pourcentage_de_clients_rÃ_currents")
    if recurrent_clients_data:
        pourcentage_recurrent = recurrent_clients_data[0]['pourcentRecurrentClients']

        # Afficher une carte avec le pourcentage
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #eaf5ff;">
                <h3 style="color: #007bff;">Pourcentage de Clients Récurrents</h3>
                <p style="font-size: 24px; font-weight: bold; color: #007bff;">{pourcentage_recurrent:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("Aucune donnée disponible.")

# 14. Section Customers : Segments de Clients
if selected_collection == "client" and st.sidebar.checkbox("Afficher les segments de clients"):
    st.subheader("Segments de Clients")
    client_segments_data = fetch_data("Les_segments_de_clients")
    if client_segments_data:
        # Conversion des données en DataFrame
        df_segments = pd.DataFrame(client_segments_data)

        # Création d'un graphique à barres
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_segments, x="totalSales", y="_id", palette="pastel", ax=ax, orient="h")

        # Ajouter des annotations pour chaque barre
        for p in ax.patches:
            ax.annotate(
                f"${p.get_width():,.0f}",
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha="left",
                va="center",
                fontsize=10,
                color="black",
                xytext=(5, 0),
                textcoords="offset points",
            )

        ax.set_xlabel("Total des Ventes ($)", fontsize=12)
        ax.set_ylabel("Segment", fontsize=12)
        ax.set_title("Total des Ventes par Segment de Clients", fontsize=16)
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")

# 15. Section Customers : Total des Commandes par Nom de Client (Barres Verticales)
if selected_collection == "client" and st.sidebar.checkbox("Afficher le total des commandes par client"):
    st.subheader("Total des Commandes par Client")
    total_orders_data = fetch_data("total_orders_by_customer_name")
    if total_orders_data:
        # Conversion des données en DataFrame
        df_orders_by_customer = pd.DataFrame(total_orders_data)

        # Tri des données pour une meilleure lisibilité
        df_orders_by_customer = df_orders_by_customer.sort_values(by="totalOrders", ascending=False).head(10)

        # Création d'un graphique à barres verticales
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df_orders_by_customer, x="customerName", y="totalOrders", palette="crest", ax=ax)

        # Ajouter des annotations au-dessus des barres
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():,}",
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha="center",  # Aligné au centre
                va="bottom",  # Aligné en haut
                fontsize=10,
                color="black",
                xytext=(0, 5),  # Légèrement au-dessus de la barre
                textcoords="offset points",
            )

        # Personnalisation des axes et du style
        ax.set_xlabel("Nom du Client", fontsize=12)
        ax.set_ylabel("Total des Commandes", fontsize=12)
        ax.set_title("Total des Commandes par Client", fontsize=16)
        ax.tick_params(axis='x', rotation=45, labelsize=10)  # Rotation des noms de clients
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible.")

# 16. Classement des 5 meilleurs clients
if selected_collection == "client" and st.sidebar.checkbox("Afficher le classement des 5 meilleurs clients"):
    st.subheader("Classement des 5 Meilleurs Clients")
    top_customers_data = fetch_data("Classement des 5 meilleurs clients")  # Fetch the data from the FastAPI endpoint
    if top_customers_data:
        # Convert the data into a DataFrame
        df_customers = pd.DataFrame(top_customers_data)

        # Rename columns for better readability
        df_customers.rename(columns={'customerId': 'Nom du Client', 'totalPurchased': 'Total des Achats ($)'}, inplace=True)

        # Remove brackets from customer names
        df_customers['Nom du Client'] = df_customers['Nom du Client'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # Sort customers by 'Total des Achats ($)' in descending order
        df_customers = df_customers.sort_values(by='Total des Achats ($)', ascending=False)

        # Reset index to start from 1
        df_customers.reset_index(drop=True, inplace=True)
        df_customers.index = df_customers.index + 1

        # Display the table in Streamlit with proper formatting
        st.table(df_customers.style.format({"Total des Achats ($)": "${:,.2f}"}))
    else:
        st.write("Aucune donnée disponible.")

# 17. Logique pour la collection "location"
if selected_collection == "localisation":
    if st.sidebar.checkbox("Afficher le nombre total des commandes par État (Top 10)"):
        st.subheader("Nombre Total des Commandes par État (Top 10)")
        orders_by_state_data = fetch_data("nombre_total_des_commandes_par_state")
        if orders_by_state_data:
            # Conversion des données en DataFrame
            df_orders_by_state = pd.DataFrame(orders_by_state_data)

            # Trier les États par nombre de commandes décroissant et sélectionner les 10 premiers
            df_orders_by_state = df_orders_by_state.sort_values(by="totalOrders", ascending=False).head(10)

            # Création du graphique à barres
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=df_orders_by_state, x="totalOrders", y="_id", palette="cool", ax=ax, orient="h")

            # Ajouter des annotations pour chaque barre
            for p in ax.patches:
                ax.annotate(
                    f"{int(p.get_width()):,}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha="left",
                    va="center",
                    fontsize=10,
                    color="black",
                    xytext=(5, 0),
                    textcoords="offset points",
                )

            # Configuration des axes et du titre
            ax.set_xlabel("Nombre Total de Commandes", fontsize=12)
            ax.set_ylabel("État", fontsize=12)
            ax.set_title("Nombre Total des Commandes par État (Top 10)", fontsize=16)

            # Afficher le graphique
            st.pyplot(fig)
        else:
            st.write("Aucune donnée disponible.")

# 18. Afficher le temps moyen de livraison par région (Pyramide - Top 10)
    if st.sidebar.checkbox("Afficher le temps moyen de livraison par région (Pyramide - Top 10)"):
        st.subheader("Temps Moyen de Livraison par Région (Pyramide - Top 10)")
        avg_delivery_time_data = fetch_data("temps_moyen_de_livraison_par_région_par_jour")
        if avg_delivery_time_data:
            # Conversion des données en DataFrame
            df_avg_delivery_time = pd.DataFrame(avg_delivery_time_data)

            # Sélection des 10 régions avec le temps moyen le plus court
            df_avg_delivery_time = df_avg_delivery_time.nsmallest(10, "avgDeliveryTime")

            # Tri des régions pour un affichage en pyramide
            df_avg_delivery_time = df_avg_delivery_time.sort_values("avgDeliveryTime", ascending=True)

            # Création de la pyramide
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.barh(
                df_avg_delivery_time["state"],
                df_avg_delivery_time["avgDeliveryTime"],
                color=sns.color_palette("mako", len(df_avg_delivery_time)),
            )

            # Annotations sur les barres
            for i, value in enumerate(df_avg_delivery_time["avgDeliveryTime"]):
                ax.text(
                    value + 0.1,  # Position horizontale
                    i,  # Position verticale
                    f"{value:.2f} jours",  # Annotation (temps moyen)
                    va="center",
                    ha="left",
                    fontsize=10,
                    color="black",
                )

            # Configuration des axes
            ax.set_xlabel("Temps Moyen de Livraison (en jours)", fontsize=12)
            ax.set_ylabel("Région", fontsize=12)
            ax.set_title("Temps Moyen de Livraison par Région (Pyramide - Top 10)", fontsize=16)
            ax.invert_yaxis()  # Inversion de l'axe Y pour un effet de pyramide

            # Afficher le graphique
            st.pyplot(fig)
        else:
            st.write("Aucune donnée disponible.")

# 19. Afficher la répartition des revenus par État (Tableau)
    if selected_collection == "localisation":
        if st.sidebar.checkbox("Afficher la répartition des revenus par État (Tableau)"):
            st.subheader("Répartition des Revenus par État (Tableau)")
            revenue_by_state_data = fetch_data("répartition_des_revenus_par_state")
            if revenue_by_state_data:
                # Conversion des données en DataFrame
                df_revenue_by_state = pd.DataFrame(revenue_by_state_data)

                # Renommer les colonnes pour une meilleure lisibilité
                df_revenue_by_state.rename(columns={"state": "État", "totalRevenue": "Revenus Totaux ($)"},
                                           inplace=True)

                # Trier les données par revenus décroissants
                df_revenue_by_state = df_revenue_by_state.sort_values(by="Revenus Totaux ($)", ascending=False)

                # Réinitialiser l'index et le faire commencer à 1
                df_revenue_by_state.reset_index(drop=True, inplace=True)
                df_revenue_by_state.index = df_revenue_by_state.index + 1

                # Afficher un tableau interactif avec le bon format
                st.dataframe(df_revenue_by_state.style.format({"Revenus Totaux ($)": "${:,.2f}"}),
                             use_container_width=True)
            else:
                st.write("Aucune donnée disponible.")

if selected_collection == "commandes":

# 20. Répartition géographique des commandes par état
    if st.sidebar.checkbox("Afficher la Répartition Géographique des Commandes par État"):
        st.subheader("Répartition Géographique des Commandes par État")
        geo_data = fetch_data("Répartition_géographique_des_commandes_par_état")
        if geo_data:
            # Convertir les données en DataFrame
            df_geo = pd.DataFrame(geo_data)

            # Trier les données en ordre décroissant par nombre total de commandes
            df_geo = df_geo.sort_values(by="totalOrders", ascending=False)

            # Réinitialiser les index pour commencer à 1
            df_geo.reset_index(drop=True, inplace=True)
            df_geo.index = df_geo.index + 1  # L'index commence maintenant à 1

            # Afficher le tableau stylisé
            st.dataframe(df_geo.style.format({"totalOrders": "{:,.0f}"}), use_container_width=True)

            # Créer un graphique à barres trié en ordre décroissant
            st.bar_chart(data=df_geo.set_index("state"), y="totalOrders", use_container_width=True)
        else:
            st.write("Aucune donnée disponible pour la répartition géographique des commandes.")

# 21. Nombre moyen de produits par commande
    if st.sidebar.checkbox("Afficher le Nombre Moyen de Produits par Commande"):
        st.subheader("Nombre Moyen de Produits par Commande")
        avg_products_data = fetch_data("Nombre moyen de produits par commande")
        if avg_products_data:
            avg_products = avg_products_data[0]["averageProductsPerOrder"]
            st.markdown(
                f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #E8F0FE; color: #1A73E8;">
                    <h3>Nombre Moyen de Produits par Commande</h3>
                    <p style="font-size: 24px; font-weight: bold;">{avg_products:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.write("Aucune donnée disponible pour le nombre moyen de produits par commande.")

# 22.Durée moyenne entre deux commandes du même client
    if st.sidebar.checkbox("Afficher la Durée Moyenne entre Deux Commandes"):
        st.subheader("Durée Moyenne entre Deux Commandes du Même Client")
        avg_time_data = fetch_data("Durée moyenne entre deux commandes du même client")
        if avg_time_data:
            avg_time = avg_time_data[0]["avgTimeBetweenOrdersInDays"]
            st.markdown(
                f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #FFF3E0; color: #FB8C00;">
                    <h3>Durée Moyenne entre Commandes (en jours)</h3>
                    <p style="font-size: 24px; font-weight: bold;">{avg_time:.2f} jours</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.write("Aucune donnée disponible pour la durée moyenne entre commandes.")

if selected_collection == "commandes":

    # Carte pour la Valeur Moyenne par Commande
    if st.sidebar.checkbox("Afficher la Valeur Moyenne par Commande"):
        st.subheader("Valeur Moyenne par Commande")
        avg_order_value_data = fetch_data("Valeur_Moyenne_Par_Commandes")
        if avg_order_value_data:
            avg_order_value = avg_order_value_data[0]["avgSales"]
            # Carte avec style personnalisé
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    padding: 20px;
                    border-radius: 15px;
                    background-color: #f8f9fa;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <h3 style="color: #007bff;">Valeur Moyenne par Commande</h3>
                    <p style="font-size: 28px; font-weight: bold; color: #28a745;">
                        ${avg_order_value:,.2f}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Aucune donnée disponible pour la valeur moyenne par commande.")


st.sidebar.markdown("Choisissez les indicateurs ci-dessus pour afficher leurs visualisations.")