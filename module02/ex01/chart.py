import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
# GRAPHIQUE 1
# NOMBRE DE CLIENTS PAR JOUR
# ============================================================

cursor.execute("""
    SELECT
        DATE(event_time) AS day,
        COUNT(DISTINCT user_id) AS number_of_customers
    FROM customers
    WHERE event_type = 'purchase'
        AND event_time >= '2022-10-01'
        AND event_time < '2023-03-01'
    GROUP BY DATE(event_time)
    ORDER BY day;
""")

results = cursor.fetchall()

df_customers = pd.DataFrame(
    results,
    columns=[
        "day",
        "number_of_customers"
    ]
)

df_customers["day"] = pd.to_datetime(df_customers["day"])


# ============================================================
# GRAPHIQUE 2
# VENTES TOTALES PAR MOIS
# ============================================================

cursor.execute("""
    SELECT
        DATE_TRUNC('month', event_time) AS month,
        SUM(price) / 1000000.0 AS total_sales
    FROM customers
    WHERE event_type = 'purchase'
        AND event_time >= '2022-10-01'
        AND event_time < '2023-03-01'
    GROUP BY DATE_TRUNC('month', event_time)
    ORDER BY month;
""")

results = cursor.fetchall()

df_sales = pd.DataFrame(
    results,
    columns=[
        "month",
        "total_sales"
    ]
)

df_sales["month"] = pd.to_datetime(df_sales["month"])
df_sales["month_name"] = df_sales["month"].dt.strftime("%b")


# ============================================================
# GRAPHIQUE 3
# DÉPENSE MOYENNE PAR CLIENT ET PAR JOUR
# ============================================================

cursor.execute("""
    SELECT
        DATE(event_time) AS day,
        SUM(price) / COUNT(DISTINCT user_id) AS average_spend
    FROM customers
    WHERE event_type = 'purchase'
        AND event_time >= '2022-10-01'
        AND event_time < '2023-03-01'
    GROUP BY DATE(event_time)
    ORDER BY day;
""")

results = cursor.fetchall()

df_average = pd.DataFrame(
    results,
    columns=[
        "day",
        "average_spend"
    ]
)

df_average["day"] = pd.to_datetime(df_average["day"])


# ============================================================
# AFFICHAGE DES DONNÉES
# ============================================================

print("\nNombre de clients par jour :")
print(df_customers)

print("\nVentes par mois :")
print(df_sales)

print("\nDépense moyenne par client et par jour :")
print(df_average)


# ============================================================
# GRAPHIQUE 1
# NUMBER OF CUSTOMERS
# ============================================================

fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(
    df_customers["day"],
    df_customers["number_of_customers"]
)

ax1.set_title("Number of customers")
ax1.set_ylabel("Number of customers")

# Afficher uniquement les mois sur l'axe X
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

# Supprimer l'espace au début et à la fin
ax1.margins(x=0)

ax1.grid(True, alpha=0.3)

fig1.tight_layout()


# ============================================================
# GRAPHIQUE 2
# TOTAL SALES
# ============================================================

fig2, ax2 = plt.subplots(figsize=(10, 6))

ax2.bar(
    df_sales["month_name"],
    df_sales["total_sales"]
)

ax2.set_title("Total sales in million of Altairian Dollars")
ax2.set_xlabel("Month")
ax2.set_ylabel("Total sales in million of Altairian Dollars")

# L'axe commence à 0
ax2.set_ylim(bottom=0)

# Pas de marge inutile au-dessus des barres
ax2.margins(y=0)

ax2.grid(axis="y", alpha=0.3)

fig2.tight_layout()


# ============================================================
# GRAPHIQUE 3
# AVERAGE SPEND / CUSTOMERS
# ============================================================

fig3, ax3 = plt.subplots(figsize=(10, 6))

ax3.fill_between(
    df_average["day"],
    df_average["average_spend"],
    0,
    alpha=0.5
)

ax3.plot(
    df_average["day"],
    df_average["average_spend"]
)

ax3.set_ylabel("Average spend / customers in Altairian Dollars")

ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

# Petite marge à gauche et à droite
ax3.margins(x=0.02)

# Zoom vertical sur la zone demandée
ax3.set_ylim(28, 42)

ax3.grid(True, alpha=0.3)

fig3.tight_layout()


# ============================================================
# AFFICHAGE DES 3 GRAPHIQUES ENSEMBLE
# ============================================================

plt.show()


# ============================================================
# FERMETURE DE LA CONNEXION
# ============================================================

cursor.close()
conn.close()