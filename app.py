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
    st.image("https://cdn-icons-png.flaticon.com/512/3443/3443338.png", width=100)
    st.title("Acesso dos Pais")
    
    # Remove espaços e traços automaticamente do que o usuário digita
    entrada = st.text_input("Digite seu celular com DDD:")
    telefone_limpo = entrada.replace("-", "").replace(" ", "").strip()
    
    if st.button("Entrar"):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # Lê a planilha e garante que todos os títulos de coluna sejam minúsculos
            df = conn.read()
            df.columns = [c.lower() for c in df.columns]
            
            # Converte a coluna de telefone para texto e limpa espaços
            df['telefone'] = df['telefone'].astype(str).str.replace(".0", "", regex=False).str.strip()
            
            if telefone_limpo in df['telefone'].values:
                st.session_state.logado = True
                st.session_state.user = df[df['telefone'] == telefone_limpo].iloc[0]
                st.rerun()
            else:
                st.error("Número não encontrado no sistema.")
        except Exception as e:
            st.warning("Erro de conexão. Verifique se os Secrets estão configurados corretamente.")
            # st.write(e) # Use esta linha apenas para ver o erro real se precisar

# APP PÓS-LOGIN
else:
    user = st.session_state.user
    # Busca 'turma' ou 'nome' em minúsculo conforme sua planilha
    turma = user.get('turma', 'Geral')
    nome = user.get('nome', 'Responsável')
    
    st.title(f"Mural: {turma}")
    st.write(f"Olá, Sr(a). {nome}")
    
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
