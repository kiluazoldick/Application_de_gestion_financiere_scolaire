import streamlit as st
import sqlite3
from db import get_all_eleves, update_eleve, delete_eleve, insert_eleve
import pandas as pd

st.set_page_config(page_title="Liste des élèves", layout="wide")

st.markdown("<h1 style='text-align: center;'>👤 Liste des élèves</h1>", unsafe_allow_html=True)

# Liste complète des classes
classes = [
    "Petite Section", "Moyenne Section", "Grande Section",
    "SIL", "CP", "CE1", "CE2", "CM1", "CM2",
    "Nursery 1", "Nursery 2", "Nursery 3",
    "CLASS 1", "CLASS 2", "CLASS 3", "CLASS 4", "CLASS 5", "CLASS 6"
]

# Formulaire d'ajout
with st.expander("➕ Ajouter un élève"):
    with st.form("form_ajout"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom de l'élève")
            sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
            date_inscription = st.date_input("Date d'inscription")
            telephone = st.text_input("Numéro de téléphone")
        with col2:
            classe = st.selectbox("Classe", classes)
            montant_inscription = st.number_input("Montant d'inscription", min_value=0.0)
            tranche1 = st.number_input("Montant 1ère tranche", min_value=0.0)
            tranche2 = st.number_input("Montant 2ème tranche", min_value=0.0)

        if st.form_submit_button("Ajouter l'élève"):
            data = (
                nom, date_inscription.strftime("%Y-%m-%d"),
                montant_inscription, tranche1, tranche2,
                telephone, classe, sexe
            )
            insert_eleve(data)
            st.success("✅ Élève ajouté avec succès")

# Liste des élèves
eleves = get_all_eleves()

st.markdown("## 📋 Liste des élèves")
if not eleves:
    st.info("Aucun élève enregistré.")
else:
    for eleve in eleves:
        with st.expander(f"{eleve[1]} ({eleve[7]})"):
            st.write(f"📅 Date d'inscription : `{eleve[2]}`")
            st.write(f"📞 Téléphone : `{eleve[6]}`")
            st.write(f"💰 Inscription : `{eleve[3]} FCFA` | Tranche 1 : `{eleve[4]} FCFA` | Tranche 2 : `{eleve[5]} FCFA`")
            st.write(f"👫 Sexe : `{eleve[8]}`")

            total = eleve[3] + eleve[4] + eleve[5]
            st.markdown(f"### 💵 Total payé : `{total} FCFA`")

            with st.form(f"form_modif_{eleve[0]}"):
                col1, col2 = st.columns(2)
                with col1:
                    new_nom = st.text_input("Nom", eleve[1])
                    new_sexe = st.selectbox("Sexe", ["Masculin", "Féminin"], index=0 if eleve[8] == "Masculin" else 1)
                    new_date = st.date_input("Date d'inscription", value=pd.to_datetime(eleve[2]))
                    new_tel = st.text_input("Téléphone", eleve[6])
                with col2:
                    # Sécurité sur la classe : utiliser la 1ère classe si inconnue
                    selected_class = eleve[7] if eleve[7] in classes else classes[0]
                    new_classe = st.selectbox("Classe", classes, index=classes.index(selected_class))
                    new_ins = st.number_input("Inscription", value=eleve[3])
                    new_tr1 = st.number_input("Tranche 1", value=eleve[4])
                    new_tr2 = st.number_input("Tranche 2", value=eleve[5])

                col3, col4 = st.columns([1, 1])
                submit_modif = col3.form_submit_button("💾 Modifier")
                submit_delete = col4.form_submit_button("🗑 Supprimer")

                if submit_modif:
                    update_eleve(eleve[0], (
                        new_nom, new_date.strftime("%Y-%m-%d"),
                        new_ins, new_tr1, new_tr2,
                        new_tel, new_classe, new_sexe
                    ))
                    st.success("Élève modifié avec succès.")
                    st.experimental_rerun()

                if submit_delete:
                    delete_eleve(eleve[0])
                    st.warning("Élève supprimé.")
                    st.experimental_rerun()

# Fermeture automatique de la sidebar sur mobile
st.markdown("""
    <script>
    const sidebar = parent.document.querySelector('section[data-testid="stSidebar"]');
    document.body.addEventListener('click', function() {
        if (window.innerWidth < 768 && sidebar && sidebar.style) {
            sidebar.style.transform = "translateX(-100%)";
        }
    });
    </script>
""", unsafe_allow_html=True)