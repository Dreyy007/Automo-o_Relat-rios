import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sistema Empresarial", layout="wide")

# =========================
# CARREGAR USUÁRIOS
# =========================
with open("usuarios.json", "r") as f:
    usuarios = json.load(f)

# =========================
# SESSÃO
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

# =========================
# LOGIN
# =========================
def tela_login():
    st.title("🔐 Login do Sistema")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title(f"📊 Bem-vindo, {st.session_state.usuario}")

    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

    # Dados simulados
    df = pd.DataFrame({
        "Departamento": ["TI", "Financeiro", "RH", "TI", "RH"],
        "Status": ["Ativo", "Inativo", "Ativo", "Ativo", "Inativo"],
        "Valor": [1000, 2000, 1500, 3000, 1200]
    })

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Total", df["Valor"].sum())
    col2.metric("Média", int(df["Valor"].mean()))

    st.divider()

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(df, names="Departamento", values="Valor")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(df, x="Departamento", y="Valor", color="Status")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("📋 Dados")
    st.dataframe(df, use_container_width=True)

# =========================
# CONTROLE
# =========================
if st.session_state.logado:
    dashboard()
else:
    tela_login()