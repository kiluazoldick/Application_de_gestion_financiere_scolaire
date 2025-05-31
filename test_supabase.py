import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Connexion
try:
    conn = psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        port=os.getenv("SUPABASE_PORT"),
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD")
    )
    print("✅ Connexion à Supabase réussie !")

    cursor = conn.cursor()

    # 🔄 Création d'une table temporaire de test (facultatif)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            nom TEXT
        );
    """)

    # 🔽 Insertion test
    cursor.execute("INSERT INTO test_table (nom) VALUES (%s)", ("Jean Dupont",))
    conn.commit()

    # 🔼 Lecture test
    cursor.execute("SELECT * FROM test_table ORDER BY id DESC LIMIT 5;")
    rows = cursor.fetchall()
    print("✅ Lecture réussie, derniers enregistrements :")
    for row in rows:
        print(row)

    #✅ Nettoyage 
    cursor.execute("DROP TABLE test_table;")
    conn.commit()

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Erreur de connexion ou requête :", e)
