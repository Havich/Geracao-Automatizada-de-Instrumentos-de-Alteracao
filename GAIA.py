import streamlit as st
import sqlite3
import pandas as pd
import hashlib

# --- 1. CONFIGURAÇÕES E SEGURANÇA ---
st.set_page_config(page_title="GAIA", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #006400 !important; text-align: center; font-family: 'Arial'; }
    .stButton>button {
        background-color: #006400; color: white; font-weight: bold;
        border-radius: 8px; width: 100%; height: 50px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FFA500; }
    </style>
""", unsafe_allow_html=True)

def get_db():
    conn = sqlite3.connect('gaia.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# --- 2. ESTADO DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'empresa_id' not in st.session_state: st.session_state.empresa_id = None
if 'user_role' not in st.session_state: st.session_state.user_role = 'Operador'

# --- 3. TELA DE LOGIN ---
def tela_login():
    st.title("GAIA")
    st.subheader("Acesso ao sistema")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")
    
    col1, col2 = st.columns(2)
    if col1.button("ENTRAR"):
        with get_db() as conn:
            user = conn.execute("SELECT nivel_acesso FROM tb_usuario WHERE login=? AND senha_hash=?", 
                            (login, gerar_hash(senha))).fetchone()
        if user:
            st.session_state.user_role = user[0]
            st.session_state.pagina = 'menu'
            st.rerun()
        else: st.error("Acesso negado")
    
    if col2.button("CADASTRE-SE"):
        st.session_state.pagina = 'registrar'
        st.rerun()

def tela_registrar():
    st.subheader("Criar nova conta")
    with st.form("form_reg"):
        novo_u = st.text_input("Novo usuário*")
        senha1 = st.text_input("Nova senha*", type="password")
        senha2 = st.text_input("Confirmar senha*", type="password")
        
        col1, col2 = st.columns(2)
        if col1.form_submit_button("CONFIRMAR"):
            if novo_u and senha1 == senha2:
                try:
                    with get_db() as conn:
                        conn.execute("INSERT INTO tb_usuario (nome, login, senha_hash, nivel_acesso) VALUES (?,?,?,?)",
                                (novo_u, novo_u, gerar_hash(senha1), 'Operador'))
                        conn.commit()
                    st.success("Conta criada!")
                    st.session_state.pagina = 'login'
                    st.rerun()
                except: st.error("Usuário já existe")
            else: st.error("Dados inválidos ou senhas diferentes")
        if col2.form_submit_button("VOLTAR"):
            st.session_state.pagina = 'login'
            st.rerun()

def tela_menu():
    st.title("GAIA")
    st.subheader("Bem vindo!")
    if st.button("Nova alteração"):
        st.session_state.pagina = 'cad_empresa'
        st.rerun()
    if st.session_state.user_role == 'Admin':
        if st.button("Gestão de usuários"):
            st.session_state.pagina = 'gestao_users'
            st.rerun()
    if st.button("Sair da conta"):
        st.session_state.pagina = 'login'
        st.rerun()

def tela_gestao_users():
    st.subheader("Usuários Cadastrados")
    with get_db() as conn:
        users = pd.read_sql_query("SELECT id, nome, login, nivel_acesso FROM tb_usuario", conn)
    st.dataframe(users, hide_index=True, use_container_width=True)
    if st.button("VOLTAR"):
        st.session_state.pagina = 'menu'
        st.rerun()

def tela_empresa():
    st.subheader("DIGITE AS INFORMAÇÕES DA EMPRESA")
    with st.form("f_emp"):
        cnpj = st.text_input("CNPJ*")
        nome = st.text_input("NOME EMPRESARIAL*")
        if st.form_submit_button("SEGUIR"):
            if cnpj and nome:
                try:
                    with get_db() as conn:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO tb_empresa (cnpj, nome_empresarial, nire, cidade, uf, cep, logradouro, numero, bairro) VALUES (?,?,'','','','','','','')", (cnpj, nome))
                        st.session_state.empresa_id = cur.lastrowid
                        conn.commit()
                    st.session_state.pagina = 'lista_socios'
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Erro: CNPJ já cadastrado.")
            else: st.error("Preencha os campos obrigatórios")

def tela_socios():
    st.subheader("INFORME OS DADOS DOS SÓCIOS")
    with get_db() as conn:
        socios = conn.execute("SELECT nome FROM tb_socio WHERE id_empresa=?", (st.session_state.empresa_id,)).fetchall()
    for s in socios: st.write(f"☑ SÓCIO: {s[0]}")
    if st.button("+ (Adicionar Sócio)"):
        st.session_state.pagina = 'cad_socio'
        st.rerun()
    if st.button("SEGUIR"):
        st.session_state.pagina = 'geracao_contrato'
        st.rerun()

def tela_cad_socio():
    st.subheader("CADASTRO DE SÓCIO")
    with st.form("f_s"):
        n = st.text_input("NOME COMPLETO*")
        c = st.text_input("CPF*")
        if st.form_submit_button("CONFIRMAR"):
            with get_db() as conn:
                conn.execute("INSERT INTO tb_socio (id_empresa, nome, cpf, rg, orgao_emissor, estado_civil, profissao, cep, logradouro, numero, bairro, cidade, uf) VALUES (?,?,?,'','','','','','','','','','')", (st.session_state.empresa_id, n, c))
                conn.commit()
            st.session_state.pagina = 'lista_socios'
            st.rerun()
            
def tela_geracao():
    st.subheader("GERAÇÃO DE CLÁUSULAS")
    evento = st.selectbox("Selecione o Evento:", ["220 - Alteração de Nome", "211 - Alteração de Endereço"])
    
    if st.button("GERAR CLÁUSULA"):
        codigo = evento.split(" - ")[0]
        dados_simulados = {'nome': 'Nova Empresa GAIA', 'logradouro': 'Rua Inovação', 'numero': '100'}
        
        if codigo == '220':
            texto = f"CLÁUSULA: A sociedade passará a girar sob o nome empresarial {dados_simulados['nome']}."
            st.code(texto)
        elif codigo == '211':
            texto = f"CLÁUSULA: A sede social é alterada para {dados_simulados['logradouro']}, {dados_simulados['numero']}."
            st.code(texto)
        else:
            st.error("Evento não programado.")
            
    if st.button("FINALIZAR"):
        st.session_state.pagina = 'menu'
        st.rerun()

# --- 4. ROTEAMENTO ---
paginas = {
    'login': tela_login, 'registrar': tela_registrar, 'menu': tela_menu, 
    'gestao_users': tela_gestao_users, 'cad_empresa': tela_empresa,
    'lista_socios': tela_socios, 'cad_socio': tela_cad_socio, 'geracao_contrato': tela_geracao
}
paginas[st.session_state.pagina]()