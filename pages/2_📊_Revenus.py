import streamlit as st
import pandas as pd
from db import get_connection

conn = get_connection()
df = pd.read_sql("SELECT * FROM eleves", conn)

TOTAL_PAYE = "total_payé"  # Constante pour éviter les répétitions

st.title("📊 Revenus par élève et par classe")

# Vérifier et créer les colonnes manquantes avec 0
for col in ["montant_inscription", "tranche1", "tranche2"]:
    if col not in df.columns:
        df[col] = 0

if df.empty:
    st.warning("Aucune donnée d'élèves trouvée.")
else:
    # Calculer total_payé en s'assurant que les NaN sont remplacés par 0
    df[TOTAL_PAYE] = df["montant_inscription"].fillna(0) + df["tranche1"].fillna(0) + df["tranche2"].fillna(0)
    total_revenu = df[TOTAL_PAYE].sum()

    st.metric("💰 Total des revenus", f"{total_revenu:,.0f} FCFA")

    classe_data = df.groupby("classe")[TOTAL_PAYE].sum().sort_values(ascending=False)
    st.bar_chart(classe_data)

    st.subheader("Détail par élève")
    st.dataframe(df[["nom", "classe", TOTAL_PAYE]].sort_values(by="nom"))
