import streamlit as st
from streamlit_gsheets import GSheetsConnection

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Agenda Escolar Digital", page_icon="📚")

# ESTILO VISUAL (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #0047AB; color: white; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 6px solid #0047AB; margin-bottom: 15px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# LOGIN
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.image("https://cdn-icons-png.flaticon.com/512/3443/3443338.png", width=100) # Logo genérica escolar
    st.title("Acesso dos Pais")
    telefone = st.text_input("Digite seu celular com DDD:")
    
    if st.button("Entrar"):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read()
            if telefone in df['Telefone'].astype(str).values:
                st.session_state.logado = True
                st.session_state.user = df[df['Telefone'].astype(str) == telefone].iloc[0]
                st.rerun()
            else:
                st.error("Número não encontrado no sistema.")
        except:
            st.warning("Configure a planilha nos Secrets do Streamlit para o login funcionar.")

# APP PÓS-LOGIN
else:
    user = st.session_state.user
    st.title(f"Mural: {user['Turma']}")
    st.write(f"Olá, Sr(a). {user['Nome']}")
    
    st.markdown("""
        <div class="card">
            <small>Aviso de Hoje</small>
            <h4>📅 Reunião de Pais</h4>
            <p>Lembramos que amanhã teremos nossa reunião trimestral às 19h.</p>
        </div>
        <div class="card">
            <small>Ontem</small>
            <h4>🍎 Lanche Especial</h4>
            <p>Teremos comemoração de aniversariantes na sexta-feira.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()
