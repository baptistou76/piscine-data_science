import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="piscineds",
    user="bcaumont",
    password="mysecretpassword"
)

print("Connexion réussi !")

cursor = conn.cursor()

cursor.execute("""
    SELECT event_type, COUNT(*) AS event_count
    FROM customers
    GROUP BY event_type
    ORDER BY event_count DESC;
""")

results = cursor.fetchall()

df = pd.DataFrame(results, columns=["event_type", "count"])
print(df)

plt.pie(
    df["count"],
    labels=df["event_type"],
    autopct="%1.1f%%"
)
plt.show()

cursor.close()
conn.close()

