import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2


# ============================================================
# CONNEXION À POSTGRESQL
# ============================================================

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="piscineds",
    user="bcaumont",
    password="mysecretpassword"
)

print("Connexion réussie !")

cursor = conn.cursor()


# ============================================================
# EXERCICE 1 : PRIX DES PRODUITS ACHETÉS
# ============================================================

query = """
SELECT price, user_id
FROM customers
WHERE event_type = 'purchase'
    AND price IS NOT NULL;
"""

cursor.execute(query)

data = cursor.fetchall()

df_purchases = pd.DataFrame(
    data,
    columns=["price", "user_id"]
)

df_purchases["price"] = df_purchases["price"].astype(float)

prices = df_purchases["price"]


# ============================================================
# STATISTIQUES
# ============================================================

print("\nStatistics of purchased items:")
print(prices.describe())


# ============================================================
# GRAPH 1 : FULL BOX PLOT
# ============================================================
# IMPORTANT :
# Toutes les données sont utilisées.
# Aucun filtre n'est appliqué.
# Le graphique montre l'ensemble des valeurs.

plt.figure(figsize=(10, 6))

plt.boxplot(
    prices,
    orientation="horizontal",
    widths=0.5,
    notch=True,
    boxprops=dict(
        facecolor="lightgray",
        edgecolor="black"
    ),
    medianprops=dict(
        linestyle="-",
        linewidth=2,
        color="black"
    ),
    flierprops=dict(
        marker="D",
        markersize=8,
        markerfacecolor="lightgray",
        markeredgecolor="none"
    ),
    patch_artist=True
)

plt.yticks([])
plt.xlabel("Price")
plt.title("Full Box Plot")

plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 2 : INTERQUARTILE RANGE
# ============================================================
# Toutes les données restent utilisées pour calculer le boxplot.
#
# Le xlim() ne supprime aucune donnée.
# Il fait simplement un ZOOM visuel sur la zone intéressante.

plt.figure(figsize=(10, 6))

plt.boxplot(
    prices,
    orientation="horizontal",
    widths=0.5,
    notch=True,
    boxprops=dict(
        facecolor="green",
        edgecolor="black"
    ),
    medianprops=dict(
        linestyle="-",
        linewidth=2,
        color="black"
    ),
    flierprops=dict(
        marker="D",
        markersize=8,
        markerfacecolor="lightgray",
        markeredgecolor="none"
    ),
    patch_artist=True,
    showfliers=False,
)

plt.yticks([])
plt.xlabel("Price")
plt.title("Interquartile range (IQR)")

# ============================================================
# ZOOM UNIQUEMENT VISUEL
# ============================================================
# Les valeurs en dehors de cette zone existent toujours
# dans "prices". Elles sont simplement hors de la fenêtre
# visible du graphique.

plt.xlim(-1, 13)

plt.xticks(np.arange(0, 14, 2))

plt.tight_layout()
plt.show()


# ============================================================
# EXERCICE 3 : PRIX MOYEN DU PANIER PAR UTILISATEUR
# ============================================================

query = """
SELECT user_id, AVG(price) AS avg_cart_price
FROM customers
WHERE event_type = 'cart'
GROUP BY user_id
HAVING AVG(price) BETWEEN 26 AND 43;
"""

cursor.execute(query)

data = cursor.fetchall()

df_basket = pd.DataFrame(
    data,
    columns=[
        "user_id",
        "average_basket_price"
    ]
)

df_basket["average_basket_price"] = (
    df_basket["average_basket_price"].astype(float)
)

avg_cart_prices = df_basket["average_basket_price"]

print(avg_cart_prices.describe())


# ============================================================
# GRAPH 3 : AVERAGE BASKET PRICE PER USER
# ============================================================
#
# ATTENTION :
# Le HAVING BETWEEN 26 AND 43 fait partie de l'énoncé :
# on récupère uniquement les utilisateurs dont la moyenne
# est comprise entre 26 et 43.
#
# Ensuite, aucune donnée récupérée n'est supprimée.
# Le xlim() sert uniquement à zoomer l'affichage.

plt.figure(figsize=(10, 6))

plt.boxplot(
    avg_cart_prices,
    orientation="horizontal",
    widths=0.5,
    notch=True,
    boxprops=dict(
        facecolor="lightblue",
        edgecolor="black"
    ),
    medianprops=dict(
        linestyle="-",
        linewidth=2,
        color="black"
    ),
    flierprops=dict(
        marker="D",
        markersize=8,
        markerfacecolor="black",
        markeredgecolor="none"
    ),
    patch_artist=True,
    whis=0.2,
    showfliers=True
)

plt.yticks([])
plt.xlabel("Price")
plt.title("Average basket price per user")


# ============================================================
# ZOOM VISUEL SUR LA ZONE DEMANDÉE
# ============================================================
# Les données restent toutes présentes dans avg_cart_prices.
#
# On affiche simplement la tranche 27 -> 43.
#
# Cela permet de ne pas avoir un espace inutile au début
# du graphique tout en conservant toutes les données.

plt.xlim(27, 43)

# Graduations tous les 2 €
plt.xticks(np.arange(28, 44, 2))


plt.tight_layout()
plt.show()


# ============================================================
# FERMETURE
# ============================================================

cursor.close()
conn.close()

print("\nConnexion fermée.")