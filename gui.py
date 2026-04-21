import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import subprocess
import threading
import sys
import winreg

def get_env_var_windows(name):
    """Tenta ler a variável direto do registro do Windows, caso não esteja no os.environ"""
    val = os.environ.get(name, "")
    if val:
        return val
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
            val, _ = winreg.QueryValueEx(key, name)
            if val:
                os.environ[name] = val # Guarda na sessão atual também
                return val
    except Exception:
        pass
    return ""

def get_env_var_name(provider):
    if provider == "ChatGPT (OpenAI)":
        return "OPENAI_API_KEY"
    elif provider == "Gemini (Google)":
        return "GEMINI_API_KEY"
    elif provider == "Claude (Anthropic)":
        return "ANTHROPIC_API_KEY"
    return "OPENAI_API_KEY"

def get_provider_id(provider_str):
    if provider_str == "ChatGPT (OpenAI)":
        return "openai"
    elif provider_str == "Gemini (Google)":
        return "gemini"
    elif provider_str == "Claude (Anthropic)":
        return "anthropic"
    return "openai"

def on_ai_change(event):
    provider = combo_ai.get()
    env_var = get_env_var_name(provider)
    
    # Atualiza modelos disponíveis
    if provider == "ChatGPT (OpenAI)":
        modelos = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]
        combo_model.config(values=modelos, state="readonly")
        combo_model.set(modelos[0])
        label_token.config(text="Sua Chave OpenAI (sk-...):")
    elif provider == "Gemini (Google)":
        modelos = ["gemini/gemini-2.5-pro", "gemini/gemini-3.1-pro-preview", "gemini/gemini-1.5-pro-latest", "gemini/gemini-1.5-flash-latest"]
        combo_model.config(values=modelos, state="readonly")
        combo_model.set(modelos[0])
        label_token.config(text="Sua Chave Gemini:")
    elif provider == "Claude (Anthropic)":
        modelos = ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-opus-20240229", "anthropic/claude-3-haiku-20240307"]
        combo_model.config(values=modelos, state="readonly")
        combo_model.set(modelos[0])
        label_token.config(text="Sua Chave Claude (sk-ant-...):")
        
    # Limpa e tenta preencher com o token existente
    entry_token.delete(0, tk.END)
    token_existente = get_env_var_windows(env_var)
    if token_existente:
        entry_token.insert(0, token_existente)

def salvar_token():
    token = entry_token.get().strip()
    provider = combo_ai.get()
    env_var = get_env_var_name(provider)
    
    if not token:
        messagebox.showwarning("Aviso", "Por favor, insira um token válido.")
        return
    
    try:
        # Salva permanentemente no Windows usando o comando 'setx'
        subprocess.run(f'setx {env_var} "{token}"', shell=True, check=True, stdout=subprocess.DEVNULL)
        # Define no ambiente da execução atual também
        os.environ[env_var] = token
        messagebox.showinfo("Sucesso", f"Token salvo com sucesso no sistema Windows!\nEle ficará salvo para os próximos usos ({env_var}).")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar token: {e}")

def selecionar_arquivo():
    filepath = filedialog.askopenfilename(
        title="Selecione o arquivo Markdown da Monografia",
        filetypes=(("Arquivos Markdown", "*.md"), ("Todos os arquivos", "*.*"))
    )
    if filepath:
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, filepath)

def executar_sava():
    arquivo = entry_arquivo.get().strip()
    if not arquivo:
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo para análise.")
        return
        
    provider_str = combo_ai.get()
    env_var = get_env_var_name(provider_str)
    provider_id = get_provider_id(provider_str)
    
    token = os.environ.get(env_var) or entry_token.get().strip()
    if not token:
        messagebox.showwarning("Aviso", f"O Token ({env_var}) não foi definido. Insira e clique em 'Salvar no Windows'.")
        return

    os.environ[env_var] = token

    # Prepara a interface para a execução
    btn_executar.config(state=tk.DISABLED)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Iniciando a Inteligência Artificial ({provider_str})... Por favor, aguarde. Isso pode demorar alguns minutos.\n\n")
    
    # Roda em uma thread separada para não travar (congelar) a janela principal
    modelo_selecionado = combo_model.get()
    threading.Thread(target=rodar_script, args=(arquivo, provider_id, modelo_selecionado), daemon=True).start()

def rodar_script(arquivo, provider_id, modelo_selecionado):
    try:
        # Importa a função do seu arquivo main.py
        from main import create_sava_crew
        crew = create_sava_crew(provider=provider_id, model=modelo_selecionado)
        
        inputs = {'monografia_path': arquivo}
        resultado = crew.kickoff(inputs=inputs)
        
        # Atualiza a interface com o resultado
        janela.after(0, lambda: text_output.insert(tk.END, "######################\nRESULTADO DA AVALIAÇÃO\n######################\n\n"))
        janela.after(0, lambda: text_output.insert(tk.END, str(resultado) + "\n"))
        janela.after(0, lambda: messagebox.showinfo("Concluído", "Análise concluída com sucesso!"))
    except Exception as e:
        erro_msg = str(e)
        janela.after(0, lambda msg=erro_msg: text_output.insert(tk.END, f"\nErro durante a execução: {msg}\n"))
        janela.after(0, lambda msg=erro_msg: messagebox.showerror("Erro", f"Ocorreu um erro: {msg}"))
    finally:
        # Reativa o botão
        janela.after(0, lambda: btn_executar.config(state=tk.NORMAL))

# ==========================================
# Configuração da Janela Principal (GUI)
# ==========================================
janela = tk.Tk()
janela.title("SAVA - Sistema Multi-Agente de Validação Acadêmica")
janela.geometry("800x650")
janela.configure(padx=10, pady=10)

# Frame 1: Seleção da IA
frame_ai = tk.LabelFrame(janela, text="1. Seleção da Inteligência Artificial", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_ai.pack(fill="x", pady=5)

tk.Label(frame_ai, text="Escolha a IA:").pack(side="left")
opcoes_ai = ["ChatGPT (OpenAI)", "Gemini (Google)", "Claude (Anthropic)"]
combo_ai = ttk.Combobox(frame_ai, values=opcoes_ai, state="readonly", width=30)
combo_ai.pack(side="left", padx=10)
combo_ai.set(opcoes_ai[0]) # Default: ChatGPT

tk.Label(frame_ai, text="Modelo:").pack(side="left", padx=(10, 2))
combo_model = ttk.Combobox(frame_ai, state="readonly", width=30)
combo_model.pack(side="left", padx=10)
# Inicializa os valores do ChatGPT
combo_model.config(values=["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"])
combo_model.set("gpt-4o")

combo_ai.bind("<<ComboboxSelected>>", on_ai_change)

# Frame 2: Token da IA
frame_token = tk.LabelFrame(janela, text="2. Configuração da API", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_token.pack(fill="x", pady=5)

label_token = tk.Label(frame_token, text="Sua Chave OpenAI (sk-...):")
label_token.pack(side="left")
entry_token = tk.Entry(frame_token, width=50, show="*")
entry_token.pack(side="left", padx=10)

btn_salvar_token = tk.Button(frame_token, text="Salvar no Windows", command=salvar_token, bg="#2196F3", fg="white", font=("Arial", 9, "bold"))
btn_salvar_token.pack(side="left", padx=5)

# Tenta carregar o token do ChatGPT (default) se já existir no Windows
token_existente = get_env_var_windows("OPENAI_API_KEY")
if token_existente:
    entry_token.insert(0, token_existente)

# Frame 3: Seleção do Arquivo
frame_arquivo = tk.LabelFrame(janela, text="3. Seleção de Documento", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_arquivo.pack(fill="x", pady=5)

tk.Label(frame_arquivo, text="Caminho do Arquivo:").pack(side="left")
entry_arquivo = tk.Entry(frame_arquivo, width=50)
entry_arquivo.pack(side="left", padx=10)

# Insere o arquivo padrão de teste
entry_arquivo.insert(0, "Inicial.md")

btn_procurar = tk.Button(frame_arquivo, text="Procurar Arquivo...", command=selecionar_arquivo)
btn_procurar.pack(side="left", padx=5)

# Botão Principal de Execução
btn_executar = tk.Button(janela, text="EXECUTAR ANÁLISE COMPLETA", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=executar_sava, pady=10)
btn_executar.pack(fill="x", pady=15)

# Frame 4: Resultados (Output)
frame_output = tk.LabelFrame(janela, text="4. Resultados da Validação", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_output.pack(fill="both", expand=True, pady=5)

text_output = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, font=("Consolas", 10))
text_output.pack(fill="both", expand=True)
text_output.insert(tk.END, "Aguardando inicialização...\n")

# Inicia o loop da interface gráfica
janela.mainloop()