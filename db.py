# db.py
import sqlite3
import os
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Créer le dossier "data" s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table des élèves
    c.execute('''
        CREATE TABLE IF NOT EXISTS eleves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libelle TEXT,
            montant REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_eleve(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO eleves (nom, date_inscription, montant_inscription, montant_tranche1, montant_tranche2, numero, classe, sexe)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def get_all_eleves():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM eleves ORDER BY classe ASC, nom ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_eleve_by_id(eleve_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM eleves WHERE id = ?", (eleve_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_eleve(eleve_id, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE eleves SET nom=?, date_inscription=?, montant_inscription=?, montant_tranche1=?,
        montant_tranche2=?, numero=?, classe=?, sexe=? WHERE id=?
    """, (*data, eleve_id))
    conn.commit()
    conn.close()

def delete_eleve(eleve_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM eleves WHERE id = ?", (eleve_id,))
    conn.commit()
    conn.close()

def insert_depense(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO depenses (libelle, montant, date) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()

def get_all_depenses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM depenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_total_revenu():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(montant_inscription + montant_tranche1 + montant_tranche2) FROM eleves")
    total = c.fetchone()[0]
    conn.close()
    return total or 0

def get_revenu_par_classe():
    conn = sqlite3.connect("data/school_data.db")
    c = conn.cursor()
    c.execute("""
        SELECT classe, SUM(montant_inscription + montant_tranche1 + montant_tranche2) as total
        FROM eleves GROUP BY classe ORDER BY total DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def get_nb_eleves_par_classe():
    conn = sqlite3.connect("data/school_data.db")
    c = conn.cursor()
    c.execute("SELECT classe, COUNT(*) FROM eleves GROUP BY classe")
    rows = c.fetchall()
    conn.close()
    return rows
