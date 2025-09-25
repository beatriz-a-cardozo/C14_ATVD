import streamlit as st

st.set_page_config(page_title="Controle Financeiro")

# Navegação entre páginas
pagina = st.sidebar.selectbox("Navegação", ["Criar Conta", "Login"])

if st.button("Criar Conta"):
    st.switch_page("pages/CriarContaPage.py")

elif st.button("Login"):
    st.switch_page("pages/LoginPage.py")