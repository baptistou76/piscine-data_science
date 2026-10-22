import psycopg2
import matplotlib.pyplot as plt


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
# PREMIÈRE REQUÊTE SQL
# MONTANT TOTAL DÉPENSÉ PAR CLIENT
# ============================================================

query_monetary = """
SELECT user_id, SUM(price)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
HAVING SUM(price) < 225;
"""

cursor.execute(query_monetary)

data_monetary = cursor.fetchall()

print("Première requête SQL exécutée avec succès !")


# ============================================================
# DEUXIÈME REQUÊTE SQL
# NOMBRE D'ACHATS PAR CLIENT
# ============================================================

query_frequency = """
SELECT user_id, COUNT(*)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id;
"""

cursor.execute(query_frequency)

data_frequency = cursor.fetchall()

print("Deuxième requête SQL exécutée avec succès !")


# ============================================================
# PRÉPARATION DES DONNÉES
# ============================================================

# Nombre d'achats par client
frequency = [
    row[1]
    for row in data_frequency
    if row[1] <= 40
]

# Montant total dépensé par client
monetary = [
    row[1]
    for row in data_monetary
]


print("Données récupérées avec succès !")


# ============================================================
# CRÉATION DES DEUX GRAPHIQUES
# ============================================================

fig, axs = plt.subplots(
    1,
    2,
    figsize=(15, 6)
)


# ============================================================
# GRAPHIQUE 1
# FREQUENCY DISTRIBUTION
# ============================================================

axs[0].hist(
    frequency,
    bins=5,
    edgecolor="k"
)

axs[0].set_title(
    "Frequency distribution of the number of orders per customer"
)

axs[0].set_xlabel("frequency")
axs[0].set_ylabel("customers")

# L'axe va jusqu'à 40 mais la graduation 40 n'est pas affichée
axs[0].set_ylim(0, 60000)
axs[0].set_xticks(range(0, 39, 10))

# L'axe dépasse légèrement 60 000,
# mais 60 000 reste la dernière graduation affichée
axs[0].set_ylim(0, 62000)
axs[0].set_yticks(range(0, 60001, 10000))

axs[0].grid(
    True,
    zorder=-1
)


# ============================================================
# GRAPHIQUE 2
# MONETARY VALUE DISTRIBUTION
# ============================================================

axs[1].hist(
    monetary,
    bins=5,
    edgecolor="k"
)

axs[1].set_title(
    "Frequency distribution of the purchase prices per customer"
)

axs[1].set_xlabel(
    "Monetary value in Altairian Dollars (A$)"
)

axs[1].set_ylabel(
    "Count of customers"
)

# L'axe X dépasse légèrement 200,
# mais 200 reste la dernière graduation affichée
axs[1].set_xlim(-5, 210)
axs[1].set_xticks([0, 50, 100, 150, 200])
# L'axe Y dépasse légèrement 40 000,
# mais 40 000 n'est pas affiché
axs[1].set_ylim(0, 42000)
axs[1].set_yticks(range(0, 40000, 5000))

axs[1].grid(
    True,
       zorder=-1
)

for ax in axs:
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    ax.set_axisbelow(True)

# ============================================================
# AFFICHAGE
# ============================================================

plt.tight_layout()
plt.show()


# ============================================================
# FERMETURE DE LA CONNEXION
# ============================================================

cursor.close()
conn.close()

print("Connexion PostgreSQL fermée.")
