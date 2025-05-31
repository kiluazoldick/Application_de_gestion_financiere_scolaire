# db.py
import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        port=os.getenv("SUPABASE_PORT"),
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        sslmode="require"
    )

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Table des élèves
    c.execute('''
        CREATE TABLE IF NOT EXISTS eleves (
            id SERIAL PRIMARY KEY,
            nom TEXT,
            date_inscription TEXT,
            montant_inscription REAL,
            montant_tranche1 REAL,
            montant_tranche2 REAL,
            numero TEXT,
            classe TEXT,
            sexe TEXT
        )
    ''')

    # Table des dépenses
    c.execute('''
        CREATE TABLE IF NOT EXISTS depenses (
            id SERIAL PRIMARY KEY,
            libelle TEXT,
            montant REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_eleve(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO eleves (nom, date_inscription, montant_inscription, montant_tranche1, montant_tranche2, numero, classe, sexe)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    conn.close()

def get_all_eleves():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM eleves ORDER BY classe ASC, nom ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_eleve_by_id(eleve_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM eleves WHERE id = %s", (eleve_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_eleve(eleve_id, data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE eleves SET nom=%s, date_inscription=%s, montant_inscription=%s, montant_tranche1=%s,
        montant_tranche2=%s, numero=%s, classe=%s, sexe=%s WHERE id=%s
    """, (*data, eleve_id))
    conn.commit()
    conn.close()

def delete_eleve(eleve_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM eleves WHERE id = %s", (eleve_id,))
    conn.commit()
    conn.close()

def insert_depense(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO depenses (libelle, montant, date) VALUES (%s, %s, %s)", data)
    conn.commit()
    conn.close()

def get_all_depenses():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM depenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_total_revenu():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(montant_inscription + montant_tranche1 + montant_tranche2) FROM eleves")
    total = c.fetchone()[0]
    conn.close()
    return total or 0

def get_revenu_par_classe():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT classe, SUM(montant_inscription + montant_tranche1 + montant_tranche2) as total
        FROM eleves GROUP BY classe ORDER BY total DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def get_nb_eleves_par_classe():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT classe, COUNT(*) FROM eleves GROUP BY classe")
    rows = c.fetchall()
    conn.close()
    return rows
