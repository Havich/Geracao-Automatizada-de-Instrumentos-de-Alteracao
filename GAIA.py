import streamlit as st
from backend import autenticar, cadastrar
import time

# 1. Configuração inicial
st.set_page_config(page_title="GAIA", page_icon="📄", layout="centered")

# Controle de tela (Login ou Cadastro)
if 'tela' not in st.session_state:
    st.session_state['tela'] = 'login'

# 2. CSS Ajuste da página
st.markdown("""
<style>
/* Esconde elementos do sistema */
header, footer, #MainMenu {visibility: hidden !important;}
button[title="View fullscreen"] {display: none !important;}

/* Ajuste de espaçamento */
.block-container {
    padding-top: 0rem !important; 
    padding-bottom: 6rem !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Logo Centralizada e com tamanho Ajustado
_, col_logo, _ = st.columns([1, 7, 1]) 
with col_logo:
    st.image("imagens/logos.png", use_container_width=True)


# 4. LÓGICA DE NAVEGAÇÃO E TELAS
if st.session_state['tela'] == 'login':
    # --- TELA DE LOGIN ---
    
    # Área de login centralizada
    _, col_login, _ = st.columns([1, 3, 1])
    with col_login:
        # Título alinhado com os campos
        st.markdown("<h3 style='margin-top: -60px;'>Acesso ao Sistema</h3>", unsafe_allow_html=True)
        usuario = st.text_input("Login")
        senha = st.text_input("Senha", type="password")

    # Botões alinhados
    _, col_botoes, _ = st.columns([1, 3, 1])
    with col_botoes:
        col_btn1, col_btn2 = st.columns(2, gap="small")
        with col_btn1:
            if st.button("ENTRAR", use_container_width=True):
                if autenticar(usuario, senha):
                    st.success(f"Bem-vindo, {usuario}!")
                    st.balloons()
                    # Seguirá o fluxograma futuro
                else:
                    st.error("Login ou Senha incorretos.")
        with col_btn2:
            if st.button("CADASTRE-SE", use_container_width=True):
                st.session_state['tela'] = 'cadastro'
                st.rerun()

else:
    # --- TELA DE CADASTRO ---
    
    # Área de cadastro centralizada
    _, col_cad, _ = st.columns([1, 3, 1])
    with col_cad:
        # Título alinhado com os campos
        st.markdown("<h3 style='margin-top: -60px;'>Criar Nova Conta</h3>", unsafe_allow_html=True)
        novo_u = st.text_input("Novo Usuário")
        novo_s = st.text_input("Nova Senha", type="password")
    
    # Botões alinhados
    _, col_btn_cad, _ = st.columns([1, 3, 1])
    with col_btn_cad:
        c1, c2 = st.columns(2, gap="small")
        with c1:
            if st.button("CONFIRMAR", use_container_width=True):
                if novo_u and novo_s:
                    if cadastrar(novo_u, novo_s):
                        # 1. Mostra a mensagem de sucesso
                        st.success("✅ Cadastro realizado com sucesso! Redirecionando para o login...")
                        
                        # 2. Faz o sistema esperar 3 segundos
                        time.sleep(3) 
                        
                        # 3. Muda a tela
                        st.session_state['tela'] = 'login'
                        st.rerun()
                    else:
                        st.error("Usuário já existe. Tente outro.")
                else:
                    st.warning("Preencha todos os campos.")
        with c2:
            if st.button("VOLTAR", use_container_width=True):
                st.session_state['tela'] = 'login'
                st.rerun()