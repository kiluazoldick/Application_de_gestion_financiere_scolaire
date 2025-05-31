import streamlit as st
from db import init_db
init_db()
from dotenv import load_dotenv
import os

load_dotenv()  # charger les variables d'environnement depuis .env

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# initialisation Supabase
from supabase import create_client, Client

supabase: Client = create_client(supabase_url, supabase_key)

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