import streamlit as st
import os
import tempfile
from main import create_sava_crew

# Configuração da página Web
st.set_page_config(page_title="SAVA - Validador Acadêmico", page_icon="🎓", layout="centered")

st.title("🎓 SAVA")
st.subheader("Sistema Multi-Agente de Validação Acadêmica")
st.markdown("Valide monografias, dissertações e teses com Inteligência Artificial.")

# ==========================================
# Barra Lateral (Configurações)
# ==========================================
with st.sidebar:
    st.header("⚙️ Configurações da IA")
    
    provedor_selecionado = st.selectbox(
        "Escolha o Provedor:",
        ["ChatGPT (OpenAI)", "Gemini (Google)", "Claude (Anthropic)", "Ollama (Local)"]
    )
    
    # Mapeia a seleção para o ID interno e variáveis
    if provedor_selecionado == "ChatGPT (OpenAI)":
        provider_id = "openai"
        env_var = "OPENAI_API_KEY"
        modelos = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]
    elif provedor_selecionado == "Gemini (Google)":
        provider_id = "gemini"
        env_var = "GEMINI_API_KEY"
        modelos = ["gemini/gemini-2.5-pro", "gemini/gemini-1.5-pro-latest"]
    elif provedor_selecionado == "Claude (Anthropic)":
        provider_id = "anthropic"
        env_var = "ANTHROPIC_API_KEY"
        modelos = ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-opus-20240229"]
    else:
        provider_id = "ollama"
        env_var = "OLLAMA_API_BASE"
        modelos = ["gemma4", "llama3", "mistral"]

    modelo_selecionado = st.selectbox("Escolha o Modelo:", modelos)
    
    # Campo de Token ou URL
    if provider_id == "ollama":
        token = st.text_input("URL do Ollama:", value="http://localhost:11434")
    else:
        token = st.text_input(f"Token ({env_var}):", type="password")

# ==========================================
# Área Principal (Upload e Execução)
# ==========================================
st.markdown("### 📄 Envio do Documento")
arquivo_upload = st.file_uploader("Arraste seu arquivo Markdown (.md) aqui", type=['md'])

if st.button("🚀 Executar Análise Completa", type="primary"):
    if not token:
        st.warning("⚠️ Por favor, preencha o Token / URL na barra lateral.")
    elif not arquivo_upload:
        st.warning("⚠️ Por favor, faça o upload de um arquivo .md.")
    else:
        # Salva o token no ambiente
        os.environ[env_var] = token
        
        # Salva o arquivo temporariamente para o CrewAI poder ler
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_file:
            tmp_file.write(arquivo_upload.getvalue())
            temp_path = tmp_file.name
            
        st.info("A inteligência artificial está lendo e discutindo o seu documento. Isso pode levar alguns minutos...")
        
        # Executa a análise com um "spinner" de carregamento
        with st.spinner('Os agentes estão trabalhando...'):
            try:
                crew = create_sava_crew(provider=provider_id, model=modelo_selecionado)
                resultado = crew.kickoff(inputs={'monografia_path': temp_path})
                
                st.success("✅ Análise Concluída com Sucesso!")
                st.markdown("### Parecer Final")
                st.markdown(resultado) # Exibe o resultado renderizado bonito na tela
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")