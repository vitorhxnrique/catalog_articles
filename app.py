import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Anais do Washes | 2021-2025", layout="wide", page_icon="🔖")

st.markdown("""
    <style>
    /* Remove espaços e linhas excessivas */
    .block-container { padding-top: 1.5rem; }
    
    .artigo-container {
        padding: 10px 0px;
        margin-bottom: 10px;
    }
    .titulo-texto {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ff4b4b; /* Cor vermelha para o título */
        margin-bottom: 2px;
    }
    .meta-dados {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 5px;
    }
    .tag-area {
        font-size: 0.75rem;
        background-color: #f0f2f6;
        padding: 2px 8px;
        border-radius: 10px;
        color: #31333f;
    }
    /* Esconde a linha decorativa do Streamlit se houver */
    hr { display: none; }
    </style>
    """, unsafe_allow_html=True)

NOME_ARQUIVO = "meus_artigos.xlsx"

def carregar_dados():
    if not os.path.exists(NOME_ARQUIVO): return None, None
    xl = pd.ExcelFile(NOME_ARQUIVO)
    return xl, xl.sheet_names

xl, abas = carregar_dados()

if xl:
    with st.sidebar:
        st.title("Filtros")
        ano_selecionado = st.selectbox("Escolha o Ano:", abas, index=len(abas)-1)
        
        df = pd.read_excel(NOME_ARQUIVO, sheet_name=ano_selecionado)
        df.columns = df.columns.str.strip()
        
        if "Área Temática" in df.columns:
            df["Área Temática"] = df["Área Temática"].astype(str).str.strip().replace("nan", "Outros")
        
        busca = st.text_input("Buscar termo:", placeholder="Título ou autor...")
        
        if "Área Temática" in df.columns:
            areas = sorted(df["Área Temática"].unique().tolist())
            selecao = st.multiselect("Filtrar Áreas:", areas, default=areas)
            df = df[df["Área Temática"].isin(selecao)]

        if busca:
            mask = df.apply(lambda row: row.astype(str).str.contains(busca, case=False).any(), axis=1)
            df = df[mask]

   
    st.title("ANAIS DO WORKSHOP SOBRE ASPECTOS SOCIAIS, HUMANOS E ECONÔMICOS DE SOFTWARE (Washes)")
    st.header(f"Artigos de {ano_selecionado}")
    st.caption(f"{len(df)} resultados encontrados")

    if df.empty:
        st.info("Nenhum resultado encontrado.")
    else:
        for _, row in df.iterrows():
            with st.container():
                st.markdown('<div class="artigo-container">', unsafe_allow_html=True)
                
                
                st.markdown(f'<div class="titulo-texto">{row["Título"]}</div>', unsafe_allow_html=True)
                
                
                autores = row.get('Nome dos Autores', row.get('Autor', 'N/A'))
                inst = row.get('Instituição', 'N/A')
                st.markdown(f'<div class="meta-dados"><i>{autores}</i> • {inst}</div>', unsafe_allow_html=True)
                
                
                st.markdown(f'<span class="tag-area">{row["Área Temática"]}</span>', unsafe_allow_html=True)
                
                
                with st.expander("Ver detalhes"):
                    st.write("**Resumo:**")
                    st.write(row.get('Resumo', 'Resumo indisponível.'))
                    
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Arquivo não encontrado.")