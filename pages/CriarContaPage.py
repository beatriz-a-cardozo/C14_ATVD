import streamlit as st
from src.service.AutenticacaoService import criar_conta

class CriarConta:

    st.title("Criar Conta")

    coluna1,coluna2,coluna3 = st.columns(3)

    with coluna1:
        pass

    with coluna2:
        nomeDeUsuario = st.text_input("Nome de Usuario")
        senha = st.text_input("Senha",type="password")

        if st.button("Criar Conta"):
            if criar_conta(nomeDeUsuario,senha):
                st.success("Conta criada com sucesso!")
                # adicionar redirecionamento de pagina aqui
            else:
                st.error("Esse nome de usuário já existe.")

    with coluna3:
        pass

