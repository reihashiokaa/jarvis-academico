#region explicação do arquivo

# ============================================================
# Arquivo: tarefas.py
# ------------------------------------------------------------
# Este arquivo será responsável por lidar com a lista de tarefas
# acadêmicas do JARVIS.
#
# A lista de tarefas é uma das funcionalidades obrigatórias do
# Trabalho 1.
#
# Ela deve permitir que o usuário faça ações como:
#
# - adicionar uma nova tarefa;
# - listar tarefas cadastradas;
# - marcar uma tarefa como concluída.
#
# Neste arquivo, vamos criar funções para ler e modificar os
# dados das tarefas que estarão guardados no arquivo:
#
# data/tarefas.json
#
# A lógica geral usada neste arquivo seguirá o mesmo padrão do
# arquivo agenda.py:
#
# carregar_...
#   -> abre o arquivo e carrega dados gerais.
#
# salvar_...
#   -> grava dados atualizados de volta no arquivo.
#
# recuperar_...
#   -> recupera dados específicos, mas ainda em formato bruto.
#
# formatar_...
#   -> transforma dados brutos em texto mais bonito.
#
# consultar_...
#   -> faz o processo completo e devolve resposta pronta.
#
# adicionar_...
#   -> faz o processo completo de criar um novo item e salvar no arquivo.
#
# Algumas funções serão intermediárias.
#
# Isso significa que elas ajudam o sistema por dentro, mas não
# serão chamadas diretamente pela LLM como ferramentas finais.
#
# Outras funções serão marcadas como:
#
# FINAL, será uma ferramenta
#
# Essas serão candidatas a serem chamadas pela LLM no tool calling.
# ============================================================

#endregion

#region importações

# ------------------------------------------------------------
# Importamos a biblioteca json.
#
# JSON é o formato que vamos usar para guardar as tarefas no
# arquivo data/tarefas.json.
#
# O arquivo tarefas.json vai conter uma lista de tarefas.
#
# Exemplo:
#
# [
#     {
#         "id": 1,
#         "titulo": "Estudar RAG",
#         "descricao": "Revisar chunking e embeddings",
#         "concluida": false
#     }
# ]
#
# A biblioteca json permite que o Python leia e escreva esse tipo
# de arquivo.
# ------------------------------------------------------------
import json


# ------------------------------------------------------------
# Importamos Path da biblioteca pathlib.
#
# O Path ajuda o Python a trabalhar com caminhos de arquivos e
# pastas de uma forma mais organizada.
#
# Neste arquivo, vamos usar Path para encontrar o arquivo:
#
# data/tarefas.json
#
# sem depender de escrever o caminho manualmente de um jeito que
# possa quebrar em outro computador.
# ------------------------------------------------------------
from pathlib import Path

# ------------------------------------------------------------
# Importamos a função recuperar_decisao_tarefa_por_descricao.
#
# Essa função está no arquivo llm_client.py.
#
# Ela será usada para pedir ao Gemma que compare uma descrição
# textual do usuário com a lista de tarefas cadastradas.
#
# Exemplo:
#
# descrição do usuário:
# "terminar o trabalho de ia"
#
# tarefas cadastradas:
# [
#     {"id": 5, "titulo": "terminar o trabalho de ia"}
# ]
#
# A função recuperar_decisao_tarefa_por_descricao(...) pede para
# a LLM identificar qual tarefa corresponde melhor à descrição.
#
# Ela devolve uma decisão em formato de dicionário Python, como:
#
# {
#     "encontrou": True,
#     "id_tarefa": 5,
#     "ambigua": False,
#     "ids_possiveis": [],
#     "mensagem": "A descrição corresponde à tarefa de id 5."
# }
#
# Essa decisão será usada pela função final:
#
# concluir_tarefa_por_descricao(...)
# ------------------------------------------------------------
from src.llm_client import recuperar_decisao_tarefa_por_descricao

#endregion

#region caminho do arquivo de tarefas

# ------------------------------------------------------------
# Aqui definimos o caminho até o arquivo tarefas.json.
#
# Vamos entender com calma:
#
# __file__
#   representa o caminho deste arquivo atual, ou seja:
#   src/tarefas.py
#
# Path(__file__)
#   transforma esse caminho em um objeto Path.
#
# Path(__file__).resolve()
#   pega o caminho completo no computador.
#
# Path(__file__).resolve().parent
#   pega a pasta onde este arquivo está.
#   Neste caso, a pasta é:
#   src/
#
# Path(__file__).resolve().parent.parent
#   sobe uma pasta.
#   Como tarefas.py está dentro de src/, subir uma pasta nos leva
#   para a pasta principal do projeto:
#   jarvis-academico/
#
# Depois juntamos:
#   "data" / "tarefas.json"
#
# Resultado final:
#   jarvis-academico/data/tarefas.json
# ------------------------------------------------------------
CAMINHO_TAREFAS = Path(__file__).resolve().parent.parent / "data" / "tarefas.json"

#endregion

#region carregar_tarefas (intermediária, retorna lista com todas as tarefas)

# ------------------------------------------------------------
# Função: carregar_tarefas
# ------------------------------------------------------------
# Esta função lê o arquivo data/tarefas.json e devolve o conteúdo
# dele para o restante do programa.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por enquanto, o conteúdo do arquivo tarefas.json será uma lista.
#
# Se o arquivo estiver vazio de tarefas, ele terá:
#
# []
#
# Então esta função devolverá uma lista vazia.
#
# Se o arquivo tiver tarefas cadastradas, ela devolverá uma lista
# de dicionários, onde cada dicionário representa uma tarefa.
#
# Exemplo de tarefa:
#
# {
#     "id": 1,
#     "titulo": "Estudar RAG",
#     "descricao": "Revisar chunking e embeddings",
#     "concluida": false
# }
# ------------------------------------------------------------
def carregar_tarefas():
    # --------------------------------------------------------
    # Aqui abrimos o arquivo tarefas.json em modo de leitura.
    #
    # open(...) serve para abrir arquivos.
    #
    # CAMINHO_TAREFAS é o caminho até o arquivo que queremos abrir.
    #
    # "r" significa read, ou seja, leitura.
    #
    # encoding="utf-8" ajuda o Python a lidar corretamente com
    # acentos e caracteres especiais da língua portuguesa.
    #
    # O "with" é usado porque ele abre o arquivo, usa o arquivo
    # e depois fecha automaticamente.
    #
    # Isso é mais seguro do que abrir o arquivo manualmente e
    # esquecer de fechar depois.
    # --------------------------------------------------------
    with open(CAMINHO_TAREFAS, "r", encoding="utf-8") as arquivo:
        # ----------------------------------------------------
        # json.load(arquivo) lê o conteúdo do arquivo JSON e
        # transforma esse conteúdo em uma estrutura do Python.
        #
        # Se o arquivo contém:
        #
        # []
        #
        # o Python transforma isso em uma lista vazia.
        #
        # Se o arquivo contém uma lista de tarefas, o Python
        # transforma isso em uma lista de dicionários.
        # ----------------------------------------------------
        tarefas = json.load(arquivo)

    # --------------------------------------------------------
    # Aqui devolvemos as tarefas para quem chamou a função.
    #
    # Exemplo:
    #
    # lista_de_tarefas = carregar_tarefas()
    #
    # Depois disso, a variável "lista_de_tarefas" terá o conteúdo
    # lido de data/tarefas.json.
    # --------------------------------------------------------
    return tarefas

#endregion

#region salvar_tarefas (intermediária, recebe lista de tarefas e escreve no arquivo)

# ------------------------------------------------------------
# Função: salvar_tarefas
# ------------------------------------------------------------
# Esta função recebe uma lista de tarefas e grava essa lista no
# arquivo data/tarefas.json.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos dessa função?
#
# Porque algumas operações modificam a lista de tarefas.
#
# Exemplos:
#
# - adicionar uma nova tarefa;
# - marcar uma tarefa como concluída;
# - futuramente remover ou editar uma tarefa.
#
# Quando uma dessas operações acontecer, não basta alterar a lista
# apenas na memória do Python.
#
# Precisamos salvar a lista atualizada de volta no arquivo
# tarefas.json, para que os dados continuem existindo mesmo depois
# que o programa for fechado.
#
# Em resumo:
#
# carregar_tarefas()
#   -> lê as tarefas do arquivo.
#
# salvar_tarefas(tarefas)
#   -> grava as tarefas atualizadas no arquivo.
# ------------------------------------------------------------
def salvar_tarefas(tarefas: list):
    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista completa de tarefas
    # que queremos salvar no arquivo.
    #
    # Essa lista pode estar:
    #
    # - vazia;
    # - com uma tarefa;
    # - com várias tarefas.
    #
    # Exemplo:
    #
    # [
    #     {
    #         "id": 1,
    #         "titulo": "Estudar RAG",
    #         "descricao": "Revisar chunking e embeddings",
    #         "concluida": False
    #     }
    # ]
    #
    # Repare que, em Python, usamos False com F maiúsculo.
    # Quando isso for salvo em JSON, aparecerá como false.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Aqui abrimos o arquivo tarefas.json em modo de escrita.
    #
    # open(...) serve para abrir arquivos.
    #
    # CAMINHO_TAREFAS é o caminho até o arquivo que queremos
    # modificar.
    #
    # "w" significa write, ou seja, escrita.
    #
    # Atenção:
    # quando abrimos um arquivo em modo "w", o conteúdo antigo
    # será substituído pelo novo conteúdo que vamos gravar.
    #
    # Isso é o que queremos aqui, porque vamos salvar a lista
    # completa e atualizada de tarefas.
    #
    # encoding="utf-8" ajuda a manter acentos e caracteres
    # especiais funcionando corretamente.
    # --------------------------------------------------------
    with open(CAMINHO_TAREFAS, "w", encoding="utf-8") as arquivo:
        # ----------------------------------------------------
        # json.dump(...) grava dados Python dentro de um arquivo
        # no formato JSON.
        #
        # Aqui estamos dizendo:
        #
        # grave a lista "tarefas" dentro do "arquivo".
        #
        # ensure_ascii=False
        #   permite salvar acentos normalmente.
        #
        # indent=2
        #   deixa o arquivo JSON organizado, com espaçamento.
        #
        # Sem indent=2, o JSON ficaria todo em uma linha só.
        # Com indent=2, ele fica mais fácil de ler.
        # ----------------------------------------------------
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)

#endregion

#region recuperar_proximo_id (intermediária, recebe lista de tarefas e retorna o próximo id disponível) 
#será usada para o usuário não precisar colocar o id manualmente quando criar uma nova tarefa também!

# ------------------------------------------------------------
# Função: recuperar_proximo_id
# ------------------------------------------------------------
# Esta função descobre qual deve ser o próximo id de uma nova
# tarefa.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos de um id?
#
# Porque cada tarefa precisa ter uma identificação única.
#
# Exemplo:
#
# {
#     "id": 1,
#     "titulo": "Estudar RAG",
#     "descricao": "Revisar chunking e embeddings",
#     "concluida": false
# }
#
# Esse id será útil quando quisermos marcar uma tarefa específica
# como concluída.
#
# Por exemplo:
#
# concluir_tarefa(1)
#
# Assim o sistema sabe exatamente qual tarefa deve ser alterada.
#
# A lógica desta função será:
#
# 1. receber a lista de tarefas;
# 2. verificar se a lista está vazia;
# 3. se estiver vazia, devolver 1;
# 4. se não estiver vazia, encontrar o maior id existente;
# 5. devolver maior id + 1.
# ------------------------------------------------------------
def recuperar_proximo_id(tarefas: list) -> int:
    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista de tarefas já
    # carregada do arquivo data/tarefas.json.
    #
    # Essa lista pode estar vazia:
    #
    # []
    #
    # Ou pode ter tarefas:
    #
    # [
    #     {
    #         "id": 1,
    #         "titulo": "Estudar RAG",
    #         "descricao": "Revisar chunking e embeddings",
    #         "concluida": False
    #     }
    # ]
    #
    # O retorno desta função será um número inteiro.
    #
    # Por isso usamos:
    #
    # -> int
    #
    # Isso indica que a função devolve um número inteiro.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro tratamos o caso mais simples:
    # a lista de tarefas está vazia.
    #
    # Em Python, uma lista vazia é considerada "falsa".
    #
    # Então:
    #
    # if not tarefas:
    #
    # significa:
    #
    # "se não existem tarefas nessa lista".
    #
    # Se não existe nenhuma tarefa ainda, a primeira tarefa deve
    # receber o id 1.
    # --------------------------------------------------------
    if not tarefas:
        return 1

    # --------------------------------------------------------
    # Se chegamos aqui, significa que já existe pelo menos uma
    # tarefa cadastrada.
    #
    # Agora precisamos descobrir qual é o maior id existente.
    #
    # Vamos criar uma lista chamada ids.
    #
    # Essa lista vai guardar apenas os ids das tarefas.
    #
    # Exemplo:
    #
    # se tarefas for:
    #
    # [
    #     {"id": 1, "titulo": "Estudar RAG"},
    #     {"id": 2, "titulo": "Fazer README"}
    # ]
    #
    # então ids será:
    #
    # [1, 2]
    # --------------------------------------------------------
    ids = []

    # --------------------------------------------------------
    # Agora percorremos cada tarefa da lista.
    #
    # "for tarefa in tarefas" significa:
    #
    # para cada tarefa dentro da lista tarefas,
    # execute o bloco de código abaixo.
    # --------------------------------------------------------
    for tarefa in tarefas:
        # ----------------------------------------------------
        # Aqui pegamos o campo "id" da tarefa.
        #
        # Usamos tarefa.get("id") em vez de tarefa["id"] porque
        # .get é mais seguro.
        #
        # Se por algum motivo uma tarefa estiver sem id,
        # tarefa.get("id") devolverá None em vez de quebrar o
        # programa imediatamente.
        # ----------------------------------------------------
        id_tarefa = tarefa.get("id")

        # ----------------------------------------------------
        # Agora verificamos se o id realmente é um número inteiro.
        #
        # isinstance(id_tarefa, int) significa:
        #
        # "id_tarefa é do tipo inteiro?"
        #
        # Isso evita colocar valores inválidos dentro da lista
        # de ids.
        # ----------------------------------------------------
        if isinstance(id_tarefa, int):
            # ------------------------------------------------
            # Se o id é válido, adicionamos esse id na lista ids.
            # ------------------------------------------------
            ids.append(id_tarefa)

    # --------------------------------------------------------
    # Agora tratamos um caso de segurança.
    #
    # Pode acontecer de a lista de tarefas existir, mas nenhuma
    # tarefa ter um id válido.
    #
    # Nesse caso, a lista ids ficaria vazia.
    #
    # Se ids estiver vazia, vamos devolver 1.
    # --------------------------------------------------------
    if not ids:
        return 1

    # --------------------------------------------------------
    # Se existem ids válidos, usamos max(ids) para descobrir o
    # maior id cadastrado.
    #
    # Exemplo:
    #
    # ids = [1, 2, 3]
    #
    # max(ids) devolve 3.
    # --------------------------------------------------------
    maior_id = max(ids)

    # --------------------------------------------------------
    # O próximo id será o maior id atual + 1.
    #
    # Exemplo:
    #
    # maior_id = 3
    #
    # próximo id = 4
    # --------------------------------------------------------
    proximo_id = maior_id + 1

    # --------------------------------------------------------
    # Por fim, devolvemos o próximo id disponível.
    # --------------------------------------------------------
    return proximo_id

#endregion

#region formatar_tarefas (intermediária, recebe lista de tarefas e devolve texto formatado)

# ------------------------------------------------------------
# Função: formatar_tarefas
# ------------------------------------------------------------
# Esta função transforma uma lista de tarefas em um texto mais
# bonito e mais fácil de ler.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque as tarefas ficam guardadas no arquivo tarefas.json em
# formato de dados.
#
# Exemplo de formato bruto:
#
# [
#     {
#         "id": 1,
#         "titulo": "Estudar RAG",
#         "descricao": "Revisar chunking e embeddings",
#         "concluida": false
#     }
# ]
#
# Esse formato é bom para o programa, mas não é o melhor formato
# para mostrar ao usuário.
#
# Queremos transformar isso em uma resposta textual mais clara,
# por exemplo:
#
# Você tem 1 tarefa cadastrada:
#
# - [1] Estudar RAG | pendente
#   Revisar chunking e embeddings
#
# Assim, quando o usuário pedir para listar as tarefas, o sistema
# poderá mostrar uma resposta mais organizada.
# ------------------------------------------------------------
def formatar_tarefas(tarefas: list) -> str:
    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista de tarefas que
    # queremos transformar em texto.
    #
    # Essa lista pode estar:
    #
    # - vazia;
    # - com uma tarefa;
    # - com várias tarefas.
    #
    # Cada tarefa deve ser um dicionário com campos como:
    #
    # - id;
    # - titulo;
    # - descricao;
    # - concluida.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro tratamos o caso em que a lista de tarefas está
    # vazia.
    #
    # Em Python, uma lista vazia é considerada "falsa".
    #
    # Então:
    #
    # if not tarefas:
    #
    # significa:
    #
    # "se não existem tarefas dentro dessa lista".
    # --------------------------------------------------------
    if not tarefas:
        # ----------------------------------------------------
        # Se não houver tarefas cadastradas, devolvemos uma
        # mensagem simples para o usuário.
        # ----------------------------------------------------
        return "Você não tem tarefas cadastradas."

    # --------------------------------------------------------
    # Se chegamos aqui, significa que existe pelo menos uma
    # tarefa cadastrada.
    #
    # Agora vamos montar uma lista chamada "linhas".
    #
    # Cada item dessa lista será uma linha do texto final.
    #
    # No final da função, vamos juntar essas linhas em um texto só.
    # --------------------------------------------------------
    linhas = []

    # --------------------------------------------------------
    # A primeira linha informa quantas tarefas foram encontradas.
    #
    # len(tarefas) conta quantos itens existem dentro da lista.
    #
    # Exemplo:
    #
    # se existe 1 tarefa, len(tarefas) será 1.
    # se existem 3 tarefas, len(tarefas) será 3.
    # --------------------------------------------------------
    linhas.append(f"Você tem {len(tarefas)} tarefa(s) cadastrada(s):")

    # --------------------------------------------------------
    # Adicionamos uma linha vazia para deixar a resposta mais
    # confortável visualmente.
    # --------------------------------------------------------
    linhas.append("")

    # --------------------------------------------------------
    # Agora vamos percorrer cada tarefa da lista.
    #
    # "for tarefa in tarefas" significa:
    #
    # para cada tarefa dentro da lista tarefas,
    # execute o bloco de código abaixo.
    # --------------------------------------------------------
    for tarefa in tarefas:
        # ----------------------------------------------------
        # Aqui pegamos o id da tarefa.
        #
        # Usamos .get("id", "sem id") em vez de tarefa["id"]
        # porque .get é mais seguro.
        #
        # Se o campo "id" existir, ele pega o valor.
        # Se o campo "id" não existir, ele usa "sem id".
        # ----------------------------------------------------
        id_tarefa = tarefa.get("id", "sem id")

        # ----------------------------------------------------
        # Aqui pegamos o título da tarefa.
        #
        # Se o campo "titulo" não existir, usamos "Sem título".
        # ----------------------------------------------------
        titulo = tarefa.get("titulo", "Sem título")

        # ----------------------------------------------------
        # Aqui pegamos a descrição da tarefa.
        #
        # Se o campo "descricao" não existir, usamos uma string
        # vazia.
        #
        # String vazia significa simplesmente "sem texto".
        # ----------------------------------------------------
        descricao = tarefa.get("descricao", "")

        # ----------------------------------------------------
        # Aqui pegamos o status da tarefa.
        #
        # O campo "concluida" deve ser um valor booleano:
        #
        # True  -> tarefa concluída
        # False -> tarefa pendente
        #
        # Usamos False como valor padrão porque, se esse campo
        # estiver faltando, é mais seguro considerar a tarefa como
        # ainda não concluída.
        # ----------------------------------------------------
        concluida = tarefa.get("concluida", False)

        # ----------------------------------------------------
        # Agora transformamos o valor booleano em um texto mais
        # fácil de entender.
        #
        # Se concluida for True:
        #   status será "concluída"
        #
        # Se concluida for False:
        #   status será "pendente"
        # ----------------------------------------------------
        if concluida:
            status = "concluída"
        else:
            status = "pendente"

        # ----------------------------------------------------
        # Agora adicionamos a linha principal da tarefa.
        #
        # Exemplo:
        #
        # - [1] Estudar RAG | pendente
        #
        # O id aparece entre colchetes porque depois ele será útil
        # para concluir uma tarefa específica.
        # ----------------------------------------------------
        linhas.append(f"- [{id_tarefa}] {titulo} | {status}")

        # ----------------------------------------------------
        # Se a tarefa tiver descrição, adicionamos a descrição na
        # linha de baixo.
        #
        # O if descricao verifica se a descrição não está vazia.
        # ----------------------------------------------------
        if descricao:
            linhas.append(f"  {descricao}")

    # --------------------------------------------------------
    # Por fim, juntamos todas as linhas em um único texto.
    #
    # "\n" significa quebra de linha.
    #
    # Então:
    #
    # "\n".join(linhas)
    #
    # pega a lista de linhas e junta tudo em um texto só,
    # colocando uma quebra de linha entre cada item.
    # --------------------------------------------------------
    return "\n".join(linhas)

#endregion

#region consultar_tarefas (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_tarefas
# ------------------------------------------------------------
# Esta função consulta todas as tarefas cadastradas e devolve uma
# resposta formatada para o usuário.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será uma candidata a ferramenta no futuro
# tool calling.
#
# Quando o usuário perguntar algo como:
#
# - "Quais são minhas tarefas?"
# - "Liste minhas tarefas"
# - "O que tenho para fazer?"
#
# a LLM poderá escolher chamar esta função.
#
# A ideia desta função é juntar duas etapas que já criamos:
#
# 1. carregar_tarefas()
#    -> lê o arquivo data/tarefas.json e recupera a lista bruta
#       de tarefas.
#
# 2. formatar_tarefas(tarefas)
#    -> transforma essa lista bruta em um texto mais bonito e
#       mais fácil de ler.
#
# Assim, esta função já devolve uma resposta pronta para ser
# mostrada ao usuário.
# ------------------------------------------------------------
def consultar_tarefas() -> str:
    # --------------------------------------------------------
    # Primeiro, carregamos todas as tarefas cadastradas no arquivo
    # data/tarefas.json.
    #
    # A função carregar_tarefas() devolve uma lista.
    #
    # Exemplo de lista vazia:
    #
    # []
    #
    # Exemplo de lista com uma tarefa:
    #
    # [
    #     {
    #         "id": 1,
    #         "titulo": "Estudar RAG",
    #         "descricao": "Revisar chunking e embeddings",
    #         "concluida": False
    #     }
    # ]
    # --------------------------------------------------------
    tarefas = carregar_tarefas()

    # --------------------------------------------------------
    # Agora transformamos a lista de tarefas em uma resposta
    # textual mais fácil de entender.
    #
    # A função formatar_tarefas(...) já sabe lidar com:
    #
    # - lista vazia;
    # - lista com uma tarefa;
    # - lista com várias tarefas.
    #
    # Então não precisamos repetir essa lógica aqui.
    # --------------------------------------------------------
    resposta = formatar_tarefas(tarefas)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta formatada.
    #
    # Quem chamar consultar_tarefas() receberá um texto pronto,
    # e não uma lista bruta de Python.
    # --------------------------------------------------------
    return resposta

#endregion

#region montar_nova_tarefa (intermediária, recebe dados da tarefa inseridos pelo usuário e retorna um dicionário em formato bruto)

# ------------------------------------------------------------
# Função: montar_nova_tarefa
# ------------------------------------------------------------
# Esta função monta a estrutura de uma nova tarefa.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque uma tarefa precisa seguir sempre o mesmo formato dentro
# do arquivo data/tarefas.json.
#
# O formato escolhido para cada tarefa será:
#
# {
#     "id": 1,
#     "titulo": "Estudar RAG",
#     "descricao": "Revisar chunking e embeddings",
#     "concluida": false
# }
#
# Essa função recebe os dados principais da tarefa e devolve um
# dicionário Python já organizado nesse formato.
#
# Ela ainda NÃO salva a tarefa no arquivo.
#
# Ela apenas monta a tarefa.
# ------------------------------------------------------------
def montar_nova_tarefa(id_tarefa: int, titulo: str, descricao: str = "") -> dict:
    # --------------------------------------------------------
    # O parâmetro "id_tarefa" representa o número identificador
    # da tarefa.
    #
    # Exemplo:
    #
    # 1
    #
    # Esse id será usado depois para marcar uma tarefa específica
    # como concluída.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "titulo" representa o nome principal da tarefa.
    #
    # Exemplo:
    #
    # "Estudar RAG"
    #
    # Esse campo é obrigatório, porque uma tarefa precisa ter pelo
    # menos um título para o usuário entender o que deve fazer.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "descricao" representa uma explicação adicional
    # sobre a tarefa.
    #
    # Exemplo:
    #
    # "Revisar chunking e embeddings"
    #
    # Esse campo tem valor padrão "".
    #
    # Isso significa que a descrição é opcional.
    #
    # Se o usuário não informar uma descrição, a tarefa será criada
    # com descrição vazia.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Aqui montamos o dicionário que representa a nova tarefa.
    #
    # Um dicionário em Python guarda informações em pares:
    #
    # chave: valor
    #
    # Neste caso, as chaves são:
    #
    # - id;
    # - titulo;
    # - descricao;
    # - concluida.
    #
    # O campo "concluida" começa como False porque toda nova tarefa
    # deve nascer como pendente.
    #
    # Em Python usamos False com F maiúsculo.
    #
    # Quando a tarefa for salva no JSON, esse valor aparecerá como:
    #
    # false
    # --------------------------------------------------------
    nova_tarefa = {
        "id": id_tarefa,
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False
    }

    # --------------------------------------------------------
    # Por fim, devolvemos o dicionário da nova tarefa.
    #
    # Quem chamar esta função receberá a tarefa pronta em formato
    # bruto, mas ainda não salva no arquivo.
    # --------------------------------------------------------
    return nova_tarefa

#endregion

#region adicionar_tarefa (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: adicionar_tarefa
# ------------------------------------------------------------
# Esta função adiciona uma nova tarefa ao arquivo data/tarefas.json.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será uma candidata a ferramenta no futuro
# tool calling.
#
# Quando o usuário disser algo como:
#
# - "Adicione uma tarefa para estudar RAG"
# - "Crie uma tarefa chamada fazer README"
# - "Anote que preciso revisar embeddings"
#
# a LLM poderá escolher chamar esta função.
#
# A lógica desta função será:
#
# 1. carregar as tarefas já existentes;
# 2. descobrir qual é o próximo id disponível;
# 3. montar a nova tarefa;
# 4. adicionar a nova tarefa na lista;
# 5. salvar a lista atualizada no arquivo tarefas.json;
# 6. devolver uma mensagem de confirmação para o usuário.
#
# Repare que esta função usa várias funções intermediárias que já
# criamos:
#
# carregar_tarefas()
#   -> lê a lista atual de tarefas.
#
# recuperar_proximo_id(tarefas)
#   -> descobre qual id a nova tarefa deve receber.
#
# montar_nova_tarefa(id, titulo, descricao)
#   -> monta o dicionário da nova tarefa.
#
# salvar_tarefas(tarefas)
#   -> grava a lista atualizada no arquivo.
# ------------------------------------------------------------
def adicionar_tarefa(titulo: str, descricao: str = "") -> str:
    # --------------------------------------------------------
    # O parâmetro "titulo" representa o nome principal da tarefa.
    #
    # Exemplo:
    #
    # "Estudar RAG"
    #
    # Esse campo é obrigatório, porque uma tarefa precisa ter um
    # título para fazer sentido.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "descricao" representa uma explicação adicional
    # sobre a tarefa.
    #
    # Exemplo:
    #
    # "Revisar chunking e embeddings"
    #
    # Esse campo é opcional.
    #
    # Por isso usamos:
    #
    # descricao: str = ""
    #
    # Isso significa que, se nenhuma descrição for informada, o
    # Python usará uma string vazia.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, carregamos todas as tarefas que já existem no
    # arquivo data/tarefas.json.
    #
    # A função carregar_tarefas() devolve uma lista.
    #
    # Exemplo:
    #
    # [
    #     {
    #         "id": 1,
    #         "titulo": "Estudar RAG",
    #         "descricao": "Revisar chunking e embeddings",
    #         "concluida": False
    #     }
    # ]
    # --------------------------------------------------------
    tarefas = carregar_tarefas()

    # --------------------------------------------------------
    # Agora descobrimos qual deve ser o id da nova tarefa.
    #
    # A função recuperar_proximo_id(tarefas) olha para a lista de
    # tarefas existentes e devolve o próximo número disponível.
    #
    # Exemplo:
    #
    # se já existe uma tarefa com id 1,
    # o próximo id será 2.
    # --------------------------------------------------------
    proximo_id = recuperar_proximo_id(tarefas)

    # --------------------------------------------------------
    # Agora montamos a nova tarefa em formato de dicionário Python.
    #
    # A função montar_nova_tarefa(...) cria uma estrutura como:
    #
    # {
    #     "id": 2,
    #     "titulo": "Fazer README",
    #     "descricao": "Escrever instruções básicas do projeto",
    #     "concluida": False
    # }
    #
    # Neste momento, a tarefa ainda está apenas na memória do
    # Python. Ela ainda não foi salva no arquivo.
    # --------------------------------------------------------
    nova_tarefa = montar_nova_tarefa(proximo_id, titulo, descricao)

    # --------------------------------------------------------
    # Agora adicionamos a nova tarefa na lista de tarefas.
    #
    # append significa "adicionar ao final da lista".
    #
    # Antes:
    #
    # tarefas = [tarefa 1]
    #
    # Depois:
    #
    # tarefas = [tarefa 1, nova tarefa]
    # --------------------------------------------------------
    tarefas.append(nova_tarefa)

    # --------------------------------------------------------
    # Agora salvamos a lista atualizada de tarefas no arquivo
    # data/tarefas.json.
    #
    # Isso é importante porque, se não salvarmos no arquivo, a
    # nova tarefa existiria apenas temporariamente na memória do
    # programa.
    #
    # Quando o programa fosse fechado, a tarefa seria perdida.
    # --------------------------------------------------------
    salvar_tarefas(tarefas)

    # --------------------------------------------------------
    # Por fim, devolvemos uma mensagem de confirmação.
    #
    # Essa mensagem será mostrada ao usuário para indicar que a
    # tarefa foi criada com sucesso.
    #
    # Também mostramos o id da tarefa, porque esse número será útil
    # depois para marcar a tarefa como concluída.
    # --------------------------------------------------------
    return f"Tarefa adicionada com sucesso: [{proximo_id}] {titulo}"

#endregion

#region recuperar_tarefa_por_id (intermediária, recebe lista de tarefas e retorna a tarefa com o Id fornecido)

# ------------------------------------------------------------
# Função: recuperar_tarefa_por_id
# ------------------------------------------------------------
# Esta função procura uma tarefa específica dentro de uma lista
# de tarefas usando o id da tarefa.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque cada tarefa tem um id único.
#
# Exemplo de tarefa:
#
# {
#     "id": 2,
#     "titulo": "Fazer README",
#     "descricao": "Escrever instruções básicas do projeto",
#     "concluida": false
# }
#
# Se o usuário quiser concluir a tarefa 2, o sistema precisa
# encontrar dentro da lista qual tarefa tem:
#
# "id": 2
#
# A lógica desta função será:
#
# 1. receber a lista de tarefas;
# 2. receber o id procurado;
# 3. percorrer cada tarefa da lista;
# 4. comparar o id da tarefa com o id procurado;
# 5. devolver a tarefa se encontrar;
# 6. devolver None se não encontrar.
#
# Importante:
#
# Esta função apenas recupera a tarefa.
# Ela ainda NÃO altera a tarefa.
# Ela ainda NÃO salva nada no arquivo.
# ------------------------------------------------------------
def recuperar_tarefa_por_id(tarefas: list, id_procurado: int):
    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista de tarefas já
    # carregada do arquivo data/tarefas.json.
    #
    # Exemplo:
    #
    # [
    #     {
    #         "id": 1,
    #         "titulo": "Estudar RAG",
    #         "descricao": "Revisar chunking e embeddings",
    #         "concluida": False
    #     },
    #     {
    #         "id": 2,
    #         "titulo": "Fazer README",
    #         "descricao": "Escrever instruções básicas do projeto",
    #         "concluida": False
    #     }
    # ]
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "id_procurado" representa o id da tarefa que
    # queremos encontrar.
    #
    # Exemplo:
    #
    # id_procurado = 2
    #
    # Nesse caso, a função vai procurar a tarefa que tem:
    #
    # "id": 2
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Agora percorremos cada tarefa dentro da lista de tarefas.
    #
    # "for tarefa in tarefas" significa:
    #
    # para cada tarefa dentro da lista tarefas,
    # execute o bloco de código abaixo.
    # --------------------------------------------------------
    for tarefa in tarefas:
        # ----------------------------------------------------
        # Aqui recuperamos o id da tarefa atual.
        #
        # Usamos tarefa.get("id") em vez de tarefa["id"] porque
        # .get é mais seguro.
        #
        # Se por algum motivo a tarefa não tiver o campo "id",
        # tarefa.get("id") devolverá None em vez de quebrar o
        # programa imediatamente.
        # ----------------------------------------------------
        id_tarefa = tarefa.get("id")

        # ----------------------------------------------------
        # Agora comparamos o id da tarefa atual com o id que
        # estamos procurando.
        #
        # Se forem iguais, encontramos a tarefa desejada.
        #
        # Exemplo:
        #
        # id_tarefa = 2
        # id_procurado = 2
        #
        # Como são iguais, esta é a tarefa procurada.
        # ----------------------------------------------------
        if id_tarefa == id_procurado:
            # ------------------------------------------------
            # Se encontramos a tarefa, devolvemos essa tarefa.
            #
            # A tarefa será devolvida em formato bruto, ou seja,
            # como dicionário Python.
            #
            # Exemplo:
            #
            # {
            #     "id": 2,
            #     "titulo": "Fazer README",
            #     "descricao": "Escrever instruções básicas do projeto",
            #     "concluida": False
            # }
            # ------------------------------------------------
            return tarefa

    # --------------------------------------------------------
    # Se o for terminou e não encontramos nenhuma tarefa com o
    # id procurado, devolvemos None.
    #
    # None significa "nenhum valor encontrado".
    #
    # Isso será útil depois, porque a função concluir_tarefa()
    # poderá verificar:
    #
    # se recuperar_tarefa_por_id(...) devolveu None,
    # então a tarefa não existe.
    # --------------------------------------------------------
    return None

#endregion

#region concluir_tarefa_por_id (intermediária, recebe o id da tarefa e marca a tarefa como concluída)

# ------------------------------------------------------------
# Função: concluir_tarefa_por_id
# ------------------------------------------------------------
# Esta função marca uma tarefa como concluída usando o id da tarefa.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que ela deixou de ser uma função FINAL?
#
# Porque o usuário normalmente não quer ficar informando id.
#
# O usuário tende a falar de forma natural, por exemplo:
#
# "conclua a tarefa de terminar o trabalho de IA"
#
# Então a função FINAL será outra:
#
# concluir_tarefa_por_descricao(...)
#
# Essa função final tentará descobrir qual id da tarefa o usuário quis
# dizer e, depois disso, chamará esta função aqui passando o id.
#
# Ou seja:
#
# concluir_tarefa_por_descricao("terminar o trabalho de IA")
#        ↓
# identifica que a tarefa correta é a de id 5
#        ↓
# chama concluir_tarefa_por_id(5)
#
# A lógica desta função será:
#
# 1. receber o id da tarefa;
# 2. converter esse id para número inteiro, se necessário;
# 3. carregar todas as tarefas cadastradas;
# 4. procurar a tarefa com o id informado;
# 5. verificar se a tarefa existe;
# 6. verificar se a tarefa já está concluída;
# 7. marcar a tarefa como concluída;
# 8. salvar a lista atualizada no arquivo tarefas.json;
# 9. devolver uma mensagem de confirmação.
# ------------------------------------------------------------
def concluir_tarefa_por_id(id_tarefa: int) -> str:
    # --------------------------------------------------------
    # O parâmetro "id_tarefa" representa o identificador da tarefa
    # que queremos marcar como concluída.
    #
    # Exemplo:
    #
    # id_tarefa = 5
    #
    # Isso significa:
    #
    # "quero concluir a tarefa que tem id 5".
    #
    # Mesmo sendo uma função intermediária, vamos deixar ela mais
    # resistente, porque às vezes a LLM pode enviar o id como texto.
    #
    # Exemplo:
    #
    # 5
    #
    # ou:
    #
    # "5"
    #
    # Para uma pessoa, os dois parecem a mesma coisa.
    # Para o Python, são tipos diferentes.
    #
    # Por isso, vamos tentar converter o valor recebido para inteiro.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro tratamos o caso em que nenhum id foi informado.
    #
    # Se id_tarefa vier como None, não temos como saber qual tarefa
    # deve ser concluída.
    #
    # Nesse caso, devolvemos uma mensagem amigável.
    # --------------------------------------------------------
    if id_tarefa is None:
        return (
            "Para concluir uma tarefa, preciso identificar qual tarefa você quer concluir. "
            "Descreva melhor a tarefa ou informe o ID dela."
        )

    # --------------------------------------------------------
    # Agora tentamos converter o id recebido para número inteiro.
    #
    # Isso resolve o caso em que o id vem como string.
    #
    # Exemplo:
    #
    # int("5") vira 5
    #
    # Se id_tarefa já for 5, ele continua funcionando.
    # --------------------------------------------------------
    try:
        id_tarefa = int(id_tarefa)

    except ValueError:
        # ----------------------------------------------------
        # ValueError acontece quando o valor não pode ser convertido
        # para inteiro.
        #
        # Exemplo:
        #
        # int("trabalho de ia")
        #
        # Isso não funciona, porque esse texto não é um número.
        # ----------------------------------------------------
        return (
            "Não consegui identificar um ID numérico válido para a tarefa. "
            "Descreva melhor a tarefa ou informe um número de ID."
        )

    except TypeError:
        # ----------------------------------------------------
        # TypeError cobre casos em que o valor recebido tem um tipo
        # que não pode ser convertido adequadamente.
        #
        # Por segurança, devolvemos uma mensagem amigável.
        # ----------------------------------------------------
        return (
            "Não consegui identificar um ID numérico válido para a tarefa. "
            "Descreva melhor a tarefa ou informe um número de ID."
        )

    # --------------------------------------------------------
    # Agora carregamos todas as tarefas cadastradas no arquivo
    # data/tarefas.json.
    #
    # A função carregar_tarefas() devolve uma lista de tarefas.
    # --------------------------------------------------------
    tarefas = carregar_tarefas()

    # --------------------------------------------------------
    # Agora tentamos recuperar a tarefa que tem o id informado.
    #
    # A função recuperar_tarefa_por_id(...) percorre a lista de
    # tarefas e devolve:
    #
    # - a tarefa encontrada, se existir;
    # - None, se não existir tarefa com aquele id.
    # --------------------------------------------------------
    tarefa = recuperar_tarefa_por_id(tarefas, id_tarefa)

    # --------------------------------------------------------
    # Aqui tratamos o caso em que a tarefa não foi encontrada.
    #
    # Se tarefa is None, significa que nenhuma tarefa da lista tem
    # o id informado.
    # --------------------------------------------------------
    if tarefa is None:
        return f"Não encontrei nenhuma tarefa com id {id_tarefa}."

    # --------------------------------------------------------
    # Se chegamos aqui, significa que a tarefa foi encontrada.
    #
    # Agora verificamos se ela já estava concluída antes.
    #
    # Isso evita salvar de novo uma tarefa que já estava marcada
    # como feita.
    # --------------------------------------------------------
    if tarefa.get("concluida", False):
        # ----------------------------------------------------
        # Pegamos o título da tarefa para deixar a mensagem mais
        # clara para o usuário.
        # ----------------------------------------------------
        titulo = tarefa.get("titulo", "Sem título")

        # ----------------------------------------------------
        # Devolvemos uma mensagem dizendo que a tarefa já estava
        # concluída.
        # ----------------------------------------------------
        return f"A tarefa [{id_tarefa}] {titulo} já estava concluída."

    # --------------------------------------------------------
    # Agora marcamos a tarefa como concluída.
    #
    # Antes:
    #
    # "concluida": False
    #
    # Depois:
    #
    # "concluida": True
    # --------------------------------------------------------
    tarefa["concluida"] = True

    # --------------------------------------------------------
    # Depois de alterar a tarefa, precisamos salvar a lista inteira
    # de volta no arquivo data/tarefas.json.
    #
    # Se não salvarmos, a alteração será perdida quando o programa
    # terminar.
    # --------------------------------------------------------
    salvar_tarefas(tarefas)

    # --------------------------------------------------------
    # Pegamos o título da tarefa para montar uma mensagem mais
    # amigável.
    # --------------------------------------------------------
    titulo = tarefa.get("titulo", "Sem título")

    # --------------------------------------------------------
    # Por fim, devolvemos uma mensagem de confirmação.
    # --------------------------------------------------------
    return f"Tarefa concluída com sucesso: [{id_tarefa}] {titulo}"

#endregion

#region concluir_tarefa_por_descricao (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: concluir_tarefa_por_descricao
# ------------------------------------------------------------
# Esta função marca uma tarefa como concluída usando uma descrição
# textual fornecida pelo usuário.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será uma candidata a ferramenta no futuro
# tool calling.
#
# Por que esta função é necessária?
#
# Porque o usuário normalmente não vai falar assim:
#
# "concluir tarefa 5"
#
# Ele provavelmente vai falar de forma mais natural, por exemplo:
#
# "conclua a tarefa de terminar o trabalho de ia"
#
# ou:
#
# "terminei aquela tarefa do README"
#
# Então, em vez de exigir que o usuário saiba o id da tarefa, esta
# função recebe uma descrição textual e tenta descobrir qual tarefa
# cadastrada corresponde melhor a essa descrição.
#
# A lógica desta função será:
#
# 1. receber a descrição textual da tarefa;
# 2. carregar todas as tarefas cadastradas;
# 3. verificar se existem tarefas cadastradas;
# 4. pedir para a LLM comparar a descrição com as tarefas existentes;
# 5. verificar se a LLM encontrou uma tarefa clara;
# 6. se encontrou, chamar concluir_tarefa_por_id(id);
# 7. se ficou ambíguo, pedir para o usuário especificar melhor;
# 8. se não encontrou, avisar que nenhuma tarefa correspondente foi encontrada.
#
# Repare que esta função NÃO altera o arquivo diretamente.
#
# Quem altera o arquivo é a função intermediária:
#
# concluir_tarefa_por_id(...)
#
# Isso deixa o código mais organizado:
#
# concluir_tarefa_por_descricao(...)
#   -> entende qual tarefa o usuário quis dizer.
#
# concluir_tarefa_por_id(...)
#   -> altera a tarefa com segurança no arquivo tarefas.json.
# ------------------------------------------------------------
def concluir_tarefa_por_descricao(descricao_tarefa: str) -> str:
    # --------------------------------------------------------
    # O parâmetro "descricao_tarefa" representa o texto usado pelo
    # usuário para descrever a tarefa que deseja concluir.
    #
    # Exemplo:
    #
    # "terminar o trabalho de ia"
    #
    # ou:
    #
    # "fazer README"
    #
    # Essa descrição será comparada com as tarefas cadastradas no
    # arquivo data/tarefas.json.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, verificamos se a descrição veio vazia.
    #
    # Isso pode acontecer se a LLM chamar a ferramenta sem passar
    # corretamente a descrição da tarefa.
    #
    # Exemplo ruim:
    #
    # concluir_tarefa_por_descricao("")
    #
    # Nesse caso, não temos informação suficiente para identificar
    # a tarefa.
    # --------------------------------------------------------
    if not descricao_tarefa:
        return (
            "Para concluir uma tarefa, preciso que você descreva qual tarefa deseja concluir. "
            "Por exemplo: \"concluir a tarefa de terminar o trabalho de IA\"."
        )

    # --------------------------------------------------------
    # Agora carregamos todas as tarefas cadastradas.
    #
    # A função carregar_tarefas() lê o arquivo data/tarefas.json
    # e devolve uma lista de tarefas.
    #
    # Exemplo:
    #
    # [
    #     {
    #         "id": 5,
    #         "titulo": "terminar o trabalho de ia",
    #         "descricao": "",
    #         "concluida": False
    #     }
    # ]
    # --------------------------------------------------------
    tarefas = carregar_tarefas()

    # --------------------------------------------------------
    # Agora verificamos se existe pelo menos uma tarefa cadastrada.
    #
    # Se a lista estiver vazia, não há nada para concluir.
    # --------------------------------------------------------
    if not tarefas:
        return "Você não tem tarefas cadastradas para concluir."

    # --------------------------------------------------------
    # Agora pedimos para a LLM identificar qual tarefa corresponde
    # melhor à descrição fornecida pelo usuário.
    #
    # A função recuperar_decisao_tarefa_por_descricao(...) está no
    # arquivo llm_client.py.
    #
    # Ela recebe:
    #
    # - a descrição textual da tarefa;
    # - a lista de tarefas cadastradas.
    #
    # E devolve uma decisão em formato de dicionário Python.
    #
    # Exemplo de decisão quando encontra uma tarefa:
    #
    # {
    #     "encontrou": True,
    #     "id_tarefa": 5,
    #     "ambigua": False,
    #     "ids_possiveis": [],
    #     "mensagem": "A descrição corresponde à tarefa de id 5."
    # }
    #
    # Exemplo de decisão quando fica ambíguo:
    #
    # {
    #     "encontrou": False,
    #     "id_tarefa": None,
    #     "ambigua": True,
    #     "ids_possiveis": [5, 6],
    #     "mensagem": "Encontrei mais de uma tarefa possível."
    # }
    # --------------------------------------------------------
    decisao = recuperar_decisao_tarefa_por_descricao(
        descricao_tarefa=descricao_tarefa,
        tarefas=tarefas
    )

    # --------------------------------------------------------
    # Agora recuperamos os campos principais da decisão.
    #
    # Usamos .get(...) para evitar erro caso alguma chave não exista.
    # --------------------------------------------------------
    encontrou = decisao.get("encontrou", False)
    id_tarefa = decisao.get("id_tarefa")
    ambigua = decisao.get("ambigua", False)
    ids_possiveis = decisao.get("ids_possiveis", [])
    mensagem = decisao.get("mensagem", "")

    # --------------------------------------------------------
    # Primeiro tratamos o caso de ambiguidade.
    #
    # Ambiguidade significa que a LLM encontrou mais de uma tarefa
    # possível e não conseguiu escolher uma com segurança.
    #
    # Exemplo:
    #
    # [5] terminar o trabalho de ia
    # [6] revisar o trabalho de ia
    #
    # Usuário:
    #
    # "conclua a tarefa do trabalho de ia"
    #
    # Nesse caso, pode não ser seguro escolher automaticamente.
    # Então pedimos para o usuário especificar melhor.
    # --------------------------------------------------------
    if ambigua:
        # ----------------------------------------------------
        # Vamos montar uma resposta amigável para mostrar ao usuário
        # quais tarefas podem ser a tarefa desejada.
        # ----------------------------------------------------
        linhas = []

        linhas.append("Encontrei mais de uma tarefa que pode corresponder ao que você pediu:")
        linhas.append("")

        # ----------------------------------------------------
        # Agora percorremos os ids possíveis sugeridos pela LLM.
        #
        # Para cada id, tentamos recuperar a tarefa correspondente.
        #
        # Assim conseguimos mostrar título e descrição, não apenas
        # o número do id.
        # ----------------------------------------------------
        for id_possivel in ids_possiveis:
            tarefa_possivel = recuperar_tarefa_por_id(tarefas, id_possivel)

            if tarefa_possivel is not None:
                titulo = tarefa_possivel.get("titulo", "Sem título")
                descricao = tarefa_possivel.get("descricao", "")

                linhas.append(f"- [{id_possivel}] {titulo}")

                if descricao:
                    linhas.append(f"  {descricao}")

        # ----------------------------------------------------
        # Depois de listar as possibilidades, pedimos para o usuário
        # especificar melhor.
        # ----------------------------------------------------
        linhas.append("")
        linhas.append("Pode me dizer com mais detalhes qual delas você quer concluir?")

        return "\n".join(linhas)

    # --------------------------------------------------------
    # Agora tratamos o caso em que nenhuma tarefa foi encontrada.
    #
    # Isso significa que a LLM não encontrou uma correspondência
    # clara entre a descrição do usuário e as tarefas cadastradas.
    # --------------------------------------------------------
    if not encontrou:
        # ----------------------------------------------------
        # Se a LLM devolveu uma mensagem explicativa, podemos usar
        # essa mensagem como complemento.
        #
        # Mas mantemos uma resposta principal simples e amigável.
        # ----------------------------------------------------
        if mensagem:
            return (
                "Não encontrei uma tarefa cadastrada que corresponda claramente a essa descrição. "
                f"Detalhe: {mensagem}"
            )

        return "Não encontrei uma tarefa cadastrada que corresponda claramente a essa descrição."

    # --------------------------------------------------------
    # Agora tratamos um caso de segurança.
    #
    # Pode acontecer de a LLM dizer que encontrou uma tarefa, mas
    # não fornecer um id válido.
    #
    # Nesse caso, não podemos concluir nada com segurança.
    # --------------------------------------------------------
    if id_tarefa is None:
        return (
            "Entendi que você quer concluir uma tarefa, mas não consegui identificar com segurança qual é. "
            "Descreva melhor a tarefa ou informe mais detalhes."
        )

    # --------------------------------------------------------
    # Se chegamos aqui, significa que:
    #
    # - não houve ambiguidade;
    # - a LLM encontrou uma tarefa;
    # - existe um id de tarefa identificado.
    #
    # Agora chamamos a função intermediária que realmente marca a
    # tarefa como concluída.
    #
    # Essa função é responsável por:
    #
    # - carregar tarefas;
    # - encontrar a tarefa pelo id;
    # - alterar "concluida" para True;
    # - salvar no arquivo tarefas.json;
    # - devolver mensagem de confirmação.
    # --------------------------------------------------------
    resposta = concluir_tarefa_por_id(id_tarefa)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta da conclusão por id.
    #
    # Exemplo:
    #
    # "Tarefa concluída com sucesso: [5] terminar o trabalho de ia"
    # --------------------------------------------------------
    return resposta

#endregion