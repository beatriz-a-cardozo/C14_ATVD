import streamlit as st

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="💰",
    layout="centered"
)

st.title("Bem-vindo ao Controle Financeiro!")

coluna1,coluna2,coluna3 = st.columns(3)

st.markdown("""
    <style>
        .main .block-container {
            padding-top: 5rem;
        }
        .stButton > button {
            width: 200px;
            height: 50px;
            background-color: #191414;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1ed760;
            color: #191414;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

with coluna1:
    pass

with coluna2:
    st.markdown(
        "<div style='display: flex;"
        "flex-direction: column;"
        "align-items: center;'>",
        unsafe_allow_html=True
    )

    if st.button("Criar Conta", key="criar_conta"):
        st.switch_page("pages/CriarContaPage.py")

    if st.button("Login", key="login"):
        st.switch_page("pages/LoginPage.py")

    st.markdown("</div>", unsafe_allow_html=True)

with coluna3:
    pass