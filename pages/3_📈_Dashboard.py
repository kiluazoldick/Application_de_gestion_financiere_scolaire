import streamlit as st
import pandas as pd
from fpdf import FPDF
from db import get_connection

st.title("📈 Dashboard")

conn = get_connection()
df = pd.read_sql("SELECT * FROM eleves", conn)

# Vérifier et créer les colonnes manquantes avec 0
for col in ["montant_inscription", "tranche1", "tranche2"]:
    if col not in df.columns:
        df[col] = 0

if df.empty:
    st.warning("Aucune donnée d'élèves trouvée.")
    st.metric("💰 Total revenus", "0 FCFA")
    st.metric("👥 Total élèves", 0)
else:
    df["total_payé"] = df["montant_inscription"].fillna(0) + df["tranche1"].fillna(0) + df["tranche2"].fillna(0)

    revenu_total = df["total_payé"].sum()
    eleves_par_classe = df["classe"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Total revenus", f"{revenu_total:,.0f} FCFA")

    with col2:
        st.metric("👥 Total élèves", len(df))

    st.subheader("📌 Nombre d’élèves par classe")
    st.bar_chart(eleves_par_classe)

    # Calculer les totaux par classe pour chaque tranche
totaux_par_classe = df.groupby("classe").agg({
    "montant_inscription": "sum",
    "tranche1": "sum",
    "tranche2": "sum",
})

totaux_par_classe["total"] = totaux_par_classe.sum(axis=1)

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Revenus par classe", ln=True, align="C")

    pdf.set_font("Arial", "B", 12)
    pdf.ln(10)

    # Header du tableau
    col_widths = [40, 40, 40, 40]
    headers = ["Classe", "Inscription", "Tranche 1", "Tranche 2", "Total"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i] if i < 4 else 40, 10, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 12)

    # Contenu
    for classe, row in data.iterrows():
        pdf.cell(col_widths[0], 10, str(classe), border=1)
        pdf.cell(col_widths[1], 10, f"{row['montant_inscription']:,.0f} FCFA", border=1, align="R")
        pdf.cell(col_widths[2], 10, f"{row['tranche1']:,.0f} FCFA", border=1, align="R")
        pdf.cell(col_widths[3], 10, f"{row['tranche2']:,.0f} FCFA", border=1, align="R")
        pdf.cell(40, 10, f"{row['total']:,.0f} FCFA", border=1, align="R")
        pdf.ln()

    return pdf.output(dest="S").encode("latin1")

pdf_bytes = generate_pdf(totaux_par_classe)

st.download_button(
    label="📥 Télécharger les revenus par classe (PDF)",
    data=pdf_bytes,
    file_name="revenus_par_classe.pdf",
    mime="application/pdf"
)
