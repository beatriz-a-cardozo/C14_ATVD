import streamlit as st
from src.service.AutenticacaoService import login


class Login:
    st.title("Login")

    coluna1,coluna2,coluna3 = st.columns(3)

    with coluna1:
        pass

    with coluna2:
        nomeDeUsuario = st.text_input("Nome de usuario")
        senha = st.text_input("Senha",type="password")

        if st.button("Login"):
            if login(nomeDeUsuario,senha):
                st.success("Logado com sucesso")
                st.session_state["user"] = nomeDeUsuario
                # adicionar redirecionamento de pagina aqui
            else:
                st.error("Usuário ou senha incorretos.")

