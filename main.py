from crewai import Agent, Task, Crew, Process

def create_sava_crew():
    """
    Cria e configura o Sistema Multi-Agente de Validação Acadêmica (SAVA)
    utilizando o framework CrewAI, conforme as especificações do documento Inicial.md.
    """

    # ==========================================
    # 1. Definição dos Agentes (Backstory & Tasks)
    # ==========================================

    agente_normatizador = Agent(
        role='Agente Normatizador',
        goal='Garantir a conformidade da monografia com as normas técnicas (ABNT, APA, Vancouver) e verificar se todas as citações possuem referência bibliográfica correspondente.',
        backstory='The Standard Guardian. Você é um especialista meticuloso em normas técnicas e documentação acadêmica. Sua missão é garantir que a forma e a estrutura do trabalho impecáveis.',
        verbose=True,
        allow_delegation=False
    )

    agente_metodologico = Agent(
        role='Agente Metodológico',
        goal='Auditar o rigor científico do trabalho, assegurando que há coerência lógica entre o problema de pesquisa, os objetivos e a metodologia aplicada.',
        backstory='The Logic Master. Você é um Doutor em Metodologia Científica com ampla visão interdisciplinar. Seu papel é garantir que o método científico escolhido realmente responda à pergunta da pesquisa e que as conclusões sejam baseadas em dados.',
        verbose=True,
        allow_delegation=False
    )

    agente_analista_dados = Agent(
        role='Agente Analista de Dados',
        goal='Auditar a consistência numérica do documento, validar a interpretação estatística, tabelas, gráficos, modelos e dados apresentados.',
        backstory='The Data Auditor. Especialista sênior em análise quantitativa e qualitativa. Sua paixão é a precisão dos dados, você não deixa passar uma inconsistência entre texto e tabelas.',
        verbose=True,
        allow_delegation=False
    )

    agente_integridade = Agent(
        role='Agente de Integridade',
        goal='Detectar possíveis indícios de plágio, uso indevido de IA generativa não assistida, além de avaliar a fluidez do texto e originalidade.',
        backstory='The Ethics Officer. Especialista em linguística forense e ética acadêmica. Sua missão é proteger a integridade institucional e a originalidade da contribuição científica.',
        verbose=True,
        allow_delegation=False
    )

    agente_revisor_final = Agent(
        role='Agente Revisor Final',
        goal='Consolidar os inputs e pareceres dos demais agentes, avaliar coesão e clareza e emitir o Parecer de Qualificação definitivo (Aprovado, Aprovado com Ressalvas ou Reprovado).',
        backstory='The Chief Editor. Editor experiente de periódicos científicos de alto impacto. Você tem a palavra final sobre a aceitação do documento, organizando as demandas de melhoria de forma clara para o autor.',
        verbose=True,
        allow_delegation=False
    )


    # ==========================================
    # 2. Definição das Tarefas (Workflow)
    # ==========================================

    # Fase Paralela (Análise estrutural, dados e integridade)
    tarefa_normatizacao = Task(
        description='Comparar a estrutura do documento {monografia_path} com os templates da instituição e validar o pareamento exato entre citações no texto e referências bibliográficas.',
        expected_output='Um "Relatório de Inconformidades Estruturais" listando erros de formatação e citações órfãs.',
        agent=agente_normatizador,
        async_execution=True # Executa paralelamente
    )

    tarefa_analise_dados = Task(
        description='Auditar tabelas, gráficos e estatísticas no documento {monografia_path}. Checar se a interpretação de fórmulas e modelos está correta e se os números citados no texto refletem os das tabelas.',
        expected_output='Uma "Nota de Auditoria de Dados", listando as divergências numéricas encontradas (se houver).',
        agent=agente_analista_dados,
        async_execution=True # Executa paralelamente
    )

    tarefa_integridade = Task(
        description='Varrer o documento completo {monografia_path} buscando por quebras de padrão de escrita, fluidez artificial (indício de IA) ou trechos não originais (plágio).',
        expected_output='Um "Score de Originalidade" acompanhado de alertas de risco.',
        agent=agente_integridade,
        async_execution=True # Executa paralelamente
    )

    # Fase Sequencial (Auditoria Metodológica e Revisão Final)
    tarefa_metodologica = Task(
        description='Com base no documento {monografia_path} e nas saídas do Agente Analista de Dados, analisar se o método responde à pergunta e se as conclusões estão fundamentadas estritamente nos dados apresentados.',
        expected_output='Um "Parecer Técnico sobre o Rigor Científico".',
        agent=agente_metodologico,
        # Como precisa dos dados, roda após as tarefas assíncronas
    )

    tarefa_revisao_final = Task(
        description='Reunir o Relatório de Inconformidades (Normatizador), Nota de Auditoria (Analista de Dados), Score de Originalidade (Integridade) e Parecer Técnico (Metodológico). Organizar uma To-Do list crítica e emitir o status final: "Aprovado", "Aprovado com Ressalvas" ou "Reprovado". Avaliar também a clareza e elegância do texto.',
        expected_output='O "Parecer de Qualificação Final" consolidado, com o status e a To-Do list para o autor.',
        agent=agente_revisor_final
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
            agente_revisor_final
        ],
        tasks=[
            tarefa_normatizacao, 
            tarefa_analise_dados, 
            tarefa_integridade, 
            tarefa_metodologica, 
            tarefa_revisao_final
        ],
        process=Process.sequential,
        verbose=True
    )

    return sava_crew

if __name__ == "__main__":
    print("Iniciando o Sistema Multi-Agente de Validação Acadêmica (SAVA)...")
    crew = create_sava_crew()
    
    # Exemplo de Ingestão de documento
    # inputs = {'monografia_path': 'arquivos/tese_joao_v1.pdf'}
    # resultado_final = crew.kickoff(inputs=inputs)
    # print("######################")
    # print("RESULTADO DA AVALIAÇÃO")
    # print("######################")
    # print(resultado_final)
    print("Agentes construídos com sucesso e prontos para operação.")