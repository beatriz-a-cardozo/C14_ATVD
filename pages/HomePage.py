import streamlit as st
import pandas as pd
from src.service.AutenticacaoService import get_usuario_atual

class Home:

    st.set_page_config(
        page_title="Controle Financeiro",
        page_icon="💰",
        layout="wide"
    )

    if "usuario_logado" not in st.session_state:
        st.warning("Você precisa fazer login para acessar esta página.")
        if st.button("Ir para Login"):
            st.switch_page("pages/LoginPage.py")
        st.stop()

    usuarioAtual = get_usuario_atual()

    if usuarioAtual is None:
        st.error("Erro ao carregar dados do usuário.")
        if st.button("Fazer Login Novamente"):
            st.switch_page("pages/LoginPage.py")
        st.stop()

    st.title(f"Bem-vindo, {usuarioAtual.nomeDeUsuario}")

    coluna1,coluna2 = st.columns(2)

    with coluna1:
        usuarioAtual.mostrar_saldo()
        usuarioAtual.mostrar_receitas()

    with coluna2:
        usuarioAtual.mostrar_faturas()
        usuarioAtual.mostrar_gastos_fixo()
        usuarioAtual.mostrar_gastos_do_mes()

