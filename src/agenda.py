#region explicação do arquivo

# ============================================================
# Arquivo: agenda.py
# ------------------------------------------------------------
# Este arquivo será responsável por lidar com a agenda acadêmica
# do JARVIS.
#
# A agenda acadêmica é uma das funcionalidades obrigatórias do
# Trabalho 1.
#
# Ela deve permitir que o usuário faça perguntas como:
#
# - "O que tenho hoje?"
# - "Quais são minhas aulas esta semana?"
# - "Tenho prova amanhã?"
#
# Neste arquivo, vamos criar funções para ler os dados da agenda
# que estarão guardados no arquivo:
#
# data/agenda.json
#
# A lógica geral usada neste arquivo será:
#
# carregar_...
#   -> abre o arquivo e carrega dados gerais.
#
# recuperar_...
#   -> recupera dados específicos, mas ainda em formato bruto.
#
# formatar_...
#   -> transforma dados brutos em texto mais bonito.
#
# consultar_...
#   -> faz o processo completo e devolve resposta pronta.
# ============================================================
#endregion

#region importações
# ------------------------------------------------------------
# Importamos a biblioteca json.
#
# JSON é um formato de dados muito usado para guardar informações
# de forma organizada.
#
# No nosso projeto, a agenda será guardada em um arquivo JSON.
#
# Exemplo de uma agenda em JSON:
#
# [
#     {
#         "titulo": "Aula de Inteligência Artificial",
#         "data": "2026-05-15",
#         "hora": "19:00",
#         "tipo": "aula"
#     }
# ]
#
# A biblioteca json permite que o Python leia esse tipo de arquivo.
# ------------------------------------------------------------
import json

# ------------------------------------------------------------
# Importamos Path da biblioteca pathlib.
#
# O Path ajuda a trabalhar com caminhos de arquivos e pastas.
#
# Em vez de escrever caminhos manualmente como texto comum,
# usamos Path para o código ficar mais organizado e funcionar
# melhor em diferentes sistemas.
#
# Exemplo de caminho:
#
# data/agenda.json
#
# O Path ajuda o Python a encontrar esse arquivo.
# ------------------------------------------------------------
from pathlib import Path

# ------------------------------------------------------------
# Importamos ferramentas da biblioteca datetime.
#
# A biblioteca datetime é usada para trabalhar com datas e horas
# em Python.
#
# No nosso projeto, ela será útil para perguntas como:
#
# - "O que tenho hoje?"
# - "Tenho prova amanhã?"
# - "Quais são minhas aulas esta semana?"
#
# Vamos importar três coisas:
#
# date:
#   representa uma data, como 2026-05-15.
#
# datetime:
#   ajuda a converter textos em datas.
#   Por exemplo, transformar "2026-05-15" em uma data que o
#   Python consegue comparar.
#
# timedelta:
#   representa uma diferença de tempo.
#   Por exemplo, "mais 1 dia" para calcular amanhã.
# ------------------------------------------------------------
from datetime import date, datetime, timedelta
#endregion

#region caminho do arquivo de agenda
# ------------------------------------------------------------
# Aqui definimos o caminho até o arquivo agenda.json.
#
# Vamos entender com calma:
#
# __file__
#   representa o caminho deste arquivo atual, ou seja:
#   src/agenda.py
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
#   Como agenda.py está dentro de src/, subir uma pasta nos leva
#   para a pasta principal do projeto:
#   jarvis-academico/
#
# Depois juntamos:
#   "data" / "agenda.json"
#
# Resultado final:
#   jarvis-academico/data/agenda.json
# ------------------------------------------------------------
CAMINHO_AGENDA = Path(__file__).resolve().parent.parent / "data" / "agenda.json"
#endregion

#region carregar_agenda (intermediária, retorna lista com todos os compromissos)

# ------------------------------------------------------------
# Função: carregar_agenda
# ------------------------------------------------------------
# Esta função lê o arquivo data/agenda.json e devolve o conteúdo
# dele para o restante do programa.
#
# Por enquanto, esse conteúdo será uma lista.
#
# Se a agenda estiver vazia, o arquivo terá:
#
# []
#
# Então esta função devolverá uma lista vazia.
#
# Se a agenda tiver compromissos, ela devolverá uma lista com
# esses compromissos.
# ------------------------------------------------------------
def carregar_agenda():
    # --------------------------------------------------------
    # Aqui abrimos o arquivo agenda.json em modo de leitura.
    #
    # open(...) serve para abrir arquivos.
    #
    # CAMINHO_AGENDA é o caminho até o arquivo que queremos abrir.
    #
    # "r" significa read, ou seja, leitura.
    #
    # encoding="utf-8" ajuda o Python a lidar corretamente com
    # acentos e caracteres especiais da língua portuguesa.
    #
    # O "with" é usado porque ele abre o arquivo, usa o arquivo
    # e depois fecha automaticamente.
    # --------------------------------------------------------
    with open(CAMINHO_AGENDA, "r", encoding="utf-8") as arquivo:
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
        # Se o arquivo contém uma lista de compromissos, o Python
        # transforma isso em uma lista de dicionários.
        # ----------------------------------------------------
        agenda = json.load(arquivo)

    # --------------------------------------------------------
    # Aqui devolvemos a agenda para quem chamou a função.
    #
    # Exemplo:
    #
    # compromissos = carregar_agenda()
    #
    # Depois disso, a variável "compromissos" terá o conteúdo
    # lido de data/agenda.json.
    # --------------------------------------------------------
    return agenda
#endregion

#region recuperar_compromissos_por_data (intermediária, retorna lista de compromissos daquela data)

# ------------------------------------------------------------
# Função: recuperar_compromissos_por_data
# ------------------------------------------------------------
# Esta função serve para recuperar compromissos de uma data
# específica.
#
# Por exemplo:
#
# recuperar_compromissos_por_data("2026-05-15")
#
# A função vai:
#
# 1. carregar todos os compromissos do arquivo agenda.json;
# 2. olhar compromisso por compromisso;
# 3. verificar quais compromissos têm a data desejada;
# 4. devolver apenas os compromissos daquela data.
#
# Esta função é intermediária.
#
# Isso significa que ela ainda não devolve uma resposta final
# bonita para o usuário. Ela devolve uma lista bruta de
# compromissos encontrados.
#
# Isso será útil quando o usuário perguntar coisas como:
#
# - "O que tenho hoje?"
# - "Tenho prova amanhã?"
# - "Quais compromissos tenho em 2026-05-15?"
# ------------------------------------------------------------
def recuperar_compromissos_por_data(data_procurada: str):
    # --------------------------------------------------------
    # O parâmetro "data_procurada" representa a data que queremos
    # consultar na agenda.
    #
    # Estamos usando o formato:
    #
    # ano-mês-dia
    #
    # Exemplo:
    #
    # "2026-05-15"
    #
    # Esse formato é bom porque é organizado, fácil de comparar
    # e muito usado em sistemas.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, carregamos todos os compromissos da agenda.
    #
    # Para isso, usamos a função carregar_agenda(), que já criamos.
    #
    # A variável "agenda" receberá uma lista de compromissos.
    #
    # Exemplo:
    #
    # [
    #     {
    #         "titulo": "Aula de Inteligência Artificial",
    #         "data": "2026-05-15",
    #         "hora": "19:00",
    #         "tipo": "aula",
    #         "descricao": "Aula sobre assistentes inteligentes e uso de LLM."
    #     }
    # ]
    # --------------------------------------------------------
    agenda = carregar_agenda()

    # --------------------------------------------------------
    # Agora criamos uma lista vazia chamada compromissos_encontrados.
    #
    # Essa lista vai guardar somente os compromissos que acontecerem
    # na data que estamos procurando.
    #
    # No começo, ela está vazia porque ainda não verificamos nada.
    # --------------------------------------------------------
    compromissos_encontrados = []

    # --------------------------------------------------------
    # Agora vamos percorrer a agenda.
    #
    # "for compromisso in agenda" significa:
    #
    # para cada compromisso dentro da lista agenda,
    # execute o bloco de código abaixo.
    #
    # Se a agenda tiver 10 compromissos, esse for passa pelos 10.
    # Se tiver 1 compromisso, passa por 1.
    # Se estiver vazia, não passa por nenhum.
    # --------------------------------------------------------
    for compromisso in agenda:
        # ----------------------------------------------------
        # Aqui verificamos se a data do compromisso é igual à
        # data que estamos procurando.
        #
        # compromisso["data"] pega o valor do campo "data" dentro
        # daquele compromisso.
        #
        # Exemplo:
        #
        # compromisso["data"] pode ser "2026-05-15"
        #
        # data_procurada também pode ser "2026-05-15"
        #
        # Se os dois forem iguais, encontramos um compromisso
        # daquela data.
        # ----------------------------------------------------
        if compromisso["data"] == data_procurada:
            # ------------------------------------------------
            # Se a data bateu, adicionamos esse compromisso na
            # lista compromissos_encontrados.
            #
            # append significa "adicionar ao final da lista".
            # ------------------------------------------------
            compromissos_encontrados.append(compromisso)

    # --------------------------------------------------------
    # Depois de verificar todos os compromissos, devolvemos a lista
    # com os compromissos encontrados.
    #
    # Se encontrou algum, a lista terá esses compromissos.
    #
    # Se não encontrou nada, a lista continuará vazia: []
    # --------------------------------------------------------
    return compromissos_encontrados
#endregion

#region formatar_compromissos_por_data (intermediária, recebe uma lista de compromissos e devolve texto formatado)

# ------------------------------------------------------------
# Função: formatar_compromissos_por_data
# ------------------------------------------------------------
# Esta função serve para transformar uma lista de compromissos
# de uma data específica em um texto mais fácil de ler.
#
# Por que precisamos disso?
#
# Porque a função recuperar_compromissos_por_data(...) devolve
# uma lista de dicionários Python.
#
# Exemplo de retorno bruto:
#
# [
#     {
#         "titulo": "Aula de Inteligência Artificial",
#         "data": "2026-05-15",
#         "hora": "19:00",
#         "tipo": "aula",
#         "descricao": "Aula sobre assistentes inteligentes e uso de LLM."
#     }
# ]
#
# Isso é bom para o código, mas não é tão confortável para uma
# pessoa ler.
#
# Então esta função transforma esses dados em uma resposta textual.
# ------------------------------------------------------------
def formatar_compromissos_por_data(compromissos: list, data_consultada: str) -> str:

    # --------------------------------------------------------
    # O parâmetro "compromissos" é a lista de compromissos que
    # queremos transformar em texto.
    #
    # Essa lista pode ter:
    #
    # - zero compromissos;
    # - um compromisso;
    # - vários compromissos.
    #
    # O parâmetro "data_consultada" representa a data pesquisada.
    #
    # Exemplo:
    #
    # data_consultada = "2026-05-15"
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro tratamos o caso em que a lista está vazia.
    #
    # Em Python, uma lista vazia é considerada "falsa" em uma
    # condição.
    #
    # Então:
    #
    # if not compromissos:
    #
    # significa:
    #
    # "se não existem compromissos nessa lista".
    # --------------------------------------------------------
    if not compromissos:
        # ----------------------------------------------------
        # Se não encontramos compromissos, devolvemos uma mensagem
        # simples para o usuário.
        # ----------------------------------------------------
        return f"Você não tem compromissos cadastrados em {data_consultada}."

    # --------------------------------------------------------
    # Se chegamos aqui, significa que existe pelo menos um
    # compromisso na lista.
    #
    # Agora vamos montar uma lista de linhas de texto.
    #
    # Cada item dessa lista será uma linha da resposta final.
    # --------------------------------------------------------
    linhas = []

    # --------------------------------------------------------
    # Aqui adicionamos a primeira linha da resposta.
    #
    # len(compromissos) conta quantos compromissos existem na
    # lista.
    #
    # Exemplo:
    #
    # se a lista tem 1 compromisso, len(compromissos) será 1.
    # se a lista tem 3 compromissos, len(compromissos) será 3.
    # --------------------------------------------------------
    linhas.append(f"Você tem {len(compromissos)} compromisso(s) em {data_consultada}:")

    # --------------------------------------------------------
    # Adicionamos uma linha vazia para deixar a resposta mais
    # confortável visualmente.
    # --------------------------------------------------------
    linhas.append("")

    # --------------------------------------------------------
    # Agora vamos passar por cada compromisso encontrado.
    #
    # Para cada compromisso, vamos pegar:
    #
    # - hora;
    # - título;
    # - tipo;
    # - descrição.
    #
    # Depois vamos montar um texto com essas informações.
    # --------------------------------------------------------
    for compromisso in compromissos:
        # ----------------------------------------------------
        # Aqui pegamos a hora do compromisso.
        #
        # Usamos .get("hora", "sem horário") em vez de
        # compromisso["hora"] porque .get é mais seguro.
        #
        # Se o campo "hora" existir, ele pega o valor.
        # Se o campo "hora" não existir, ele usa "sem horário".
        #
        # Isso evita erro caso algum compromisso esteja incompleto.
        # ----------------------------------------------------
        hora = compromisso.get("hora", "sem horário")

        # ----------------------------------------------------
        # Aqui pegamos o título do compromisso.
        #
        # Se não existir título, usamos "Sem título".
        # ----------------------------------------------------
        titulo = compromisso.get("titulo", "Sem título")

        # ----------------------------------------------------
        # Aqui pegamos o tipo do compromisso.
        #
        # Exemplo de tipo:
        #
        # - aula
        # - prova
        # - trabalho
        # - reunião
        #
        # Se não existir tipo, usamos "sem tipo".
        # ----------------------------------------------------
        tipo = compromisso.get("tipo", "sem tipo")

        # ----------------------------------------------------
        # Aqui pegamos a descrição do compromisso.
        #
        # Se não existir descrição, usamos uma string vazia.
        # String vazia significa simplesmente "sem texto".
        # ----------------------------------------------------
        descricao = compromisso.get("descricao", "")

        # ----------------------------------------------------
        # Agora adicionamos uma linha principal para o compromisso.
        #
        # Exemplo de linha:
        #
        # - 19:00 | Aula de Inteligência Artificial | aula
        #
        # Repare que aqui não colocamos a data em cada linha.
        # Isso acontece porque esta função é usada para uma data
        # específica. Todos os compromissos da lista pertencem ao
        # mesmo dia.
        # ----------------------------------------------------
        linhas.append(f"- {hora} | {titulo} | {tipo}")

        # ----------------------------------------------------
        # Se existir descrição, adicionamos a descrição logo abaixo.
        #
        # O if descricao: verifica se a descrição não está vazia.
        # ----------------------------------------------------
        if descricao:
            linhas.append(f"  {descricao}")

    # --------------------------------------------------------
    # Agora juntamos todas as linhas em um único texto.
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

#region consultar_agenda_por_data (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_agenda_por_data
# ------------------------------------------------------------
# Esta função é uma função mais "completa" e mais fácil de usar.
#
# Ela junta duas etapas que já criamos antes:
#
# 1. recuperar_compromissos_por_data(data_consultada)
#    -> recupera os compromissos daquela data.
#
# 2. formatar_compromissos_por_data(compromissos, data_consultada)
#    -> transforma os compromissos em um texto legível.
#
# Por que essa função é útil?
#
# Porque depois, quando implementarmos tool calling, será melhor
# ter uma ferramenta simples para consultar agenda por data.
#
# Assim, a LLM poderá pedir algo como:
#
# ferramenta: consultar_agenda_por_data
# entrada: {"data": "2026-05-15"}
#
# E essa função devolverá uma resposta pronta para o usuário.
# ------------------------------------------------------------
def consultar_agenda_por_data(data_consultada: str) -> str:
    # --------------------------------------------------------
    # O parâmetro "data_consultada" é a data que queremos buscar
    # na agenda.
    #
    # Vamos usar o formato:
    #
    # "AAAA-MM-DD"
    #
    # Exemplo:
    #
    # "2026-05-15"
    #
    # Esse formato é bom porque evita confusão entre dia e mês.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, usamos a função recuperar_compromissos_por_data().
    #
    # Essa função lê a agenda e devolve somente os compromissos
    # que acontecem na data informada.
    #
    # O resultado será uma lista.
    #
    # Exemplo de lista com compromisso:
    #
    # [
    #     {
    #         "titulo": "Aula de Inteligência Artificial",
    #         "data": "2026-05-15",
    #         "hora": "19:00",
    #         "tipo": "aula",
    #         "descricao": "Aula sobre assistentes inteligentes e uso de LLM."
    #     }
    # ]
    #
    # Exemplo de lista vazia:
    #
    # []
    # --------------------------------------------------------
    compromissos = recuperar_compromissos_por_data(data_consultada)

    # --------------------------------------------------------
    # Depois, usamos a função formatar_compromissos_por_data().
    #
    # Ela recebe a lista de compromissos e transforma em uma
    # mensagem fácil de ler.
    #
    # Se houver compromissos, ela lista os compromissos.
    #
    # Se não houver compromissos, ela informa que não há nada
    # cadastrado naquela data.
    # --------------------------------------------------------
    resposta_formatada = formatar_compromissos_por_data(compromissos, data_consultada)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta formatada.
    #
    # Quem chamar consultar_agenda_por_data(...) receberá um
    # texto pronto.
    # --------------------------------------------------------
    return resposta_formatada
#endregion

#region obter_data_hoje (intermediária, retorna a data de hoje no formato "AAAA-MM-DD")

# ------------------------------------------------------------
# Função: obter_data_hoje
# ------------------------------------------------------------
# Esta função serve para descobrir qual é a data de hoje.
#
# Por que precisamos dela?
#
# Porque o usuário pode perguntar:
#
# "O que tenho hoje?"
#
# Mas o arquivo agenda.json não guarda a palavra "hoje".
# Ele guarda datas no formato:
#
# "AAAA-MM-DD"
#
# Exemplo:
#
# "2026-05-15"
#
# Então precisamos transformar "hoje" em uma data concreta.
#
# Esta função faz exatamente isso:
#
# 1. pega a data atual do computador;
# 2. transforma essa data em texto;
# 3. devolve esse texto no formato compatível com agenda.json.
# ------------------------------------------------------------
def obter_data_hoje() -> str:
    # --------------------------------------------------------
    # date.today() pega a data atual do computador.
    #
    # Exemplo:
    #
    # se hoje for 15 de maio de 2026,
    # date.today() representa:
    #
    # 2026-05-15
    #
    # Neste momento, isso ainda é um objeto de data do Python,
    # não exatamente um texto comum.
    # --------------------------------------------------------
    hoje = date.today()

    # --------------------------------------------------------
    # isoformat() transforma a data em texto no formato ISO.
    #
    # O formato ISO para datas é:
    #
    # AAAA-MM-DD
    #
    # Exemplo:
    #
    # 2026-05-15
    #
    # Esse formato é o mesmo que escolhemos usar no agenda.json.
    # Isso facilita muito a comparação entre datas.
    # --------------------------------------------------------
    hoje_em_texto = hoje.isoformat()

    # --------------------------------------------------------
    # Por fim, devolvemos a data de hoje em formato de texto.
    #
    # Quem chamar esta função receberá algo como:
    #
    # "2026-05-15"
    # --------------------------------------------------------
    return hoje_em_texto
#endregion

#region consultar_agenda_hoje (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_agenda_hoje
# ------------------------------------------------------------
# Esta função serve para consultar os compromissos cadastrados
# para o dia de hoje.
#
# Ela será útil quando o usuário perguntar algo como:
#
# - "O que tenho hoje?"
# - "Quais são meus compromissos de hoje?"
# - "Tenho algo hoje?"
#
# A ideia dela é juntar duas funções que já criamos:
#
# 1. obter_data_hoje()
#    -> descobre qual é a data atual no formato "AAAA-MM-DD".
#
# 2. consultar_agenda_por_data(data_de_hoje)
#    -> procura compromissos nessa data e devolve uma resposta
#       formatada.
#
# Essa função é importante porque deixa o código mais simples
# para o futuro tool calling.
#
# Mais tarde, a LLM poderá escolher a ferramenta:
#
# consultar_agenda_hoje
#
# sem precisar calcular a data manualmente.
# ------------------------------------------------------------
def consultar_agenda_hoje() -> str:
    # --------------------------------------------------------
    # Primeiro, descobrimos qual é a data de hoje.
    #
    # A função obter_data_hoje() devolve uma string no formato:
    #
    # "AAAA-MM-DD"
    #
    # Exemplo:
    #
    # "2026-05-15"
    #
    # Guardamos esse valor na variável "data_de_hoje".
    # --------------------------------------------------------
    data_de_hoje = obter_data_hoje()

    # --------------------------------------------------------
    # Agora usamos a função consultar_agenda_por_data().
    #
    # Essa função recebe uma data e devolve uma resposta textual
    # pronta para o usuário.
    #
    # Então, se data_de_hoje for "2026-05-15", o código abaixo
    # será equivalente a:
    #
    # consultar_agenda_por_data("2026-05-15")
    #
    # Como já temos um compromisso de teste nessa data, esperamos
    # que ela encontre a Aula de Inteligência Artificial.
    # --------------------------------------------------------
    resposta = consultar_agenda_por_data(data_de_hoje)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta.
    #
    # Quem chamar consultar_agenda_hoje() receberá um texto como:
    #
    # "Você tem 1 compromisso(s) em 2026-05-15..."
    # --------------------------------------------------------
    return resposta
#endregion

#region obter_data_amanha (intermediária, retorna a data de amanhã no formato "AAAA-MM-DD")

# ------------------------------------------------------------
# Função: obter_data_amanha
# ------------------------------------------------------------
# Esta função serve para descobrir qual é a data de amanhã.
#
# Por que precisamos dela?
#
# Porque o usuário pode perguntar:
#
# "Tenho prova amanhã?"
#
# Só que o arquivo agenda.json não guarda a palavra "amanhã".
# Ele guarda datas concretas, no formato:
#
# "AAAA-MM-DD"
#
# Exemplo:
#
# "2026-05-16"
#
# Então precisamos transformar a ideia de "amanhã" em uma data
# real que o sistema consiga comparar com as datas da agenda.
# ------------------------------------------------------------
def obter_data_amanha() -> str:
    # --------------------------------------------------------
    # Primeiro, pegamos a data de hoje.
    #
    # date.today() devolve a data atual do computador.
    #
    # Exemplo:
    #
    # se hoje for 2026-05-15,
    # então date.today() representa essa data.
    # --------------------------------------------------------
    hoje = date.today()

    # --------------------------------------------------------
    # Agora somamos 1 dia à data de hoje.
    #
    # timedelta(days=1) representa uma diferença de tempo de
    # exatamente 1 dia.
    #
    # Então:
    #
    # hoje + timedelta(days=1)
    #
    # significa:
    #
    # data de hoje + 1 dia
    #
    # Exemplo:
    #
    # 2026-05-15 + 1 dia = 2026-05-16
    # --------------------------------------------------------
    amanha = hoje + timedelta(days=1)

    # --------------------------------------------------------
    # Agora transformamos a data de amanhã em texto no formato ISO.
    #
    # O formato ISO é:
    #
    # AAAA-MM-DD
    #
    # Esse é o mesmo formato que estamos usando no agenda.json.
    #
    # Isso é importante porque facilita comparar:
    #
    # data do compromisso == data procurada
    # --------------------------------------------------------
    amanha_em_texto = amanha.isoformat()

    # --------------------------------------------------------
    # Por fim, devolvemos a data de amanhã em formato de texto.
    #
    # Quem chamar esta função receberá algo como:
    #
    # "2026-05-16"
    # --------------------------------------------------------
    return amanha_em_texto
#endregion

#region consultar_agenda_amanha (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_agenda_amanha
# ------------------------------------------------------------
# Esta função serve para consultar os compromissos cadastrados
# para o dia de amanhã.
#
# Ela será útil quando o usuário perguntar algo como:
#
# - "O que tenho amanhã?"
# - "Tenho algo amanhã?"
# - "Tenho prova amanhã?"
#
# A ideia dela é juntar duas funções que já criamos:
#
# 1. obter_data_amanha()
#    -> calcula a data de amanhã no formato "AAAA-MM-DD".
#
# 2. consultar_agenda_por_data(data_de_amanha)
#    -> procura compromissos nessa data e devolve uma resposta
#       formatada.
#
# Assim, a função consultar_agenda_amanha() já devolve uma
# resposta pronta para o usuário.
# ------------------------------------------------------------
def consultar_agenda_amanha() -> str:
    # --------------------------------------------------------
    # Primeiro, descobrimos qual é a data de amanhã.
    #
    # A função obter_data_amanha() faz isso para nós.
    #
    # Exemplo:
    #
    # se hoje for "2026-05-15",
    # então obter_data_amanha() devolverá "2026-05-16".
    #
    # Guardamos esse resultado na variável "data_de_amanha".
    # --------------------------------------------------------
    data_de_amanha = obter_data_amanha()

    # --------------------------------------------------------
    # Agora consultamos a agenda usando a data de amanhã.
    #
    # A função consultar_agenda_por_data(...) já sabe:
    #
    # - procurar os compromissos daquela data;
    # - formatar a resposta de um jeito mais legível.
    #
    # Então, se data_de_amanha for "2026-05-16", o código abaixo
    # será equivalente a:
    #
    # consultar_agenda_por_data("2026-05-16")
    # --------------------------------------------------------
    resposta = consultar_agenda_por_data(data_de_amanha)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta pronta.
    #
    # Se houver compromissos amanhã, eles serão listados.
    #
    # Se não houver compromissos amanhã, a resposta dirá que não
    # existem compromissos cadastrados nessa data.
    # --------------------------------------------------------
    return resposta
#endregion

#region obter_datas_da_semana_atual (intermediária, retorna uma lista com as datas da semana atual no formato "AAAA-MM-DD")

# ------------------------------------------------------------
# Função: obter_datas_da_semana_atual
# ------------------------------------------------------------
# Esta função serve para descobrir quais datas fazem parte da
# semana atual.
#
# Por que precisamos dela?
#
# Porque o usuário pode perguntar:
#
# "Quais são minhas aulas esta semana?"
#
# Mas o arquivo agenda.json não guarda a expressão "esta semana".
# Ele guarda datas específicas, como:
#
# "2026-05-15"
#
# Então precisamos transformar "esta semana" em uma lista de datas.
#
# Nesta função, vamos considerar que a semana começa na segunda-feira
# e termina no domingo.
#
# Exemplo:
#
# se hoje for sexta-feira, 2026-05-15,
# a semana atual será:
#
# 2026-05-11 até 2026-05-17
# ------------------------------------------------------------
def obter_datas_da_semana_atual() -> list:
    # --------------------------------------------------------
    # Primeiro, pegamos a data de hoje.
    #
    # date.today() devolve a data atual do computador.
    #
    # Exemplo:
    #
    # se hoje for 2026-05-15,
    # a variável "hoje" representará essa data.
    # --------------------------------------------------------
    hoje = date.today()

    # --------------------------------------------------------
    # Agora precisamos descobrir em qual dia da semana estamos.
    #
    # O método weekday() devolve um número:
    #
    # segunda-feira = 0
    # terça-feira   = 1
    # quarta-feira  = 2
    # quinta-feira  = 3
    # sexta-feira   = 4
    # sábado        = 5
    # domingo       = 6
    #
    # Exemplo:
    #
    # se hoje for sexta-feira, hoje.weekday() será 4.
    # --------------------------------------------------------
    numero_dia_semana = hoje.weekday()

    # --------------------------------------------------------
    # Agora calculamos a segunda-feira da semana atual.
    #
    # Se hoje é sexta-feira, e sexta-feira tem número 4,
    # então precisamos voltar 4 dias para chegar na segunda.
    #
    # Exemplo:
    #
    # 2026-05-15 menos 4 dias = 2026-05-11
    #
    # timedelta(days=numero_dia_semana) representa essa quantidade
    # de dias que vamos subtrair.
    # --------------------------------------------------------
    inicio_da_semana = hoje - timedelta(days=numero_dia_semana)

    # --------------------------------------------------------
    # Agora vamos criar uma lista vazia.
    #
    # Essa lista vai guardar as 7 datas da semana atual.
    # --------------------------------------------------------
    datas_da_semana = []

    # --------------------------------------------------------
    # Agora usamos um for para gerar os 7 dias da semana.
    #
    # range(7) gera os números:
    #
    # 0, 1, 2, 3, 4, 5, 6
    #
    # Cada número representa quantos dias vamos somar à segunda-feira.
    #
    # Exemplo:
    #
    # segunda + 0 dias = segunda
    # segunda + 1 dia  = terça
    # segunda + 2 dias = quarta
    # ...
    # segunda + 6 dias = domingo
    # --------------------------------------------------------
    for quantidade_de_dias in range(7):
        # ----------------------------------------------------
        # Aqui calculamos uma data da semana.
        #
        # Se inicio_da_semana for 2026-05-11:
        #
        # com quantidade_de_dias = 0, data_da_semana = 2026-05-11
        # com quantidade_de_dias = 1, data_da_semana = 2026-05-12
        # com quantidade_de_dias = 2, data_da_semana = 2026-05-13
        #
        # e assim por diante.
        # ----------------------------------------------------
        data_da_semana = inicio_da_semana + timedelta(days=quantidade_de_dias)

        # ----------------------------------------------------
        # Agora transformamos essa data em texto no formato:
        #
        # AAAA-MM-DD
        #
        # Esse é o mesmo formato usado no agenda.json.
        # ----------------------------------------------------
        data_da_semana_em_texto = data_da_semana.isoformat()

        # ----------------------------------------------------
        # Depois colocamos essa data dentro da lista.
        #
        # append significa "adicionar ao final da lista".
        # ----------------------------------------------------
        datas_da_semana.append(data_da_semana_em_texto)

    # --------------------------------------------------------
    # Por fim, devolvemos a lista com as 7 datas da semana.
    #
    # Exemplo de retorno:
    #
    # [
    #     "2026-05-11",
    #     "2026-05-12",
    #     "2026-05-13",
    #     "2026-05-14",
    #     "2026-05-15",
    #     "2026-05-16",
    #     "2026-05-17"
    # ]
    # --------------------------------------------------------
    return datas_da_semana
#endregion

#region recuperar_compromissos_da_semana_atual (intermediária, retorna uma lista de compromissos que acontecem na semana atual)

# ------------------------------------------------------------
# Função: recuperar_compromissos_da_semana_atual
# ------------------------------------------------------------
# Esta função serve para recuperar todos os compromissos cadastrados
# na semana atual.
#
# Por que precisamos dela?
#
# Porque o usuário pode perguntar:
#
# "Quais são minhas aulas esta semana?"
#
# Para responder isso, o sistema precisa:
#
# 1. descobrir quais são as datas da semana atual;
# 2. carregar todos os compromissos da agenda;
# 3. verificar quais compromissos têm data dentro dessa semana;
# 4. devolver apenas os compromissos encontrados.
#
# Esta função é intermediária.
#
# Isso significa que ela ainda não devolve uma resposta final
# bonita para o usuário. Ela devolve uma lista bruta de
# compromissos encontrados na semana.
#
# Nesta função, vamos considerar a semana de segunda-feira até
# domingo, igual fizemos na função obter_datas_da_semana_atual().
# ------------------------------------------------------------
def recuperar_compromissos_da_semana_atual() -> list:
    # --------------------------------------------------------
    # Primeiro, buscamos a lista com as 7 datas da semana atual.
    #
    # A função obter_datas_da_semana_atual() devolve algo assim:
    #
    # [
    #     "2026-05-11",
    #     "2026-05-12",
    #     "2026-05-13",
    #     "2026-05-14",
    #     "2026-05-15",
    #     "2026-05-16",
    #     "2026-05-17"
    # ]
    #
    # Guardamos essa lista na variável "datas_da_semana".
    # --------------------------------------------------------
    datas_da_semana = obter_datas_da_semana_atual()

    # --------------------------------------------------------
    # Agora carregamos todos os compromissos cadastrados no arquivo
    # data/agenda.json.
    #
    # A função carregar_agenda() já faz isso para nós.
    #
    # Ela devolve uma lista com todos os compromissos, mesmo que
    # sejam de datas diferentes.
    # --------------------------------------------------------
    agenda = carregar_agenda()

    # --------------------------------------------------------
    # Agora criamos uma lista vazia.
    #
    # Essa lista vai guardar somente os compromissos que acontecerem
    # dentro da semana atual.
    # --------------------------------------------------------
    compromissos_da_semana = []

    # --------------------------------------------------------
    # Agora vamos percorrer todos os compromissos da agenda.
    #
    # "for compromisso in agenda" significa:
    #
    # para cada compromisso dentro da lista agenda,
    # execute o bloco de código abaixo.
    # --------------------------------------------------------
    for compromisso in agenda:
        # ----------------------------------------------------
        # Aqui pegamos a data do compromisso.
        #
        # Usamos .get("data") em vez de compromisso["data"] porque
        # .get é mais seguro.
        #
        # Se por algum motivo um compromisso não tiver o campo
        # "data", o programa não quebra imediatamente.
        #
        # Nesse caso, compromisso.get("data") devolveria None.
        # ----------------------------------------------------
        data_do_compromisso = compromisso.get("data")

        # ----------------------------------------------------
        # Agora verificamos se a data do compromisso está dentro
        # da lista de datas da semana.
        #
        # A expressão:
        #
        # data_do_compromisso in datas_da_semana
        #
        # significa:
        #
        # "a data deste compromisso está entre as datas da semana?"
        #
        # Se estiver, então esse compromisso pertence à semana atual.
        # ----------------------------------------------------
        if data_do_compromisso in datas_da_semana:
            # ------------------------------------------------
            # Se o compromisso pertence à semana atual, colocamos
            # ele dentro da lista compromissos_da_semana.
            # ------------------------------------------------
            compromissos_da_semana.append(compromisso)

    # --------------------------------------------------------
    # Depois de verificar todos os compromissos, devolvemos a lista
    # de compromissos encontrados na semana atual.
    #
    # Se houver compromissos, a lista terá esses compromissos.
    #
    # Se não houver nenhum compromisso na semana, a lista será [].
    # --------------------------------------------------------
    return compromissos_da_semana
#endregion

#region formatar_compromissos_da_semana (intermediária, recebe uma lista de compromissos e devolve um texto formatado)

# ------------------------------------------------------------
# Função: formatar_compromissos_da_semana
# ------------------------------------------------------------
# Esta função transforma a lista de compromissos da semana em
# um texto mais bonito e mais fácil de entender.
#
# Por que precisamos dela?
#
# A função recuperar_compromissos_da_semana_atual() devolve os
# compromissos em formato de lista de dicionários Python.
#
# Esse formato é bom para o programa, mas não é tão bom para o
# usuário ler diretamente.
#
# Exemplo de formato bruto:
#
# [
#     {
#         "titulo": "Aula de Inteligência Artificial",
#         "data": "2026-05-15",
#         "hora": "19:00",
#         "tipo": "aula",
#         "descricao": "Aula sobre assistentes inteligentes e uso de LLM."
#     }
# ]
#
# Queremos transformar isso em algo parecido com:
#
# Você tem 1 compromisso(s) nesta semana:
#
# - 2026-05-15 às 19:00 | Aula de Inteligência Artificial | aula
#   Aula sobre assistentes inteligentes e uso de LLM.
#
# Assim a resposta fica mais clara para uma pessoa.
# ------------------------------------------------------------
def formatar_compromissos_da_semana(compromissos: list) -> str:
    # --------------------------------------------------------
    # O parâmetro "compromissos" é uma lista.
    #
    # Essa lista pode estar:
    #
    # - vazia, se não houver compromissos na semana;
    # - com um compromisso;
    # - com vários compromissos.
    #
    # Cada compromisso deve ser um dicionário com campos como:
    #
    # - titulo;
    # - data;
    # - hora;
    # - tipo;
    # - descricao.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro tratamos o caso em que a lista está vazia.
    #
    # Em Python, uma lista vazia é considerada "falsa".
    #
    # Então:
    #
    # if not compromissos:
    #
    # significa:
    #
    # "se não existem compromissos dentro dessa lista".
    # --------------------------------------------------------
    if not compromissos:
        # ----------------------------------------------------
        # Se não houver compromissos na semana, devolvemos uma
        # mensagem simples e direta para o usuário.
        # ----------------------------------------------------
        return "Você não tem compromissos cadastrados para esta semana."

    # --------------------------------------------------------
    # Se chegamos aqui, significa que existe pelo menos um
    # compromisso na semana.
    #
    # Antes de montar o texto, vamos ordenar os compromissos.
    #
    # Por que ordenar?
    #
    # Porque o arquivo agenda.json pode não estar organizado.
    # Um compromisso de sexta poderia aparecer antes de um de
    # segunda, por exemplo.
    #
    # A ordenação deixa a resposta mais natural:
    #
    # primeiro os compromissos mais cedo,
    # depois os compromissos mais tarde.
    # --------------------------------------------------------
    compromissos_ordenados = sorted(
        compromissos,

        # ----------------------------------------------------
        # A chave de ordenação diz ao Python como comparar os
        # compromissos.
        #
        # Aqui usamos uma tupla com:
        #
        # 1. data do compromisso;
        # 2. hora do compromisso.
        #
        # Assim, o Python ordena primeiro pela data.
        # Se dois compromissos forem no mesmo dia, ordena pela hora.
        #
        # Usamos .get(...) para evitar erro caso algum campo não
        # exista em algum compromisso.
        # ----------------------------------------------------
        key=lambda compromisso: (
            compromisso.get("data", ""),
            compromisso.get("hora", "")
        )
    )

    # --------------------------------------------------------
    # Agora vamos montar uma lista chamada "linhas".
    #
    # Cada item dessa lista será uma linha do texto final.
    #
    # No final da função, vamos juntar todas essas linhas usando
    # quebra de linha.
    # --------------------------------------------------------
    linhas = []

    # --------------------------------------------------------
    # A primeira linha informa quantos compromissos foram
    # encontrados na semana.
    #
    # len(compromissos_ordenados) conta quantos itens existem na
    # lista.
    # --------------------------------------------------------
    linhas.append(
        f"Você tem {len(compromissos_ordenados)} compromisso(s) nesta semana:"
    )

    # --------------------------------------------------------
    # Adicionamos uma linha vazia só para deixar a resposta mais
    # confortável visualmente.
    # --------------------------------------------------------
    linhas.append("")

    # --------------------------------------------------------
    # Agora passamos por cada compromisso da lista ordenada.
    #
    # Para cada compromisso, vamos pegar os campos principais e
    # montar uma linha de texto.
    # --------------------------------------------------------
    for compromisso in compromissos_ordenados:
        # ----------------------------------------------------
        # Pegamos a data do compromisso.
        #
        # Se o campo "data" não existir, usamos "sem data".
        # ----------------------------------------------------
        data = compromisso.get("data", "sem data")

        # ----------------------------------------------------
        # Pegamos a hora do compromisso.
        #
        # Se o campo "hora" não existir, usamos "sem horário".
        # ----------------------------------------------------
        hora = compromisso.get("hora", "sem horário")

        # ----------------------------------------------------
        # Pegamos o título do compromisso.
        #
        # Se o campo "titulo" não existir, usamos "Sem título".
        # ----------------------------------------------------
        titulo = compromisso.get("titulo", "Sem título")

        # ----------------------------------------------------
        # Pegamos o tipo do compromisso.
        #
        # Exemplos possíveis:
        #
        # - aula;
        # - prova;
        # - trabalho;
        # - reunião.
        #
        # Se o campo "tipo" não existir, usamos "sem tipo".
        # ----------------------------------------------------
        tipo = compromisso.get("tipo", "sem tipo")

        # ----------------------------------------------------
        # Pegamos a descrição do compromisso.
        #
        # Se não existir descrição, usamos uma string vazia.
        # ----------------------------------------------------
        descricao = compromisso.get("descricao", "")

        # ----------------------------------------------------
        # Agora adicionamos a linha principal do compromisso.
        #
        # Exemplo:
        #
        # - 2026-05-15 às 19:00 | Aula de Inteligência Artificial | aula
        # ----------------------------------------------------
        linhas.append(f"- {data} às {hora} | {titulo} | {tipo}")

        # ----------------------------------------------------
        # Se existir uma descrição, colocamos ela na linha abaixo.
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
    # Então "\n".join(linhas) transforma a lista de linhas em
    # um texto final organizado.
    # --------------------------------------------------------
    return "\n".join(linhas)
#endregion

#region consultar_agenda_semana_atual (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_agenda_semana_atual
# ------------------------------------------------------------
# Esta função consulta os compromissos da semana atual e já
# devolve uma resposta formatada para o usuário.
#
# Ela é parecida com as funções:
#
# consultar_agenda_hoje()
# consultar_agenda_amanha()
#
# Só que, em vez de olhar apenas uma data, ela olha a semana
# inteira.
#
# Por que criamos essa função?
#
# Porque, no futuro, quando implementarmos tool calling, será
# muito mais fácil a LLM escolher uma ferramenta com nome direto:
#
# consultar_agenda_semana_atual
#
# Essa função será útil para perguntas como:
#
# - "Quais são minhas aulas esta semana?"
# - "O que tenho esta semana?"
# - "Quais compromissos tenho na semana?"
#
# Internamente, ela usa duas funções que já criamos:
#
# 1. recuperar_compromissos_da_semana_atual()
#    -> recupera os compromissos da semana no arquivo agenda.json.
#
# 2. formatar_compromissos_da_semana(compromissos)
#    -> transforma a lista encontrada em um texto bonito.
# ------------------------------------------------------------
def consultar_agenda_semana_atual() -> str:
    # --------------------------------------------------------
    # Primeiro, recuperamos os compromissos cadastrados na semana
    # atual.
    #
    # Essa função devolve uma lista.
    #
    # Se houver compromissos na semana, a lista terá esses
    # compromissos.
    #
    # Se não houver compromissos, a lista será vazia:
    #
    # []
    # --------------------------------------------------------
    compromissos = recuperar_compromissos_da_semana_atual()

    # --------------------------------------------------------
    # Agora pegamos a lista de compromissos e transformamos em
    # uma resposta textual mais fácil de ler.
    #
    # A função formatar_compromissos_da_semana já sabe lidar com
    # dois casos:
    #
    # 1. lista com compromissos;
    # 2. lista vazia.
    #
    # Então não precisamos repetir essa lógica aqui.
    # --------------------------------------------------------
    resposta = formatar_compromissos_da_semana(compromissos)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta pronta.
    #
    # Quem chamar consultar_agenda_semana_atual() receberá um
    # texto organizado, não uma lista bruta de Python.
    # --------------------------------------------------------
    return resposta
#endregion