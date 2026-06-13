#region explicação do arquivo

# ============================================================
# Arquivo: aprendizado.py
# ------------------------------------------------------------
# Este arquivo é responsável por lidar com as funcionalidades
# voltadas ao aprendizado.
#
# A ideia principal dessas funcionalidades é permitir que o
# assistente gere exercícios com base nos materiais de estudo
# carregados no projeto, como PDFs, textos e anotações.
#
# A lógica geral deste arquivo é:
#
# 1. enviar tema com contexto recuperado a partir das funções
# de RAG, importadas do arquivo rag.py, para a LLM;
# 2. devolver uma lista de exercícios com gabarito baseada
# nos materiais.
#
# A organização das funções segue o padrão usado no projeto:
#
# gerar_...
#   -> gera prompts ou respostas.
#
# consultar_...
#   -> executa o processo completo e devolve uma resposta pronta.
#
# A função final deste arquivo é:
#
# gerar_exercicios(tema, qtde)
#
# Essa função será cadastrada no tools.py como ferramenta
# disponível para tool calling.
# ============================================================
#endregion

#region importações

# ------------------------------------------------------------
# Importamos o módulo json.
# ------------------------------------------------------------
#
# Esse módulo será usado para salvar e carregar a sessão de
# active recall em um arquivo .json.
#
# Por que precisamos disso?
#
# Porque a funcionalidade interativa acontece em dois momentos:
#
# 1. primeiro o sistema faz uma pergunta ao usuário;
# 2. depois o usuário responde.
#
# Entre esses dois momentos, o sistema precisa lembrar:
#
# - qual pergunta foi feita;
# - qual era a resposta esperada;
# - qual tema estava sendo estudado;
# - quais trechos dos materiais foram usados como contexto.
#
# Para guardar essas informações de forma simples, usaremos um
# arquivo JSON dentro da pasta data/.
# ------------------------------------------------------------

import json

# ------------------------------------------------------------
# Importamos a classe Path.
# ------------------------------------------------------------
#
# Path é usado para montar caminhos de arquivos de forma mais
# segura e organizada.
#
# Em vez de escrever caminhos manualmente como:
#
# "data/active_recall.json"
#
# usamos Path para montar o caminho a partir da localização real
# do arquivo Python.
#
# Isso evita problemas quando o projeto é executado em pastas
# diferentes ou em sistemas diferentes.
# ------------------------------------------------------------

from pathlib import Path


# ------------------------------------------------------------
# Importamos a função chamar_llm.
#
# Essa função está no arquivo llm_client.py e é responsável por
# enviar uma mensagem para o Gemma e devolver a resposta textual
# gerada pelo modelo.
#
# No RAG, ela será usada depois que os trechos relevantes forem
# recuperados.
#
# O fluxo será:
#
# pergunta do usuário
#     ↓
# chunks relevantes recuperados
#     ↓
# contexto formatado
#     ↓
# prompt enviado ao Gemma por chamar_llm(...)
#     ↓
# resposta final baseada nos materiais
# ------------------------------------------------------------
from src.llm_client import chamar_llm


# ------------------------------------------------------------
# Importamos as funções recuperar_chunks_relevantes,
# formatar_chunks_recuperados.
#
# Essas funções estão no arquivo rag.py são responsáveis por
# recuperar chunks (trechos) relevantes a partir dos materiais
# disponíveis no projeto e formatar esses chunks recuperados
# tornando-os mais legíveis e organizados.
# ------------------------------------------------------------
from src.rag import recuperar_chunks_relevantes, formatar_chunks_recuperados


#endregion

#region caminho do arquivo de active recall

# ============================================================
# Caminho do arquivo que vai guardar a sessão de active recall.
# ------------------------------------------------------------
#
# O active recall será a funcionalidade interativa de aprendizado.
#
# A ideia é:
#
# 1. o usuário pede para ser testado sobre um tema;
# 2. o sistema recupera trechos relevantes dos materiais;
# 3. o sistema gera uma pergunta;
# 4. o sistema salva essa pergunta e a resposta esperada;
# 5. o usuário responde;
# 6. o sistema lê a pergunta salva;
# 7. o sistema avalia a resposta do usuário.
#
# Para isso, precisamos de um pequeno arquivo de armazenamento.
#
# Esse arquivo será:
#
# data/active_recall.json
#
# Ele ficará dentro da pasta data porque representa dados usados
# durante a execução do sistema.
# ============================================================

CAMINHO_ACTIVE_RECALL = Path(__file__).resolve().parent.parent / "data" / "active_recall.json"

#endregion

#region carregar_sessao_active_recall (intermediária, carrega a pergunta ativa salva)

# ------------------------------------------------------------
# Função: carregar_sessao_active_recall
# ------------------------------------------------------------
#
# Esta função carrega a sessão atual de active recall.
#
# O que é uma sessão de active recall?
#
# É o conjunto de informações sobre a pergunta que o sistema fez
# ao usuário e que ainda está esperando resposta.
#
# Essa sessão pode guardar, por exemplo:
#
# - o tema estudado;
# - a pergunta feita ao usuário;
# - a resposta esperada;
# - o contexto recuperado dos materiais.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque a funcionalidade interativa acontece em dois momentos:
#
# 1. primeiro o sistema faz uma pergunta;
# 2. depois o usuário responde.
#
# Entre esses dois momentos, precisamos carregar a pergunta que
# ficou salva no arquivo data/active_recall.json.
# ------------------------------------------------------------

def carregar_sessao_active_recall() -> dict:

    # --------------------------------------------------------
    # Primeiro, verificamos se o arquivo existe.
    #
    # Se o arquivo ainda não existir, significa que nenhuma
    # pergunta foi iniciada ainda.
    #
    # Nesse caso, devolvemos um dicionário vazio.
    # --------------------------------------------------------

    if not CAMINHO_ACTIVE_RECALL.exists():
        return {}

    # --------------------------------------------------------
    # Se o arquivo existir, abrimos o arquivo para leitura.
    #
    # Usamos encoding="utf-8" para preservar acentos e caracteres
    # especiais corretamente.
    # --------------------------------------------------------

    with open(CAMINHO_ACTIVE_RECALL, "r", encoding="utf-8") as arquivo:

        # ----------------------------------------------------
        # Tentamos carregar o conteúdo do arquivo como JSON.
        #
        # Se o arquivo estiver vazio ou com algum problema de
        # formatação, o json.load pode gerar erro.
        #
        # Por isso usamos try/except.
        # ----------------------------------------------------

        try:
            sessao = json.load(arquivo)

        except json.JSONDecodeError:
            return {}

    # --------------------------------------------------------
    # Depois de carregar, conferimos se o conteúdo é realmente
    # um dicionário.
    #
    # A sessão precisa ser um dicionário porque vamos acessar
    # informações pelo nome, como:
    #
    # sessao["pergunta"]
    # sessao["resposta_esperada"]
    #
    # Se por algum motivo o arquivo tiver outro formato, devolvemos
    # um dicionário vazio por segurança.
    # --------------------------------------------------------

    if not isinstance(sessao, dict):
        return {}

    # --------------------------------------------------------
    # Se tudo deu certo, devolvemos a sessão carregada.
    # --------------------------------------------------------

    return sessao

#endregion

#region salvar_sessao_active_recall (intermediária, salva a pergunta ativa)

# ------------------------------------------------------------
# Função: salvar_sessao_active_recall
# ------------------------------------------------------------
#
# Esta função salva a sessão atual de active recall em um arquivo
# JSON.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos salvar a sessão?
#
# Porque a funcionalidade de active recall é interativa.
#
# Ela não termina em uma única mensagem.
#
# O fluxo é:
#
# 1. o sistema faz uma pergunta ao usuário;
# 2. o usuário lê a pergunta;
# 3. depois o usuário envia uma resposta;
# 4. o sistema precisa lembrar qual pergunta tinha feito;
# 5. o sistema avalia a resposta do usuário.
#
# Para o sistema lembrar da pergunta entre uma mensagem e outra,
# salvamos os dados em data/active_recall.json.
#
# A sessão salva deve ser um dicionário com informações como:
#
# {
#   "tema": "regressão logística",
#   "pergunta": "Qual é o objetivo da regressão logística?",
#   "resposta_esperada": "Estimar a probabilidade de uma classe.",
#   "contexto": "trechos recuperados dos materiais..."
# }
# ------------------------------------------------------------

def salvar_sessao_active_recall(sessao: dict) -> None:

    # --------------------------------------------------------
    # Primeiro, garantimos que a pasta data/ existe.
    #
    # Normalmente ela já existe no projeto, mas essa verificação
    # deixa a função mais segura.
    #
    # parent:
    # -> representa a pasta onde o arquivo ficará.
    #
    # mkdir:
    # -> cria a pasta, caso ela ainda não exista.
    #
    # parents=True:
    # -> permite criar pastas intermediárias, se necessário.
    #
    # exist_ok=True:
    # -> evita erro caso a pasta já exista.
    # --------------------------------------------------------

    CAMINHO_ACTIVE_RECALL.parent.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Agora abrimos o arquivo em modo de escrita.
    #
    # "w":
    # -> modo de escrita.
    #
    # Se o arquivo não existir, ele será criado.
    #
    # Se o arquivo já existir, o conteúdo antigo será substituído
    # pela nova sessão.
    #
    # Isso faz sentido aqui porque teremos apenas uma pergunta
    # ativa por vez.
    # --------------------------------------------------------

    with open(CAMINHO_ACTIVE_RECALL, "w", encoding="utf-8") as arquivo:

        # ----------------------------------------------------
        # Salvamos o dicionário no formato JSON.
        #
        # ensure_ascii=False:
        # -> mantém acentos corretamente.
        #
        # indent=2:
        # -> deixa o arquivo organizado e legível.
        # ----------------------------------------------------

        json.dump(sessao, arquivo, ensure_ascii=False, indent=2)

#endregion

#region limpar_sessao_active_recall (intermediária, remove a pergunta ativa salva)

# ------------------------------------------------------------
# Função: limpar_sessao_active_recall
# ------------------------------------------------------------
#
# Esta função limpa a sessão atual de active recall.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos limpar a sessão?
#
# Porque, depois que o usuário responde uma pergunta e o sistema
# avalia a resposta, aquela pergunta não precisa mais ficar ativa.
#
# Se não limpássemos a sessão, o sistema poderia tentar avaliar
# uma resposta nova usando uma pergunta antiga.
#
# O fluxo será:
#
# 1. o sistema faz uma pergunta;
# 2. a pergunta fica salva;
# 3. o usuário responde;
# 4. o sistema avalia;
# 5. o sistema limpa a pergunta salva.
#
# Assim, uma nova rodada de active recall pode começar depois.
# ------------------------------------------------------------

def limpar_sessao_active_recall() -> None:

    # --------------------------------------------------------
    # Primeiro, verificamos se o arquivo da sessão existe.
    #
    # Se ele existir, significa que há uma pergunta ativa salva.
    # --------------------------------------------------------

    if CAMINHO_ACTIVE_RECALL.exists():

        # ----------------------------------------------------
        # Removemos o arquivo da sessão.
        #
        # unlink():
        # -> apaga o arquivo indicado pelo caminho.
        #
        # Depois disso, quando carregar_sessao_active_recall()
        # for chamada, ela retornará um dicionário vazio.
        # ----------------------------------------------------

        CAMINHO_ACTIVE_RECALL.unlink()

#endregion

#region gerar_pergunta_active_recall_com_contexto (intermediária, gera uma pergunta e resposta esperada com apoio da LLM)

# ------------------------------------------------------------
# Função: gerar_pergunta_active_recall_com_contexto
# ------------------------------------------------------------
#
# Esta função gera uma pergunta de active recall com base em um
# tema e em um contexto recuperado dos materiais.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# O que é active recall?
#
# Active recall é uma estratégia de estudo em que o estudante tenta
# recuperar uma informação da memória, em vez de apenas reler o
# conteúdo.
#
# Em vez de o sistema simplesmente explicar o assunto, ele pergunta
# algo ao usuário.
#
# Exemplo:
#
# Tema:
# "regressão logística"
#
# Pergunta:
# "Qual é o objetivo da regressão logística?"
#
# Resposta esperada:
# "Estimar a probabilidade de uma determinada classe a partir das
# variáveis de entrada."
#
# Por que esta função recebe contexto?
#
# Porque queremos que a pergunta seja baseada nos materiais de
# estudo carregados no projeto, e não apenas no conhecimento geral
# da LLM.
# ------------------------------------------------------------

def gerar_pergunta_active_recall_com_contexto(tema: str, contexto: str) -> str:

    # --------------------------------------------------------
    # Primeiro, verificamos se existe contexto.
    #
    # Se o contexto estiver vazio, significa que o RAG não
    # encontrou trechos relevantes nos materiais.
    #
    # Nesse caso, devolvemos um JSON textual com uma mensagem de
    # erro, para manter o formato esperado pela próxima etapa.
    # --------------------------------------------------------

    if not contexto:
        return json.dumps(
            {
                "pergunta": "",
                "resposta_esperada": "",
                "erro": "Não encontrei trechos relevantes nos materiais para gerar uma pergunta sobre esse tema."
            },
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # Agora montamos o prompt que será enviado para a LLM.
    #
    # O objetivo é pedir que ela gere:
    #
    # 1. uma pergunta;
    # 2. uma resposta esperada.
    #
    # Pedimos uma resposta em JSON porque depois o Python precisa
    # interpretar esse retorno automaticamente.
    #
    # Também pedimos para não usar Markdown nem blocos de código,
    # porque isso atrapalharia o json.loads().
    # --------------------------------------------------------

    prompt = f"""
Você é o JARVIS Acadêmico, um assistente de estudos.

Sua tarefa é criar UMA pergunta de active recall para testar o usuário.

Use como base principalmente os trechos dos materiais de estudo fornecidos abaixo.

Tema escolhido pelo usuário:
{tema}

Trechos recuperados dos materiais:
{contexto}

Responda APENAS com um JSON válido, sem Markdown, sem ``` e sem explicações fora do JSON.

O JSON deve seguir exatamente este formato:

{{
  "pergunta": "texto da pergunta que será feita ao usuário",
  "resposta_esperada": "resposta esperada para avaliar o usuário depois"
}}
"""

    # --------------------------------------------------------
    # Enviamos o prompt para a LLM.
    #
    # A função chamar_llm(...) já cuida da comunicação com a API
    # e devolve a resposta textual gerada pelo modelo.
    # --------------------------------------------------------

    resposta = chamar_llm(prompt)

    # --------------------------------------------------------
    # Por enquanto, devolvemos a resposta em formato de texto.
    #
    # No próximo baby-step, criaremos uma função para interpretar
    # esse texto como JSON.
    # --------------------------------------------------------

    return resposta

#endregion

#region interpretar_pergunta_active_recall (intermediária, transforma a resposta da LLM em dicionário)

# ------------------------------------------------------------
# Função: interpretar_pergunta_active_recall
# ------------------------------------------------------------
#
# Esta função interpreta a resposta textual gerada pela LLM na
# criação da pergunta de active recall.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque a LLM devolve texto.
#
# Mesmo quando pedimos para ela responder em JSON, o retorno ainda
# chega ao Python como uma string.
#
# Exemplo de texto retornado pela LLM:
#
# {
#   "pergunta": "O que é Python?",
#   "resposta_esperada": "Python é uma linguagem de programação."
# }
#
# Para o sistema conseguir acessar:
#
# dados["pergunta"]
# dados["resposta_esperada"]
#
# precisamos converter esse texto para um dicionário Python.
#
# Também precisamos tratar possíveis erros, porque a LLM pode:
#
# - devolver JSON inválido;
# - devolver texto antes ou depois do JSON;
# - devolver um bloco com ```json;
# - esquecer algum campo importante.
# ------------------------------------------------------------

def interpretar_pergunta_active_recall(resposta_llm: str) -> dict:

    # --------------------------------------------------------
    # Primeiro, removemos espaços extras do começo e do fim.
    #
    # Isso ajuda a evitar problemas quando a resposta vem com
    # quebras de linha antes ou depois do JSON.
    # --------------------------------------------------------

    texto = resposta_llm.strip()

    # --------------------------------------------------------
    # Às vezes a LLM pode devolver o JSON dentro de um bloco
    # Markdown, assim:
    #
    # ```json
    # { ... }
    # ```
    #
    # Mesmo tendo pedido para não fazer isso, é mais seguro tratar.
    #
    # Aqui removemos essas marcações caso apareçam.
    # --------------------------------------------------------

    if texto.startswith("```"):
        texto = texto.replace("```json", "")
        texto = texto.replace("```", "")
        texto = texto.strip()

    # --------------------------------------------------------
    # Agora tentamos converter o texto para um dicionário Python.
    #
    # json.loads(...)
    # -> lê uma string em formato JSON e transforma em objeto Python.
    #
    # Se o texto não for um JSON válido, cairá no except.
    # --------------------------------------------------------

    try:
        dados = json.loads(texto)

    except json.JSONDecodeError:
        return {
            "pergunta": "",
            "resposta_esperada": "",
            "erro": "Não foi possível interpretar a pergunta gerada pela LLM.",
            "resposta_original": resposta_llm
        }

    # --------------------------------------------------------
    # Conferimos se o conteúdo convertido é realmente um dicionário.
    #
    # Se não for, não conseguiremos acessar campos como:
    #
    # dados["pergunta"]
    #
    # Então devolvemos uma estrutura de erro.
    # --------------------------------------------------------

    if not isinstance(dados, dict):
        return {
            "pergunta": "",
            "resposta_esperada": "",
            "erro": "A resposta da LLM não veio no formato esperado.",
            "resposta_original": resposta_llm
        }

    # --------------------------------------------------------
    # Se a própria resposta já tiver um campo de erro, repassamos
    # esse erro para quem chamou a função.
    #
    # Isso pode acontecer quando não há contexto suficiente para
    # gerar uma pergunta.
    # --------------------------------------------------------

    if dados.get("erro"):
        return {
            "pergunta": "",
            "resposta_esperada": "",
            "erro": dados.get("erro"),
            "resposta_original": resposta_llm
        }

    # --------------------------------------------------------
    # Recuperamos os campos principais.
    #
    # Usamos get(...) para evitar erro caso algum campo não exista.
    #
    # Também conferimos se os valores são strings antes de aplicar
    # strip().
    # --------------------------------------------------------

    pergunta = dados.get("pergunta", "")
    resposta_esperada = dados.get("resposta_esperada", "")

    if isinstance(pergunta, str):
        pergunta = pergunta.strip()
    else:
        pergunta = ""

    if isinstance(resposta_esperada, str):
        resposta_esperada = resposta_esperada.strip()
    else:
        resposta_esperada = ""

    # --------------------------------------------------------
    # Conferimos se a pergunta e a resposta esperada vieram
    # preenchidas.
    #
    # Se algum desses campos estiver vazio, a funcionalidade não
    # conseguirá continuar corretamente.
    # --------------------------------------------------------

    if not pergunta or not resposta_esperada:
        return {
            "pergunta": "",
            "resposta_esperada": "",
            "erro": "A resposta da LLM não trouxe pergunta e resposta esperada corretamente.",
            "resposta_original": resposta_llm
        }

    # --------------------------------------------------------
    # Se tudo deu certo, devolvemos os dados limpos.
    # --------------------------------------------------------

    return {
        "pergunta": pergunta,
        "resposta_esperada": resposta_esperada,
        "erro": ""
    }

#endregion

#region iniciar_active_recall (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: iniciar_active_recall
# ------------------------------------------------------------
#
# Esta função inicia uma sessão de active recall.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será cadastrada no tools.py como uma
# ferramenta disponível para a LLM.
#
# O objetivo dela é fazer o sistema perguntar algo ao usuário.
#
# Fluxo completo:
#
# 1. o usuário informa um tema;
# 2. o sistema busca trechos relevantes nos materiais usando RAG;
# 3. o sistema monta um contexto com esses trechos;
# 4. o sistema pede para a LLM gerar uma pergunta;
# 5. o sistema interpreta a pergunta gerada;
# 6. o sistema salva a pergunta e a resposta esperada;
# 7. o sistema mostra apenas a pergunta ao usuário.
#
# Repare:
#
# A resposta esperada NÃO é mostrada ao usuário nesse momento.
#
# Ela fica salva internamente para ser usada depois, quando o
# usuário responder.
#
# Isso é o que torna a funcionalidade realmente interativa.
# ------------------------------------------------------------

def iniciar_active_recall(tema: str) -> str:

    # --------------------------------------------------------
    # Primeiro, validamos o tema.
    #
    # Se o usuário não informar tema nenhum, o sistema não tem
    # como saber sobre qual conteúdo deve gerar uma pergunta.
    # --------------------------------------------------------

    if not tema or not tema.strip():
        return "Informe um tema para iniciar o active recall."

    # --------------------------------------------------------
    # Limpamos espaços extras do começo e do fim do tema.
    #
    # Exemplo:
    #
    # "  regressão logística  "
    #
    # vira:
    #
    # "regressão logística"
    # --------------------------------------------------------

    tema = tema.strip()

    # --------------------------------------------------------
    # Recuperamos os chunks mais relevantes sobre o tema.
    #
    # Essa função vem do arquivo rag.py.
    #
    # Ela procura nos materiais de estudo os trechos mais próximos
    # do assunto informado pelo usuário.
    # --------------------------------------------------------

    chunks_relevantes = recuperar_chunks_relevantes(tema)

    # --------------------------------------------------------
    # Formatamos os chunks recuperados.
    #
    # A LLM entende melhor quando os trechos estão organizados
    # em um texto claro.
    # --------------------------------------------------------

    contexto = formatar_chunks_recuperados(chunks_relevantes)

    # --------------------------------------------------------
    # Pedimos para a LLM gerar uma pergunta e uma resposta esperada
    # usando o tema e o contexto recuperado.
    #
    # Essa função devolve um texto, idealmente em formato JSON.
    # --------------------------------------------------------

    resposta_llm = gerar_pergunta_active_recall_com_contexto(tema, contexto)

    # --------------------------------------------------------
    # Interpretamos a resposta da LLM.
    #
    # Aqui transformamos o texto retornado pela LLM em um dicionário
    # Python com:
    #
    # - pergunta;
    # - resposta_esperada;
    # - erro.
    # --------------------------------------------------------

    dados_pergunta = interpretar_pergunta_active_recall(resposta_llm)

    # --------------------------------------------------------
    # Se houve erro na geração ou interpretação da pergunta,
    # interrompemos o fluxo e devolvemos a mensagem de erro.
    # --------------------------------------------------------

    if dados_pergunta.get("erro"):
        return dados_pergunta["erro"]

    # --------------------------------------------------------
    # Montamos a sessão de active recall.
    #
    # Essa sessão guarda tudo que será necessário depois para
    # avaliar a resposta do usuário.
    #
    # O usuário verá apenas a pergunta.
    #
    # Mas internamente o sistema guarda também:
    #
    # - o tema;
    # - a resposta esperada;
    # - o contexto usado para gerar a pergunta.
    # --------------------------------------------------------

    sessao = {
        "tema": tema,
        "pergunta": dados_pergunta["pergunta"],
        "resposta_esperada": dados_pergunta["resposta_esperada"],
        "contexto": contexto
    }

    # --------------------------------------------------------
    # Salvamos a sessão no arquivo data/active_recall.json.
    #
    # Assim, quando o usuário responder na próxima mensagem, o
    # sistema conseguirá recuperar a pergunta feita.
    # --------------------------------------------------------

    salvar_sessao_active_recall(sessao)

    # --------------------------------------------------------
    # Por fim, devolvemos a pergunta para o usuário.
    #
    # Também orientamos o usuário a responder usando "resposta:".
    #
    # Isso vai ajudar depois a LLM a entender que a próxima mensagem
    # deve ser avaliada pela ferramenta responder_active_recall.
    # --------------------------------------------------------

    return (
        "Vamos treinar active recall.\n\n"
        f"Tema: {tema}\n\n"
        f"Pergunta:\n{dados_pergunta['pergunta']}\n\n"
        "Responda usando o formato:\n"
        "resposta: sua resposta aqui"
    )

#endregion

#region avaliar_resposta_active_recall_com_contexto (intermediária, avalia a resposta do usuário com apoio da LLM)

# ------------------------------------------------------------
# Função: avaliar_resposta_active_recall_com_contexto
# ------------------------------------------------------------
#
# Esta função avalia a resposta do usuário em uma sessão de
# active recall.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# O que ela recebe?
#
# - a pergunta feita ao usuário;
# - a resposta esperada;
# - a resposta que o usuário enviou;
# - o contexto usado para gerar a pergunta.
#
# Por que usamos a LLM para avaliar?
#
# Porque a resposta do usuário pode estar correta mesmo usando
# palavras diferentes da resposta esperada.
#
# Exemplo:
#
# Resposta esperada:
# "Python é uma linguagem de programação."
#
# Resposta do usuário:
# "É uma linguagem usada para programar."
#
# A comparação exata de texto diria que são diferentes.
#
# Mas semanticamente a resposta está correta.
#
# A LLM ajuda a avaliar esse significado.
# ------------------------------------------------------------

def avaliar_resposta_active_recall_com_contexto(
    pergunta: str,
    resposta_esperada: str,
    resposta_usuario: str,
    contexto: str
) -> str:

    # --------------------------------------------------------
    # Primeiro, verificamos se o usuário enviou alguma resposta.
    #
    # Se a resposta estiver vazia, não há o que avaliar.
    # --------------------------------------------------------

    if not resposta_usuario or not resposta_usuario.strip():
        return "Envie uma resposta para que eu possa avaliar."

    # --------------------------------------------------------
    # Limpamos espaços extras da resposta do usuário.
    # --------------------------------------------------------

    resposta_usuario = resposta_usuario.strip()

    # --------------------------------------------------------
    # Montamos o prompt de avaliação.
    #
    # Neste prompt, a LLM recebe:
    #
    # 1. o contexto dos materiais;
    # 2. a pergunta feita;
    # 3. a resposta esperada;
    # 4. a resposta do usuário.
    #
    # A tarefa da LLM não é responder a pergunta de novo.
    #
    # A tarefa dela é avaliar se a resposta do usuário está:
    #
    # - correta;
    # - parcialmente correta;
    # - incorreta.
    # --------------------------------------------------------

    prompt = f"""
Você é o JARVIS Acadêmico, um assistente de estudos.

Sua tarefa é avaliar a resposta do usuário em uma atividade de active recall.

Use como referência principalmente o contexto e a resposta esperada.

Contexto dos materiais:
{contexto}

Pergunta feita ao usuário:
{pergunta}

Resposta esperada:
{resposta_esperada}

Resposta do usuário:
{resposta_usuario}

Avalie a resposta do usuário de forma didática.

Responda neste formato:

Classificação: correta, parcialmente correta ou incorreta.

Feedback:
Explique de forma curta o que o usuário acertou e/ou errou.

Resposta ideal:
Mostre uma resposta melhor ou mais completa.

Sugestão de revisão:
Diga o que o usuário deveria revisar, se necessário.
"""

    # --------------------------------------------------------
    # Enviamos o prompt para a LLM e retornamos o feedback gerado.
    # --------------------------------------------------------

    avaliacao = chamar_llm(prompt)

    return avaliacao

#endregion

#region responder_active_recall (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: responder_active_recall
# ------------------------------------------------------------
#
# Esta função recebe a resposta do usuário para uma pergunta de
# active recall e devolve uma avaliação.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será cadastrada no tools.py como uma
# ferramenta disponível para a LLM.
#
# Ela completa a funcionalidade interativa exigida no trabalho.
#
# Fluxo completo:
#
# 1. o sistema já fez uma pergunta antes;
# 2. a pergunta ficou salva em data/active_recall.json;
# 3. o usuário envia uma resposta;
# 4. esta função carrega a pergunta salva;
# 5. a resposta do usuário é comparada com a resposta esperada;
# 6. o sistema devolve feedback;
# 7. a sessão é limpa.
#
# Por que limpamos a sessão no final?
#
# Porque, depois que a resposta foi avaliada, aquela pergunta já
# foi encerrada.
#
# Se o usuário quiser continuar estudando, ele pode iniciar uma
# nova pergunta de active recall.
# ------------------------------------------------------------

def responder_active_recall(resposta_usuario: str) -> str:

    # --------------------------------------------------------
    # Primeiro, carregamos a sessão ativa.
    #
    # Essa sessão deve ter sido criada anteriormente pela função
    # iniciar_active_recall(...).
    # --------------------------------------------------------

    sessao = carregar_sessao_active_recall()

    # --------------------------------------------------------
    # Se não existir sessão ativa, significa que o usuário tentou
    # responder sem que o sistema tivesse feito uma pergunta antes.
    # --------------------------------------------------------

    if not sessao:
        return (
            "Não há nenhuma pergunta de active recall ativa no momento.\n\n"
            "Para começar, peça algo como:\n"
            "me faça uma pergunta sobre Inteligência Artificial"
        )

    # --------------------------------------------------------
    # Validamos a resposta do usuário.
    #
    # Se a resposta estiver vazia, não avaliamos e também não
    # limpamos a sessão.
    #
    # Assim, o usuário ainda pode responder a pergunta depois.
    # --------------------------------------------------------

    if not resposta_usuario or not resposta_usuario.strip():
        return "Envie uma resposta para que eu possa avaliar."

    # --------------------------------------------------------
    # Limpamos espaços extras da resposta.
    # --------------------------------------------------------

    resposta_usuario = resposta_usuario.strip()

    # --------------------------------------------------------
    # Como orientamos o usuário a responder usando:
    #
    # resposta: texto da resposta
    #
    # aqui removemos esse prefixo, caso ele apareça.
    #
    # Assim, a avaliação recebe apenas o conteúdo da resposta.
    # --------------------------------------------------------

    if resposta_usuario.lower().startswith("resposta:"):
        resposta_usuario = resposta_usuario.split(":", 1)[1].strip()

    # --------------------------------------------------------
    # Depois de remover o prefixo, conferimos novamente se ainda
    # existe algum conteúdo para avaliar.
    # --------------------------------------------------------

    if not resposta_usuario:
        return "Escreva sua resposta depois de 'resposta:'."

    # --------------------------------------------------------
    # Recuperamos os dados salvos na sessão.
    #
    # Usamos get(...) para evitar erro caso algum campo esteja
    # ausente no arquivo.
    # --------------------------------------------------------

    tema = sessao.get("tema", "")
    pergunta = sessao.get("pergunta", "")
    resposta_esperada = sessao.get("resposta_esperada", "")
    contexto = sessao.get("contexto", "")

    # --------------------------------------------------------
    # Conferimos se a sessão possui os dados mínimos necessários.
    #
    # Para avaliar, precisamos pelo menos da pergunta e da resposta
    # esperada.
    #
    # Se a sessão estiver incompleta, limpamos o arquivo para evitar
    # que o sistema fique preso em uma sessão quebrada.
    # --------------------------------------------------------

    if not pergunta or not resposta_esperada:
        limpar_sessao_active_recall()

        return (
            "A sessão de active recall estava incompleta e foi encerrada.\n\n"
            "Por favor, inicie uma nova pergunta."
        )

    # --------------------------------------------------------
    # Agora avaliamos a resposta do usuário.
    #
    # Para isso, usamos a função intermediária criada no passo
    # anterior.
    # --------------------------------------------------------

    avaliacao = avaliar_resposta_active_recall_com_contexto(
        pergunta=pergunta,
        resposta_esperada=resposta_esperada,
        resposta_usuario=resposta_usuario,
        contexto=contexto
    )

    # --------------------------------------------------------
    # Depois da avaliação, limpamos a sessão.
    #
    # Isso encerra a pergunta atual.
    # --------------------------------------------------------

    limpar_sessao_active_recall()

    # --------------------------------------------------------
    # Por fim, devolvemos um texto organizado para o usuário.
    # --------------------------------------------------------

    return (
        "Avaliação da sua resposta\n\n"
        f"Tema: {tema}\n\n"
        f"Pergunta:\n{pergunta}\n\n"
        f"Sua resposta:\n{resposta_usuario}\n\n"
        f"{avaliacao}"
    )

#endregion

#region gerar_exercicios_com_contexto (intermediária, envia o tema e contexto para a LLM e retorna a resposta)

# ------------------------------------------------------------
# Função: gerar_exercicios_com_contexto
# ------------------------------------------------------------
# Esta função recebe o tema decidido pelo usuário e o contexto
# recuperado dos materiais.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque não devemos simplesmente mandar a solicitação do usuário
# solta para a LLM.
#
# Ele deve mandar:
#
# 1. o tema do usuário;
# 2. os trechos relevantes recuperados dos documentos;
# 3. a quantidade de exercícios que deverão ser gerados;
# 4. uma instrução dizendo para gerar exercícios com base nesses
# trechos.
#
# Assim, os exercícios gerados ficam orientados pelos materiais de estudo,
# e não apenas pelo conhecimento geral do modelo.
# ------------------------------------------------------------
def gerar_exercicios_com_contexto(tema:str, contexto:str, qtde):
    # --------------------------------------------------------
    # Primeiro, verificamos se existe contexto.
    #
    # Se contexto estiver vazio, significa que nenhum trecho relevante
    # foi recuperado dos materiais.
    #
    # Nesse caso, não vale a pena chamar a LLM, porque ela não teria
    # material de apoio para responder.
    # --------------------------------------------------------
    if not contexto:
        return (
            "Não encontrei trechos relevantes nos materiais para gerar exercícios sobre esse tema."
        )
    
    prompt = f"""
    Você é o JARVIS Acadêmico, um assistente de estudos.

    Gere exercícios com resposta para estudo, usando como referência apenas ou principalmente os trechos fornecidos abaixo.
    A quantidade de exercícios será definida pelo usuário. Se não for específicado nenhuma quantidade, gere no mínimo cinco (5) exercícios.

    Trechos recuperados dos materiais:

    {contexto}

    Tema (conteúdo) pedido pelo usuário:

    {tema}

    Quantidade de exercícios:

    {qtde}
    """

    # --------------------------------------------------------
    # Agora enviamos o prompt para o Gemma.
    #
    # A função chamar_llm(...) já cuida da chamada ao modelo e
    # também já tem tratamento para timeout, conexão e erros da API.
    # --------------------------------------------------------
    resposta = chamar_llm(prompt)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta gerada pela LLM.
    # --------------------------------------------------------
    return resposta
#endregion

#region gerar_exercicios (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: gerar_exercicios
# ------------------------------------------------------------
# Esta função executa o processo completo para gerar exercícios.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será cadastrada depois no tools.py como
# uma ferramenta disponível para a LLM.
#
# Ela faz o fluxo completo:
#
# 1. recebe o tema do usuário;
# 2. recupera os chunks mais relevantes;
# 3. formata esses chunks como contexto;
# 4. envia tema + contexto + qtde para o Gemma;
# 5. recebe os exercícios gerados;
# 6. devolve a resposta final para o usuário.
# ------------------------------------------------------------
def gerar_exercicios(tema: str, qtde:int=None):
    # --------------------------------------------------------
    # Recupera os chunks (trechos) releventas sobre o tema a
    # partir dos materiais de estudo.
    # --------------------------------------------------------
    chunks_relevantes = recuperar_chunks_relevantes(tema)

    # --------------------------------------------------------
    # Formata os chunks recuperados, de forma que fique organizado
    # e estruturado em uma única string.
    # --------------------------------------------------------
    contexto = formatar_chunks_recuperados(chunks_relevantes)

    # --------------------------------------------------------
    # Gera os exercícios com base no tema solicitado pelo usuário,
    # no contexto recuperado e com base na quantidade solicitada.
    # --------------------------------------------------------
    resposta = gerar_exercicios_com_contexto(tema, contexto, qtde)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta gerada pela LLM.
    # --------------------------------------------------------
    return resposta
#endregion