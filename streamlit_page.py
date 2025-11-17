#--------------------------------------------------------------#
# BIBLIOTECAS
#--------------------------------------------------------------#

import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime

#--------------------------------------------------------------#
# SIDEBAR STREAMLIT
#--------------------------------------------------------------#

# Config da página
st.set_page_config(page_title = "Filtro METADADOS", page_icon =  "⚓", layout = "centered")

# Sidebar

st.sidebar.markdown("# Survey Info")
st.sidebar.markdown("### ")
imagem = Image.open("lh2_foto.jpg")
st.sidebar.image(imagem, width=250)
st.sidebar.markdown("""---""")

# Sidebar (with CSS)
st.sidebar.markdown("""
<style>
    .sidebar-text {
        text-align: center;
        font-size: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-text">Powered by Pedro Garcia.</p>', unsafe_allow_html=True)

#----------------------------------------------#
### PÁGINA STREAMLIT ###
#----------------------------------------------#

with st.container():
        st.title("METADADOS ROV - OCEANICASUB X 🚢")

        st.write("")
        st.markdown("### 1. Selecione o arquivo LOG:")

        # Widget para upload de arquivo
        uploaded_file = st.file_uploader("", type=[".npc"], help="Insirir ou arrastar o arquivo LOG_Metadados_BR " \
        "com extensão .NPD gerado pelo Navipac.")
        
        # Verifica se deu certo o upload de dado e 
        if uploaded_file is not None:
            st.success("Arquivo enviado com sucesso!")
            

st.markdown("---")
st.markdown("### 2. Informar intervalo da operação:")

col1, col2 = st.columns(2)
with col1:
        data_inicio = st.date_input("Data de início:", format="DD/MM/YYYY")
        hora_inicio = st.time_input("Hora de início:", value="now", step=60)
        datetime_inicio = datetime.combine(data_inicio, hora_inicio)

with col2:
        data_final = st.date_input("Data de final:", format="DD/MM/YYYY")
        hora_final = st.time_input("Hora de final:", value="now", step=60)
        datetime_final = datetime.combine(data_final, hora_final)

with st.container():
        
        st.markdown("---")
        st.markdown("### 3. Extrair Metadados:")
        linhas_filtradas = None
        
        if st.button("Extrair"):
                if not uploaded_file:
                        st.error("Informe um arquivo .NPD válido.")
                else:
                        linhas_filtradas = []

                        # Decodifica o arquivo
                        conteudo = uploaded_file.read().decode("utf-8", errors="ignore")

                        for linha in conteudo.splitlines():
                                coluna = linha.strip().split(",")
                                try:
                                        coluna_data = coluna[1]
                                        coluna_hora = coluna[2]
                                        datahora_linha = datetime.strptime(f"{coluna_data} {coluna_hora}", "%d.%m.%Y %H.%M.%S")
                                        
                                        if datetime_inicio <= datahora_linha <= datetime_final:
                                                linhas_filtradas.append(linha.strip())

                                except Exception:
                                        continue

                        if len(linhas_filtradas) == 0:
                                st.warning("Nenhuma linha encontrada dentro do intervalo informado.")

                        else:
                                st.success(f"Foram encontradas {len(linhas_filtradas)} linhas dentro do intervalo.")


with st.container():
        st.markdown("---")
        st.markdown("### 4. Baixar Metadados:")
        if linhas_filtradas is not None:
                st.download_button("Baixar", linhas_filtradas)
        else:
                st.error("Nenhum arquivo .NPC foi localizado.")
        

