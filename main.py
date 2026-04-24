import os
from crewai import Agent, Task, Crew, Process

def create_sava_crew(provider="openai", model=None):
    """
    Cria e configura o Sistema Multi-Agente de Validação Acadêmica (SAVA)
    utilizando o framework CrewAI.
    """
    
    # ==========================================
    # 0. Configuração da Inteligência Artificial
    # ==========================================
    llm = None
    if provider == "openai":
        llm = model if model else "gpt-4o"
    elif provider == "gemini":
        # Remove variáveis de ambiente do Google Cloud que forçam o uso do Vertex AI
        # para garantir que o CrewAI use a API Key do Google AI Studio corretamente
        os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
        os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
        llm = model if model else "gemini/gemini-2.5-pro"
    elif provider == "anthropic":
        llm = model if model else "anthropic/claude-3-5-sonnet-20240620"
    elif provider == "ollama":
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        # A integração nativa do Ollama no CrewAI/LiteLLM usa a URL base sem /v1
        if base_url.endswith("/v1"):
            base_url = base_url[:-3]
        os.environ["OLLAMA_API_BASE"] = base_url
        _model = model if model else "gemma4"
        # O CrewAI espera uma string no formato 'provedor/modelo'
        llm = f"ollama/{_model}"

    # ==========================================
    # 1. Definição dos Agentes (Backstory & Tasks)
    # ==========================================

    agente_normatizador = Agent(
        role='Agente Normatizador',
        goal='Garantir a conformidade da monografia com as normas técnicas (ABNT, APA, Vancouver) e verificar se todas as citações possuem referência bibliográfica correspondente.',
        backstory='The Standard Guardian. Você é um especialista meticuloso em normas técnicas e documentação acadêmica. Sua missão é garantir que a forma e a estrutura do trabalho impecáveis.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_metodologico = Agent(
        role='Agente Metodológico',
        goal='Auditar o rigor científico do trabalho, assegurando que há coerência lógica entre o problema de pesquisa, os objetivos e a metodologia aplicada.',
        backstory='The Logic Master. Você é um Doutor em Metodologia Científica com ampla visão interdisciplinar. Seu papel é garantir que o método científico escolhido realmente responda à pergunta da pesquisa e que as conclusões sejam baseadas em dados.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_analista_dados = Agent(
        role='Agente Analista de Dados',
        goal='Auditar a consistência numérica do documento, validar a interpretação estatística, tabelas, gráficos, modelos e dados apresentados.',
        backstory='The Data Auditor. Especialista sênior em análise quantitativa e qualitativa. Sua paixão é a precisão dos dados, você não deixa passar uma inconsistência entre texto e tabelas.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_integridade = Agent(
        role='Agente de Integridade',
        goal='Detectar possíveis indícios de plágio, uso indevido de IA generativa não assistida, além de avaliar a fluidez do texto e originalidade.',
        backstory='The Ethics Officer. Especialista em linguística forense e ética acadêmica. Sua missão é proteger a integridade institucional e a originalidade da contribuição científica.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_revisor_final = Agent(
        role='Agente Revisor Final',
        goal='Consolidar os inputs e pareceres dos demais agentes, avaliar coesão e clareza e emitir o Parecer de Qualificação definitivo (Aprovado, Aprovado com Ressalvas ou Reprovado).',
        backstory='The Chief Editor. Editor experiente de periódicos científicos de alto impacto. Você tem a palavra final sobre a aceitação do documento, organizando as demandas de melhoria de forma clara para o autor.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_resumidor = Agent(
        role='Agente Resumidor',
        goal='Criar um resumo executivo claro, destacando os pontos principais, a metodologia aplicada e as conclusões do documento.',
        backstory='Especialista em síntese de textos acadêmicos. Você possui a habilidade de ler trabalhos longos e extrair sua essência rapidamente, facilitando a compreensão de seus pontos-chave.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    agente_alteracoes = Agent(
        role='Agente de Melhorias e Alterações',
        goal='Demonstrar possíveis alterações práticas no texto, sugerindo reescritas para trechos confusos, redundantes ou com falhas de estilo.',
        backstory='Revisor textual focado em aprimoramento de estilo e clareza. Você não apenas aponta o que está ruim, mas reescreve os trechos mostrando na prática o "antes e depois" para guiar o autor.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


    # ==========================================
    # 2. Definição das Tarefas (Workflow)
    # ==========================================

    # Fase Paralela (Análise estrutural, dados e integridade)
    tarefa_normatizacao = Task(
        description='Comparar a estrutura do documento {monografia_path} com os templates da instituição e validar o pareamento exato entre citações no texto e referências bibliográficas.',
        expected_output='Um "Relatório de Inconformidades Estruturais" listando erros de formatação e citações órfãs.',
        agent=agente_normatizador,
        async_execution=False # Desativado para evitar limite de requisições (Error 429)
    )

    tarefa_analise_dados = Task(
        description='Auditar tabelas, gráficos e estatísticas no documento {monografia_path}. Checar se a interpretação de fórmulas e modelos está correta e se os números citados no texto refletem os das tabelas.',
        expected_output='Uma "Nota de Auditoria de Dados", listando as divergências numéricas encontradas (se houver).',
        agent=agente_analista_dados,
        async_execution=False # Desativado para evitar limite de requisições (Error 429)
    )

    tarefa_integridade = Task(
        description='Varrer o documento completo {monografia_path} buscando por quebras de padrão de escrita, fluidez artificial (indício de IA) ou trechos não originais (plágio).',
        expected_output='Um "Score de Originalidade" acompanhado de alertas de risco.',
        agent=agente_integridade,
        async_execution=False # Desativado para evitar limite de requisições (Error 429)
    )

    # Fase Sequencial (Auditoria Metodológica e Revisão Final)
    tarefa_metodologica = Task(
        description='Com base no documento {monografia_path} e nas saídas do Agente Analista de Dados, analisar se o método responde à pergunta e se as conclusões estão fundamentadas estritamente nos dados apresentados.',
        expected_output='Um "Parecer Técnico sobre o Rigor Científico".',
        agent=agente_metodologico,
        # Como precisa dos dados, roda após as tarefas assíncronas
    )

    tarefa_resumo = Task(
        description='Ler o documento {monografia_path} e gerar um resumo detalhado contendo o problema de pesquisa, metodologia, resultados principais e conclusão.',
        expected_output='Um resumo executivo bem estruturado do trabalho acadêmico.',
        agent=agente_resumidor
    )

    tarefa_alteracoes = Task(
        description='Com base no documento {monografia_path} e nas análises anteriores, selecione trechos que precisam de melhoria e reescreva-os. Demonstre o trecho original e a nova sugestão de reescrita.',
        expected_output='Um documento contendo exemplos práticos de reescrita e sugestões detalhadas de melhoria de estilo.',
        agent=agente_alteracoes,
        output_file='alteracoes_sugeridas.md'
    )

    tarefa_revisao_final = Task(
        description='Reunir o Relatório de Inconformidades, Nota de Auditoria, Score de Originalidade, Parecer Técnico e o Resumo elaborado. Organizar uma To-Do list crítica e emitir o status final: "Aprovado", "Aprovado com Ressalvas" ou "Reprovado". Avaliar também a clareza e elegância do texto.',
        expected_output='O "Parecer de Qualificação Final" consolidado, com o status e a To-Do list para o autor.',
        agent=agente_revisor_final,
        output_file='parecer_final.md'
    )

    # ==========================================
    # 3. Formação da Crew e Orquestração
    # ==========================================
    
    sava_crew = Crew(
        agents=[
            agente_normatizador, 
            agente_analista_dados, 
            agente_integridade, 
            agente_metodologico, 
            agente_resumidor,
            agente_alteracoes,
            agente_revisor_final
        ],
        tasks=[
            tarefa_normatizacao, 
            tarefa_analise_dados, 
            tarefa_integridade, 
            tarefa_metodologica, 
            tarefa_resumo,
            tarefa_alteracoes,
            tarefa_revisao_final
        ],
        process=Process.sequential,
        verbose=True
    )

    return sava_crew

if __name__ == "__main__":
    print("Iniciando o Sistema Multi-Agente de Validação Acadêmica (SAVA)...")
    
    # Solicita o caminho para um arquivo Markdown (.md) local ao usuário
    caminho_arquivo = input("Insira o caminho para o arquivo Markdown (.md) da monografia (ou pressione Enter para usar o Inicial.md de teste): ").strip()
    
    if not caminho_arquivo:
        caminho_arquivo = 'Inicial.md'
        print("Nenhum caminho fornecido. Usando o arquivo de teste local (Inicial.md).")
    elif not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        exit(1)
    else:
        print(f"Documento '{caminho_arquivo}' selecionado com sucesso!")

    crew = create_sava_crew()
    
    inputs = {'monografia_path': caminho_arquivo}
    
    print("\nIniciando a análise (isso pode demorar um pouco)...")
    resultado_final = crew.kickoff(inputs=inputs)
    
    print("\n######################")
    print("RESULTADO DA AVALIAÇÃO")
    print("######################\n")
    print(resultado_final)
    print("\nAgentes construídos e executados com sucesso.")