from datetime import datetime
import streamlit as st
import pandas as pd
from pathlib import Path
import json

class Usuario:

    def __init__(self, nomeDeUsuario: str, senhaHash: str, saldo: float = 0, gastoFixo:list = None, gastoDoMes:list = None, fatura:list = None, receitas:list = None):
        self.nomeDeUsuario = nomeDeUsuario
        self.senhaHash = senhaHash
        self.saldo = saldo
        self.gastoFixo = gastoFixo if gastoFixo is not None else []
        self.gastoDoMes = gastoDoMes if gastoDoMes is not None else []
        self.fatura = fatura if fatura is not None else []
        self.receitas = receitas if receitas is not None else []

    # =============================================== MÉTODOS PARA O JSON ==============================================
    def para_diciionario(self) -> dict:
        return {
            "nome_de_usuario": self.nomeDeUsuario,
            "senha_hash": self.senhaHash,
            "saldo": self.saldo,
            "gasto_fixo": self.gastoFixo,
            "gasto_do_mes": self.gastoDoMes,
            "fatura": self.fatura,
            "receitas": self.receitas
        }

    @staticmethod
    def de_dicionario(data: dict):
        usuario = Usuario(data["nome_de_usuario"],data["senha_hash"])

        usuario.saldo = data["saldo"]
        usuario.receitas = data.get("receitas",[])
        usuario.gastoFixo = data.get("gasto_fixo",[])
        usuario.gastoDoMes = data.get("gasto_do_mes", [])
        usuario.fatura = data.get("fatura", [])

        return usuario

    # ============================================= MÉTODOS PARA O USUÁRIO =============================================

    def valor_restante_por_dia(self) -> int: # calcula o a relação do saldo / quantidade de dias que faltam no mes

        hoje = datetime.now()
        mesAtual = hoje.month
        anoAtual = hoje.year

        if mesAtual == 2:
            if anoAtual % 4 and anoAtual % 100 != 0 or anoAtual % 400 == 0:
                mes = 29
            else:
                mes = 28
        elif mesAtual in [1,3,5,7,8,10,12]:
            mes = 31
        else:
            mes = 30

        diasRestantes = mes - hoje.day

        return int(self.saldo / diasRestantes)

    def gerar_relatorio(self,mesAtual) -> None:
        pass

    # ====================================================== SALDO =====================================================
    def calcular_saldo(self) -> float:
        pass

    def mostrar_saldo(self):
        st.markdown("""
                <style>
                    .caixa-saldo {
                        background-color: #FFFFFF;
                        border: 2px solid #1DB954;
                        border-radius: 12px;
                        padding: 24px;
                        margin: 16px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        font-family: 'Arial', sans-serif;
                        color: #191414;
                        font-size: 18px;  /* Fonte aumentada */
                        line-height: 1.5;
                        font-weight: bold;
                    }

                    .texto-verde {
                        color: #1DB954;
                        font-weight: bold;
                    }

                    .texto-laranja {
                        color: #FF8C00;
                        font-weight: bold;
                    }

                    .texto-vermelho {
                        color: #FF4444;
                        font-weight: bold;
                    }

                    .texto-emergencia {
                        color: #CC0000;
                        font-weight: bold;
                        background-color: #FFE6E6;
                        padding: 8px 12px;
                        border-radius: 6px;
                        border: 2px solid #CC0000;
                    }

                    .icone-emergencia {
                        font-size: 24px;
                        margin-right: 8px;
                    }
                </style>
            """, unsafe_allow_html=True)

        texto = f"R$ {self.saldo}"
        if self.valor_restante_por_dia() >= 30:
            cor = "texto-verde"
        elif self.saldo <= 0:
            cor = "texto-emergencia"
            texto = f"⚠️R$ {self.saldo}⚠️"
        elif self.valor_restante_por_dia() <= 12:
            cor = "texto-vermelho"
        else:
            cor = "texto-laranja"

        st.markdown(
            f'<div class="caixa-saldo {cor}">'
            f'{texto}'
            f'</div>',
            unsafe_allow_html=True
        )

    # ===================================================== RECEITA ====================================================
    def adicionar_receita(self,origem,valor,data):
        arq = Path("src/data/usuarios.json")

        with open(arq, "r") as f:
            usuariosInfo = json.load(f)

        novaReceita = {
            "origem": origem,
            "valor": valor,
            "data": data
        }

        usuariosInfo[self.nomeDeUsuario]["receitas"].append(novaReceita)
        usuariosInfo[self.nomeDeUsuario]["saldo"] += valor

        self.receitas.append(novaReceita)
        self.saldo += valor

        with open(arq, "w") as f:
            json.dump(usuariosInfo, f, indent=4)

        return True

    def mostrar_receitas(self):

        st.subheader("📈 Receitas")

        if self.receitas:
            dataframe = pd.DataFrame(self.receitas)

            if not dataframe.empty:
                dataframe["valor"] = dataframe["valor"].apply(
                    lambda x: f"R$ {x:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "origem": "Origem",
                        "valor": "Valor",
                        "data": "Data"
                    }
                )

        else:
            st.info("Nenhuma receita cadastrada ainda.")

        with st.form("novaReceita"):
            st.write("Adicionar nova receita")
            coluna1, coluna2, coluna3 = st.columns(3)

            with coluna1:
                origem = st.text_input("Origem")
            with coluna2:
                valor = st.number_input(
                    "Valor",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )
            with coluna3:
                data = st.date_input("Data de Recebimento")

            enviado = st.form_submit_button("Adicionar receita")

            if enviado:
                if origem and valor > 0:
                    if self.adicionar_receita(origem, valor, data.strftime("%d/%m/%Y")):
                        st.success("Receita adicionada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar a receita.")
                else:
                    st.error("Preencha todos os campos obrigatórios")

    def get_total_receitas(self):
        return sum(receita["valor"] for receita in self.receitas)

    # ===================================================== GASTOS =====================================================
    def adicionar_gasto_fixo(self,gasto, categoria, metodo, valor, data, periodo):
        arq = Path("src/data/usuarios.json")

        with open(arq, "r") as f:
            usuariosInfo = json.load(f)

        novoGasto = {
            "gasto": gasto,
            "categoria": categoria,
            "metodo": metodo,
            "valor": valor,
            "data": data,
            "periodo": periodo
        }

        usuariosInfo[self.nomeDeUsuario]["gasto_fixo"].append(novoGasto)
        if metodo != "Credito":
            usuariosInfo[self.nomeDeUsuario]["saldo"] -= valor
            self.gastoDoMes.append(novoGasto)
            self.saldo -= valor
        else:
            pass

        with open(arq, "w") as f:
            json.dump(usuariosInfo, f, indent=4)

        return True

    def mostrar_gastos_fixo(self):

        st.subheader("📉 Gastos fixos")

        if self.gastoFixo:
            dataframe = pd.DataFrame(self.gastoFixo)

            if not dataframe.empty:
                dataframe["valor"] = dataframe["valor"].apply(
                    lambda x: f"R$ {x:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "gasto": "Gasto",
                        "categoria": "Categoria",
                        "metodo": "Metodo",
                        "valor": "Valor",
                        "data": "Data",
                        "periodo": "Periodo"
                    }
                )

        else:
            st.info("Nenhum gasto fixo cadastrado ainda.")

        with st.form("novoGastoFixo"):
            st.write("Adicionar novo gasto fixo")
            coluna1, coluna2, coluna3, coluna4, coluna5, coluna6 = st.columns(6)

            with coluna1:
                gasto = st.text_input("Gasto")
            with coluna2:
                categoria = st.selectbox(
                    "Categoria:",
                    ("Alimentacao", "Transporte", "Moradia", "Lazer", "Saude","Investimento")
                )
            with coluna3:
                metodo = st.selectbox(
                    "Met. de Pagamento:",
                    ("Debito","Credito","Dinheiro","Pix")
                )
            with coluna4:
                valor = st.number_input(
                    "Valor",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )
            with coluna5:
                data = st.date_input("Data do Pagamento")
            with coluna6:
                periodo = st.number_input(
                    "Periodo",
                    min_value=1,
                    max_value=12
                )

            enviado = st.form_submit_button("Adicionar gasto fixo")

            if enviado:
                if gasto and data and categoria and metodo and valor and periodo > 0:
                    if self.adicionar_gasto_fixo(gasto, categoria, metodo, valor, data.strftime("%d/%m/%Y"), periodo):
                        st.success("Gasto fixo adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar gasto.")
                else:
                    st.error("Preencha todos os campos obrigatórios")

    def adicionar_gasto_do_mes(self, gasto, categoria, metodo, valor, data):
        arq = Path("src/data/usuarios.json")

        with open(arq, "r") as f:
            usuariosInfo = json.load(f)

        novoGasto = {
            "gasto": gasto,
            "categoria": categoria,
            "metodo": metodo,
            "valor": valor,
            "data": data
        }

        usuariosInfo[self.nomeDeUsuario]["gasto_do_mes"].append(novoGasto)
        if metodo != "Credito":
            usuariosInfo[self.nomeDeUsuario]["saldo"] -= valor
            self.gastoFixo.append(novoGasto)
            self.saldo -= valor
        else:
            pass

        with open(arq, "w") as f:
            json.dump(usuariosInfo, f, indent=4)

        return True

    def mostrar_gastos_do_mes(self):

        st.subheader("📉 Gastos do mês")

        if self.gastoDoMes:
            dataframe = pd.DataFrame(self.gastoDoMes)

            if not dataframe.empty:
                dataframe["valor"] = dataframe["valor"].apply(
                    lambda x: f"R$ {x:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "gasto": "Gasto",
                        "categoria": "Categoria",
                        "metodo": "Metodo",
                        "valor": "Valor",
                        "data": "Data"
                    }
                )

        else:
            st.info("Nenhum gasto do mês cadastrado ainda.")

        with st.form("novoGastoDoMes"):
            st.write("Adicionar novo gasto do mês")
            coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)

            with coluna1:
                gasto = st.text_input("Gasto")
            with coluna2:
                categoria = st.selectbox(
                    "Categoria:",
                    ("Alimentacao", "Transporte", "Moradia", "Lazer", "Saude", "Investimento")
                )
            with coluna3:
                metodo = st.selectbox(
                    "Met. de Pagamento:",
                    ("Debito", "Credito", "Dinheiro", "Pix")
                )
            with coluna4:
                valor = st.number_input(
                    "Valor",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )
            with coluna5:
                data = st.date_input("Data do Pagamento")

            enviado = st.form_submit_button("Adicionar gasto do mês")

            if enviado:
                if gasto and data and categoria and metodo and valor > 0:
                    if self.adicionar_gasto_do_mes(gasto, categoria, metodo, valor, data.strftime("%d/%m/%Y")):
                        st.success("Gasto do mês adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar gasto.")
                else:
                    st.error("Preencha todos os campos obrigatórios")

    def adicionar_fatura(self, gasto, valor, data):

        arq = Path("src/data/usuarios.json")

        with open(arq, "r") as f:
            usuariosInfo = json.load(f)

        novaFatura= {
            "gasto": gasto,
            "valor": valor,
            "data": data
        }

        usuariosInfo[self.nomeDeUsuario]["fatura"].append(novaFatura)
        usuariosInfo[self.nomeDeUsuario]["saldo"] -= valor
        self.fatura.append(novaFatura)
        self.saldo -= valor

        with open(arq, "w") as f:
            json.dump(usuariosInfo, f, indent=4)

        return True

    def mostrar_faturas(self):

        st.subheader("📉 Fatura")

        if self.fatura:
            dataframe = pd.DataFrame(self.fatura)

            if not dataframe.empty:
                dataframe["valor"] = dataframe["valor"].apply(
                    lambda x: f"R$ {x:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "gasto": "Gasto",
                        "valor": "Valor",
                        "data": "Data"
                    }
                )

        else:
            st.info("Nenhuma fatura cadastrada ainda.")

        with st.form("novaFatura"):
            st.write("Adicionar nova fatura")
            coluna1, coluna2, coluna3 = st.columns(3)

            with coluna1:
                gasto = st.text_input("Banco")
            with coluna2:
                valor = st.number_input(
                    "Valor",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )
            with coluna3:
                data = st.date_input("Data do Pagamento")

            enviado = st.form_submit_button("Adicionar fatura")

            if enviado:
                if gasto and data and valor > 0:
                    if self.adicionar_fatura(gasto, valor, data.strftime("%d/%m/%Y")):
                        st.success("Fatura adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar fatura.")
                else:
                    st.error("Preencha todos os campos obrigatórios")