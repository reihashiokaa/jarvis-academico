#region explicação do arquivo

# ============================================================
# Arquivo: tools.py
# ------------------------------------------------------------
# Este arquivo será responsável por organizar as ferramentas
# disponíveis no JARVIS Acadêmico.
#
# No trabalho, tool calling é obrigatório.
#
# Tool calling significa que a LLM não vai apenas responder texto.
# Ela também poderá escolher chamar funções do sistema, como:
#
# - consultar agenda;
# - listar tarefas;
# - adicionar tarefa;
# - concluir tarefa;
# - consultar materiais pelo RAG.
#
# Este arquivo funcionará como uma ponte entre:
#
# 1. a decisão da LLM;
# 2. as funções reais do sistema;
# 3. o registro de logs.
#
# Exemplo:
#
# Se a LLM decidir chamar a ferramenta "consultar_tarefas",
# este arquivo deverá:
#
# 1. chamar a função consultar_tarefas() do arquivo tarefas.py;
# 2. receber a resposta dessa função;
# 3. registrar no log qual ferramenta foi chamada, qual entrada
#    recebeu e qual saída devolveu;
# 4. devolver a resposta para o restante do sistema.
#
# A lógica geral usada neste arquivo será:
#
# carregar_...
#   -> carrega definições ou estruturas gerais.
#
# recuperar_...
#   -> recupera informações específicas em formato bruto.
#
# executar_...
#   -> executa uma ferramenta escolhida.
#
# registrar_...
#   -> registra informações importantes, geralmente em logs.
#
# As funções deste arquivo serão importantes para o futuro fluxo
# de tool calling.
#
# Algumas funções serão intermediárias.
#
# Isso significa que elas ajudam o sistema por dentro, mas não
# são a ação final chamada pelo usuário.
#
# Outras funções poderão ser tratadas como parte central do fluxo
# de ferramentas.
# ============================================================

#endregion

#region importações

# ------------------------------------------------------------
# Importamos as funções de agenda que já criamos.
#
# Essas funções são funções finais do arquivo agenda.py, porque
# elas já devolvem respostas prontas para o usuário.
#
# Elas serão disponibilizadas como ferramentas para a LLM.
# ------------------------------------------------------------
from src.agenda import (
    consultar_agenda_por_data,
    consultar_agenda_hoje,
    consultar_agenda_amanha,
    consultar_agenda_semana_atual
)


# ------------------------------------------------------------
# Importamos as funções de tarefas que já criamos.
#
# Essas funções representam as ações principais da lista de tarefas:
#
# - consultar tarefas;
# - adicionar tarefa;
# - concluir tarefa.
#
# Elas também serão disponibilizadas como ferramentas para a LLM.
# ------------------------------------------------------------
from src.tarefas import (
    concluir_tarefa_por_descricao,
    consultar_tarefas,
    adicionar_tarefa
)


# ------------------------------------------------------------
# Importamos a função responsável por registrar logs de ferramentas.
#
# Sempre que uma ferramenta for executada, vamos registrar:
#
# - nome da ferramenta;
# - entrada recebida;
# - saída devolvida.
#
# Isso atende ao requisito do trabalho sobre logs de tool calling.
# ------------------------------------------------------------
from src.logger import registrar_chamada_ferramenta


# ------------------------------------------------------------
# Importamos a função responsável por executar o processo
# completo da consulta de materiais.
#
# Ela recebe uma pergunta e então executa todo o processo de
# recuperação dos materiais e formatação da pergunta/respostas.
# ------------------------------------------------------------
from src.rag import consultar_material_rag


from src.aprendizado import (
    gerar_exercicios,
    iniciar_active_recall,
    responder_active_recall
)

#endregion

#region carregar_ferramentas_disponiveis (intermediária, retorna dicionário com nomes e funções disponíveis)

# ------------------------------------------------------------
# Função: carregar_ferramentas_disponiveis
# ------------------------------------------------------------
# Esta função monta e devolve um dicionário com as ferramentas
# disponíveis no JARVIS.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque, no tool calling, a LLM vai escolher uma ferramenta pelo
# nome.
#
# Exemplo:
#
# "consultar_tarefas"
#
# Só que o Python precisa transformar esse nome em texto na função
# real que deve ser executada.
#
# Então criamos um dicionário assim:
#
# {
#     "consultar_tarefas": consultar_tarefas,
#     "adicionar_tarefa": adicionar_tarefa,
#     "concluir_tarefa_por_descricao": concluir_tarefa_por_descricao
# }
#
# A parte da esquerda é o nome da ferramenta em texto.
#
# A parte da direita é a função Python real.
#
# Assim, se o sistema receber o nome "consultar_tarefas",
# ele consegue encontrar e executar a função consultar_tarefas().
#
# Por enquanto, vamos cadastrar as ferramentas que já existem:
#
# Agenda:
# - consultar_agenda_por_data
# - consultar_agenda_hoje
# - consultar_agenda_amanha
# - consultar_agenda_semana_atual
#
# Tarefas:
# - consultar_tarefas
# - adicionar_tarefa
# - concluir_tarefa_por_descricao
# ------------------------------------------------------------
def carregar_ferramentas_disponiveis() -> dict:
    # --------------------------------------------------------
    # Aqui criamos um dicionário chamado ferramentas.
    #
    # Um dicionário em Python guarda pares de chave e valor.
    #
    # Neste caso:
    #
    # chave:
    #   nome da ferramenta em texto.
    #
    # valor:
    #   função Python que será chamada.
    #
    # Exemplo:
    #
    # "consultar_tarefas": consultar_tarefas
    #
    # Isso significa:
    #
    # quando alguém pedir a ferramenta "consultar_tarefas",
    # o sistema deve executar a função consultar_tarefas().
    # --------------------------------------------------------
    ferramentas = {
        # ----------------------------------------------------
        # Ferramentas relacionadas à agenda acadêmica.
        #
        # Essas funções foram criadas no arquivo agenda.py.
        # Elas já devolvem respostas prontas para o usuário.
        # ----------------------------------------------------
        "consultar_agenda_por_data": consultar_agenda_por_data,
        "consultar_agenda_hoje": consultar_agenda_hoje,
        "consultar_agenda_amanha": consultar_agenda_amanha,
        "consultar_agenda_semana_atual": consultar_agenda_semana_atual,

        # ----------------------------------------------------
        # Ferramentas relacionadas à lista de tarefas.
        #
        # Essas funções foram criadas no arquivo tarefas.py.
        # Elas representam as ações principais exigidas no
        # Trabalho 1:
        #
        # - listar tarefas;
        # - adicionar tarefa;
        # - concluir tarefa por descrição;
        # ----------------------------------------------------
        "consultar_tarefas": consultar_tarefas,
        "adicionar_tarefa": adicionar_tarefa,
        "concluir_tarefa_por_descricao": concluir_tarefa_por_descricao,

        # ----------------------------------------------------
        # Ferramenta relacionada à consulta de materiais de estudo
        # (RAG).
        #
        # Essa função foi criada no arquivo rag.py.
        # Ela representa as ações principais exigidas no
        # Trabalho 1:
        #
        # - carregar documentos;
        # - dividir em chunks;
        # - gerar embeddings;
        # - recuperar trechos relevantes;
        # - gerar respostas baseadas nesses trechos
        # ----------------------------------------------------
        "consultar_material_rag": consultar_material_rag,

        # ----------------------------------------------------
        # Ferramenta relacionada à geração de exercícios baseado
        # nos materiais de estudo.
        #
        # Essa função foi criada no arquivo aprendizado.py.
        # Ela representa as ações principais exigidas no
        # Trabalho 1:
        #
        # - geração de exercícios (Melhorias de Aprendizado)
        # ----------------------------------------------------
        "gerar_exercicios": gerar_exercicios,
        "iniciar_active_recall": iniciar_active_recall,
        "responder_active_recall": responder_active_recall
    }

    # --------------------------------------------------------
    # Por fim, devolvemos o dicionário de ferramentas.
    #
    # Outras partes do sistema poderão usar esse dicionário para
    # descobrir quais ferramentas existem e qual função executar.
    # --------------------------------------------------------
    return ferramentas

#endregion

#region recuperar_ferramenta_por_nome (intermediária, recebe o nome da ferramenta e retorna a função correspondente)

# ------------------------------------------------------------
# Função: recuperar_ferramenta_por_nome
# ------------------------------------------------------------
# Esta função recupera uma ferramenta específica a partir do nome
# dela.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque, no tool calling, a LLM vai indicar qual ferramenta deseja
# chamar usando um nome em texto.
#
# Exemplo:
#
# "consultar_tarefas"
#
# Só que o Python não executa uma função apenas porque recebeu
# uma string com o nome dela.
#
# Então precisamos consultar o dicionário de ferramentas disponíveis
# e descobrir qual função real corresponde àquele nome.
#
# Exemplo:
#
# nome_ferramenta = "consultar_tarefas"
#
# O sistema procura esse nome no dicionário:
#
# {
#     "consultar_tarefas": consultar_tarefas,
#     "adicionar_tarefa": adicionar_tarefa,
#     "concluir_tarefa_por_descricao": concluir_tarefa_por_descricao
# }
#
# E recupera a função Python real:
#
# consultar_tarefas
#
# Se o nome existir, a função correspondente será devolvida.
#
# Se o nome não existir, será devolvido None.
# ------------------------------------------------------------
def recuperar_ferramenta_por_nome(nome_ferramenta: str):
    # --------------------------------------------------------
    # O parâmetro "nome_ferramenta" representa o nome textual da
    # ferramenta que queremos recuperar.
    #
    # Exemplo:
    #
    # "consultar_tarefas"
    #
    # Esse nome virá, no futuro, da decisão feita pela LLM.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, carregamos o dicionário com todas as ferramentas
    # disponíveis no sistema.
    #
    # A função carregar_ferramentas_disponiveis() devolve algo como:
    #
    # {
    #     "consultar_agenda_hoje": consultar_agenda_hoje,
    #     "consultar_tarefas": consultar_tarefas,
    #     "adicionar_tarefa": adicionar_tarefa,
    # }
    # --------------------------------------------------------
    ferramentas = carregar_ferramentas_disponiveis()

    # --------------------------------------------------------
    # Agora tentamos recuperar a ferramenta pelo nome.
    #
    # Usamos ferramentas.get(nome_ferramenta) em vez de:
    #
    # ferramentas[nome_ferramenta]
    #
    # porque .get é mais seguro.
    #
    # Se o nome existir no dicionário, .get devolve a função.
    #
    # Se o nome não existir, .get devolve None.
    #
    # Isso evita que o programa quebre caso a LLM tente chamar uma
    # ferramenta inexistente.
    # --------------------------------------------------------
    ferramenta = ferramentas.get(nome_ferramenta)

    # --------------------------------------------------------
    # Por fim, devolvemos a ferramenta encontrada.
    #
    # Se o nome era válido, será devolvida uma função Python.
    #
    # Se o nome não era válido, será devolvido None.
    # --------------------------------------------------------
    return ferramenta

#endregion

#region executar_ferramenta (intermediária, executa uma ferramenta pelo nome, registra log e retorna a saída)

# ------------------------------------------------------------
# Função: executar_ferramenta
# ------------------------------------------------------------
# Esta função executa uma ferramenta a partir do nome dela.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque, no tool calling, a LLM vai decidir algo como:
#
# ferramenta escolhida:
#   "consultar_tarefas"
#
# entrada:
#   {}
#
# Ou:
#
# ferramenta escolhida:
#   "adicionar_tarefa"
#
# entrada:
#   {
#       "titulo": "Estudar RAG",
#       "descricao": "Revisar chunking e embeddings"
#   }
#
# Só que a LLM escolher a ferramenta não basta.
#
# O nosso código precisa:
#
# 1. receber o nome da ferramenta;
# 2. encontrar a função Python correspondente;
# 3. executar essa função com os dados de entrada;
# 4. receber a saída da função;
# 5. registrar tudo no log;
# 6. devolver a saída para o restante do sistema.
#
# Esta função será uma peça central do fluxo de ferramentas.
# ------------------------------------------------------------
def executar_ferramenta(nome_ferramenta: str, entrada: dict = None):
    # --------------------------------------------------------
    # O parâmetro "nome_ferramenta" representa o nome textual da
    # ferramenta que deve ser executada.
    #
    # Exemplos:
    #
    # "consultar_tarefas"
    # "adicionar_tarefa"
    # "consultar_agenda_hoje"
    #
    # Esse nome será usado para recuperar a função Python real.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "entrada" representa os dados que serão enviados
    # para a ferramenta.
    #
    # Exemplos:
    #
    # Para consultar tarefas:
    #
    # {}
    #
    # Para adicionar tarefa:
    #
    # {
    #     "titulo": "Estudar RAG",
    #     "descricao": "Revisar chunking e embeddings"
    # }
    #
    #
    # Usamos dict porque vamos passar os argumentos em formato de
    # dicionário.
    #
    # O valor padrão é None para permitir chamar a função mesmo
    # sem informar entrada.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Se entrada for None, transformamos em um dicionário vazio.
    #
    # Por quê?
    #
    # Porque algumas ferramentas não precisam de dados de entrada.
    #
    # Exemplo:
    #
    # consultar_tarefas()
    #
    # Essa função não precisa receber nenhum parâmetro.
    #
    # Então podemos representar a entrada dela como:
    #
    # {}
    # --------------------------------------------------------
    if entrada is None:
        entrada = {}

    # --------------------------------------------------------
    # Agora recuperamos a função Python correspondente ao nome da
    # ferramenta.
    #
    # A função recuperar_ferramenta_por_nome(...) devolve:
    #
    # - a função Python, se o nome existir;
    # - None, se o nome não existir.
    # --------------------------------------------------------
    ferramenta = recuperar_ferramenta_por_nome(nome_ferramenta)

    # --------------------------------------------------------
    # Aqui tratamos o caso em que a ferramenta não foi encontrada.
    #
    # Isso pode acontecer se:
    #
    # - a LLM tentar chamar uma ferramenta que não existe;
    # - o nome da ferramenta vier escrito errado;
    # - a ferramenta ainda não tiver sido cadastrada no dicionário.
    #
    # Nesse caso, não podemos executar nada.
    # Então criamos uma mensagem de erro.
    # --------------------------------------------------------
    if ferramenta is None:
        saida = f"Ferramenta não encontrada: {nome_ferramenta}"

        # ----------------------------------------------------
        # Mesmo quando a ferramenta não existe, registramos o caso
        # no log.
        #
        # Isso é útil para análise, porque mostra que houve uma
        # tentativa inválida de chamada.
        # ----------------------------------------------------
        registrar_chamada_ferramenta(
            nome_ferramenta=nome_ferramenta,
            entrada=entrada,
            saida=saida
        )

        # ----------------------------------------------------
        # Depois devolvemos a mensagem de erro para quem chamou
        # esta função.
        # ----------------------------------------------------
        return saida

    # --------------------------------------------------------
    # Se chegamos aqui, significa que a ferramenta existe.
    #
    # Agora vamos tentar executar a função.
    #
    # Usamos try/except porque pode acontecer algum erro durante
    # a execução.
    #
    # Exemplo:
    #
    # A ferramenta adicionar_tarefa espera receber:
    #
    # titulo
    # descricao
    #
    # Se a entrada vier faltando algum dado obrigatório, o Python
    # pode gerar erro.
    #
    # O try/except evita que o programa quebre de forma brusca.
    # --------------------------------------------------------
    try:
        # ----------------------------------------------------
        # Aqui está uma parte muito importante.
        #
        # ferramenta(**entrada)
        #
        # O ** pega um dicionário e transforma suas chaves em
        # argumentos da função.
        #
        # Exemplo:
        #
        # entrada = {
        #     "titulo": "Estudar RAG",
        #     "descricao": "Revisar chunking"
        # }
        #
        # ferramenta(**entrada)
        #
        # vira:
        #
        # adicionar_tarefa(
        #     titulo="Estudar RAG",
        #     descricao="Revisar chunking"
        # )
        #
        # Isso é muito útil para tool calling, porque a LLM poderá
        # devolver os argumentos em formato de dicionário.
        # ----------------------------------------------------
        saida = ferramenta(**entrada)

    except Exception as erro:
        # ----------------------------------------------------
        # Se aconteceu algum erro durante a execução da ferramenta,
        # capturamos esse erro aqui.
        #
        # A variável "erro" guarda a descrição do problema.
        #
        # Em vez de deixar o programa quebrar, devolvemos uma
        # mensagem explicando que houve falha.
        # ----------------------------------------------------
        saida = f"Erro ao executar a ferramenta {nome_ferramenta}: {erro}"

    # --------------------------------------------------------
    # Depois da execução, registramos a chamada no log.
    #
    # Isso acontece tanto quando a ferramenta executa com sucesso
    # quanto quando ela gera erro.
    #
    # Assim, o arquivo logs/tool_calls.jsonl guarda o histórico
    # completo das tentativas de uso de ferramentas.
    # --------------------------------------------------------
    registrar_chamada_ferramenta(
        nome_ferramenta=nome_ferramenta,
        entrada=entrada,
        saida=saida
    )

    # --------------------------------------------------------
    # Por fim, devolvemos a saída da ferramenta.
    #
    # Essa saída pode ser:
    #
    # - uma resposta normal da ferramenta;
    # - uma mensagem de erro;
    # - uma mensagem dizendo que a ferramenta não foi encontrada.
    # --------------------------------------------------------
    return saida

#endregion

#region carregar_descricoes_ferramentas (intermediária, retorna lista com descrições das ferramentas disponíveis)

# ------------------------------------------------------------
# Função: carregar_descricoes_ferramentas
# ------------------------------------------------------------
# Esta função monta uma lista com as descrições das ferramentas
# disponíveis no JARVIS.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque a LLM precisa saber quais ferramentas existem antes de
# decidir qual ferramenta chamar.
#
# A função carregar_ferramentas_disponiveis() cria um dicionário
# que o Python usa para executar ferramentas.
#
# Já esta função cria uma descrição em texto/dados que será usada
# para explicar as ferramentas para a LLM.
#
# Em outras palavras:
#
# carregar_ferramentas_disponiveis()
#   -> ajuda o Python a executar ferramentas.
#
# carregar_descricoes_ferramentas()
#   -> ajuda a LLM a entender quais ferramentas pode escolher.
#
# Cada ferramenta será descrita com:
#
# - nome;
# - descrição;
# - parâmetros esperados.
#
# Isso será útil no futuro prompt de decisão da LLM.
# ------------------------------------------------------------
def carregar_descricoes_ferramentas() -> list:
    # --------------------------------------------------------
    # Aqui criamos uma lista chamada descricoes.
    #
    # Cada item dessa lista será um dicionário representando uma
    # ferramenta disponível.
    #
    # Cada dicionário terá informações úteis para a LLM:
    #
    # - nome da ferramenta;
    # - quando usar essa ferramenta;
    # - quais parâmetros essa ferramenta espera receber.
    # --------------------------------------------------------
    descricoes = [
        # ----------------------------------------------------
        # Ferramenta: consultar_agenda_por_data
        #
        # Essa ferramenta consulta compromissos de uma data
        # específica.
        # ----------------------------------------------------
        {
            "nome": "consultar_agenda_por_data",
            "descricao": "Use quando o usuário quiser consultar compromissos de uma data específica.",
            "parametros": {
                "data_consultada": "Data no formato AAAA-MM-DD. Exemplo: 2026-05-15."
            }
        },

        # ----------------------------------------------------
        # Ferramenta: consultar_agenda_hoje
        #
        # Essa ferramenta consulta automaticamente a agenda de hoje.
        # ----------------------------------------------------
        {
            "nome": "consultar_agenda_hoje",
            "descricao": "Use quando o usuário perguntar o que tem hoje, se tem algo hoje ou quais são os compromissos de hoje.",
            "parametros": {}
        },

        # ----------------------------------------------------
        # Ferramenta: consultar_agenda_amanha
        #
        # Essa ferramenta consulta automaticamente a agenda de amanhã.
        # ----------------------------------------------------
        {
            "nome": "consultar_agenda_amanha",
            "descricao": "Use quando o usuário perguntar o que tem amanhã, se tem algo amanhã ou se tem prova amanhã.",
            "parametros": {}
        },

        # ----------------------------------------------------
        # Ferramenta: consultar_agenda_semana_atual
        #
        # Essa ferramenta consulta compromissos da semana atual.
        # ----------------------------------------------------
        {
            "nome": "consultar_agenda_semana_atual",
            "descricao": "Use quando o usuário perguntar o que tem esta semana, quais são as aulas da semana ou quais compromissos tem na semana atual.",
            "parametros": {}
        },

        # ----------------------------------------------------
        # Ferramenta: consultar_tarefas
        #
        # Essa ferramenta lista as tarefas cadastradas.
        # ----------------------------------------------------
        {
            "nome": "consultar_tarefas",
            "descricao": "Use quando o usuário quiser listar, ver ou consultar as tarefas cadastradas.",
            "parametros": {}
        },

        # ----------------------------------------------------
        # Ferramenta: adicionar_tarefa
        #
        # Essa ferramenta adiciona uma nova tarefa.
        # ----------------------------------------------------
        {
            "nome": "adicionar_tarefa",
            "descricao": "Use quando o usuário quiser adicionar, criar, anotar ou registrar uma nova tarefa.",
            "parametros": {
                "titulo": "Título principal da tarefa.",
                "descricao": "Descrição opcional da tarefa. Se não houver descrição, use uma string vazia."
            }
        },
        
        # ----------------------------------------------------
        # Ferramenta: concluir_tarefa_por_descricao
        #
        # Essa ferramenta marca uma tarefa como concluída a partir
        # de uma descrição textual dada pelo usuário.
        # ----------------------------------------------------
        {
            "nome": "concluir_tarefa_por_descricao",
            "descricao": "Use quando o usuário quiser concluir, finalizar, marcar como feita ou dizer que terminou uma tarefa. A entrada deve ser uma descrição textual da tarefa mencionada pelo usuário.",
            "parametros": {
                "descricao_tarefa": "Descrição textual da tarefa que o usuário quer concluir. Exemplo: terminar o trabalho de ia."
            }
        },

        # ----------------------------------------------------
        # Ferramenta: consultar_material_rag
        #
        # Essa ferramenta recebe uma pergunta do usuário e retorna
        # uma resposta final baseada nos trechos recuperados dos
        # materiais de estudo.
        # ----------------------------------------------------
        {
            "nome": "consultar_material_rag",
            "descricao": "Use quando o usuário fizer perguntas sobre materiais de estudo, PDFs, textos, anotações ou conteúdos carregados no sistema.",
            "parametros": {
                "pergunta": "Descrição textual de uma pergunta relacionada a materiais de estudo. Exemplo: Explique regressão logística."
            }
        },

        # ----------------------------------------------------
        # Ferramenta: gerar_exercicios
        #
        # Essa ferramenta recebe uma solicitação do usuário para
        # gerar exercícios relacionados a um assunto e retorna
        # uma lista de exercícios com gabarito baseado nos trechos
        # recuperados dos materiais de estudo.
        # ----------------------------------------------------
        {
            "nome": "gerar_exercicios",
            "descricao": "Use quando o usuário pedir para gerar exercícios sobre algum determinado tema relacionado aos materiais de estudo, PDFs, textos, anotações ou conteúdos carregados no sistema. Exemplos: Gere uma lista de exercícios sobre Regressão Logística.",
            "parametros": {
                "tema": "Descrição textual do tema (conteúdo) no qual os exercícios irão se basear.",
                "qtde": "Valor numérico inteiro que determina a quantidade de exercícios que serão gerados. Não precisa ser específicado caso o usuário não defina nenhuma quantidade."
            }
        },

            # ----------------------------------------------------
        # Ferramenta: iniciar_active_recall
        #
        # Essa ferramenta inicia uma sessão interativa de estudo.
        #
        # Ela deve ser usada quando o usuário quiser que o sistema
        # faça uma pergunta sobre algum tema.
        #
        # Exemplo de intenção do usuário:
        #
        # - "me faça uma pergunta sobre Inteligência Artificial"
        # - "quero treinar active recall sobre RAG"
        # - "me teste sobre regressão logística"
        # - "faça uma pergunta para eu responder"
        # ----------------------------------------------------

        {
            "nome": "iniciar_active_recall",

            "descricao": "Use quando o usuário pedir para ser testado, quiser treinar active recall, pedir uma pergunta sobre um tema ou quiser que o sistema faça uma pergunta para ele responder.",

            "parametros": {
                "tema": "Tema ou conteúdo sobre o qual a pergunta de active recall deve ser gerada. Exemplo: Inteligência Artificial."
            }
        },

        # ----------------------------------------------------
        # Ferramenta: responder_active_recall
        #
        # Essa ferramenta avalia a resposta do usuário para uma
        # pergunta de active recall feita anteriormente.
        #
        # Ela deve ser usada quando o usuário estiver respondendo
        # uma pergunta ativa.
        #
        # Para facilitar a identificação, orientamos o usuário a
        # responder usando:
        #
        # resposta: texto da resposta
        #
        # Exemplo:
        #
        # "resposta: sistemas que pensam como humanos..."
        # ----------------------------------------------------

        {
            "nome": "responder_active_recall",

            "descricao": "Use quando o usuário responder uma pergunta de active recall feita anteriormente. Normalmente a mensagem começa com 'resposta:' ou indica que ele está tentando responder à pergunta feita pelo sistema.",

            "parametros": {
                "resposta_usuario": "Resposta textual enviada pelo usuário para a pergunta de active recall."
            }
        }
    ]

    # --------------------------------------------------------
    # Por fim, devolvemos a lista de descrições.
    #
    # Essa lista será usada depois para montar o prompt que pede
    # para a LLM decidir qual ferramenta deve ser chamada.
    # --------------------------------------------------------
    return descricoes

#endregion