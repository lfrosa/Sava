# SAVA - Sistema Multi-Agente de Validação Acadêmica

O **SAVA** é um sistema baseado em Inteligência Artificial que utiliza um grupo de agentes autônomos para revisar, auditar e validar monografias, dissertações e teses. Ele verifica desde normas da ABNT até o rigor metodológico e a consistência dos dados do trabalho.

Este documento contém o passo a passo completo para executar o projeto em um computador "zerado", que não possui nenhuma ferramenta de desenvolvimento instalada.

---

## 🛠️ 1. Pré-requisitos (O que você precisa instalar)

### Passo 1: Instalar o Python (Versão 3.10 a 3.12)
O sistema foi construído utilizando Python e o framework CrewAI. O CrewAI requer especificamente uma versão do Python entre a `3.10` e a `3.12`.

1. Acesse o site oficial do Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe a versão **Python 3.12** (ou 3.11).
3. **MUITO IMPORTANTE:** Durante a instalação no Windows, na primeira tela, marque a caixa que diz **"Add Python to PATH"** (ou "Adicionar Python ao PATH"). Se esquecer disso, o computador não reconhecerá os comandos.
4. Siga clicando em "Next" até concluir a instalação.

### Passo 2: Obter uma Chave de API de Inteligência Artificial
Os agentes "pensam" usando modelos de linguagem avançados. O sistema agora suporta três opções de IA. Você precisa de uma chave de acesso para pelo menos uma delas:
- **ChatGPT (OpenAI)**: Crie uma conta em [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) e gere uma "secret key" (`sk-...`).
- **Gemini (Google)**: Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey), faça login com sua conta Google e crie uma API Key.
- **Claude (Anthropic)**: Crie uma conta no [Anthropic Console](https://console.anthropic.com/settings/keys) e gere uma API Key (`sk-ant-...`).
- **Ollama (Local)**: Tenha o Ollama rodando localmente (ex: `ollama run gemma4`). Não requer chave, apenas preencha com a URL (geralmente `http://localhost:11434`).

*Guarde a sua chave em um local seguro após a criação.*

---

## 🚀 2. Configurando o Projeto

### Passo 1: Baixar os arquivos
Se você ainda não tem os arquivos do projeto na nova máquina:
1. Crie uma pasta no seu computador (por exemplo: `C:\TeseValidator`).
2. Coloque dentro dela os arquivos essenciais deste projeto:
   - `main.py` (o código principal dos agentes)
   - `gui.py` (a interface visual do sistema)
   - `requirements.txt` (a lista de bibliotecas, agora com suporte a múltiplos provedores)
   - `Inicial.md` (ou outro arquivo de texto Markdown com a sua monografia)

### Passo 2: Abrir o Terminal
No Windows:
1. Abra a pasta onde você salvou os arquivos (ex: `C:\TeseValidator`).
2. Clique na barra de endereços da pasta no topo da janela, digite `cmd` e aperte **Enter**. Isso abrirá uma tela preta (Terminal) já na pasta correta.

### Passo 3: Criar um Ambiente Virtual (Recomendado)
O ambiente virtual isola este projeto para não interferir em outros programas do seu computador.
No terminal aberto, digite:
```bash
python -m venv .venv
```
*(Isso criará uma pasta oculta chamada `.venv`. Pode demorar alguns segundos).*

### Passo 4: Ativar o Ambiente Virtual
Para usar o ambiente que você acabou de criar, digite:
**No Windows:**
```bash
.venv\Scripts\activate
```
*(Você verá que o terminal agora mostra `(.venv)` no início da linha, indicando que está ativado).*

**No Mac/Linux:**
```bash
source .venv/bin/activate
```

### Passo 5: Instalar as Bibliotecas
Com o ambiente ativado, instale o CrewAI e as dependências necessárias executando:
```bash
pip install -r requirements.txt
```
*(Isso vai baixar a inteligência do sistema, incluindo os pacotes extras para Google GenAI e Anthropic. Pode demorar alguns minutos dependendo da sua internet).*

---

## 🧠 3. Executando o Programa (Interface Gráfica)

### Passo 1: Iniciar a Interface
Agora que tudo está instalado, para abrir a tela do programa, basta digitar:
```bash
python gui.py
```
*(Uma nova janela do SAVA se abrirá na sua tela).*

### Passo 2: Escolher a IA e Configurar o Token
Com a janela do SAVA aberta:
1. Na seção **"1. Seleção da Inteligência Artificial"**, escolha qual IA você deseja utilizar (ChatGPT, Gemini, Claude ou Ollama).
2. Na seção **"2. Configuração da API"**, cole a sua chave secreta correspondente (ou a URL `http://localhost:11434` no caso do Ollama).
3. Clique no botão azul **"Salvar no Windows"**.
*(Nota: O sistema salva sua chave no Registro do Windows. Você só precisará fazer isso na primeira vez para cada provedor que utilizar!)*

### Passo 3: Iniciar a Análise
1. Na seção **"3. Seleção de Documento"**, clique no botão **"Procurar Arquivo..."**.
2. Selecione o seu arquivo de texto da monografia (em formato Markdown `.md`). Se quiser apenas testar, deixe o arquivo padrão que já vem preenchido (`Inicial.md`).
3. Clique no botão verde gigante **"EXECUTAR ANÁLISE COMPLETA"**.

Aguarde enquanto os agentes leem, analisam e discutem o documento. Todo o processo será exibido na área preta de "Resultados da Validação". Ao final, a inteligência artificial imprimirá o **Parecer de Qualificação Final** detalhado!

---
**Dica para os próximos dias:** Sempre que fechar e for usar o sistema novamente, basta abrir o terminal na pasta do projeto, ativar o ambiente (Passo 2.4) e rodar o `python gui.py`. A interface já carregará automaticamente as chaves salvas conforme você troca a IA no menu!