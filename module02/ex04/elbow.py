import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


dbname = "piscineds"
user = "zstenger"
password = "msp"
host = "localhost"
port = "5432"

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="piscineds",
        user="bcaumont",
        password="mysecretpassword"
    )
    print("Connected to PostgreSQL!")
    cursor = conn.cursor()
    query_purchase = """
    SELECT user_id, COUNT(*) AS purchases
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
    HAVING COUNT(*) < 30
    ORDER BY purchases DESC;
    """
    cursor.execute(query_purchase)
    data = cursor.fetchall()
    print("Query has completed !")
    wss = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(data)
        wss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wss)
    plt.xlabel("Number of clusters")
    plt.title("The Elbow Method")
    plt.show()
except Exception as e:
    print(f"Error: {e}")