import streamlit as st
import sqlite3
from db import get_connection
import pandas as pd

conn = get_connection()
cursor = conn.cursor()

st.title("💸 Gestion des dépenses")

with st.form("form_depense"):
    libelle = st.text_input("Libellé de la dépense")
    montant = st.number_input("Montant (FCFA)")
    date = st.date_input("Date")

    if st.form_submit_button("Ajouter la dépense"):
        cursor.execute("INSERT INTO depenses (libelle, montant, date) VALUES (?, ?, ?)", (libelle, montant, date.strftime("%Y-%m-%d")))
        conn.commit()
        st.success("Dépense ajoutée.")

df_dep = pd.read_sql("SELECT * FROM depenses", conn)
st.subheader("📄 Liste des dépenses")
st.dataframe(df_dep)