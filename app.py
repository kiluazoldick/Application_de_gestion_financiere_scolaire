import streamlit as st
from db import init_db
init_db()


st.set_page_config(page_title="L'avenir du peuple Gestion Fianciere", layout="wide")
init_db()

st.title("📚 Application de gestion financière L'avenir du peuple")
st.markdown("""
Bienvenue dans l’interface de gestion. Utilisez le menu à gauche pour accéder aux fonctionnalités :
- Ajouter et consulter les élèves
- Voir les revenus
- Ajouter des dépenses
- Accéder au tableau de bord
""")