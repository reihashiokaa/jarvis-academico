#region explicação do arquivo

# ============================================================
# Arquivo: llm_client.py
# ------------------------------------------------------------
# Este arquivo será responsável por conversar com a LLM.
#
# No nosso trabalho, a LLM obrigatória é o
# Gemma 12B, conforme pedido pelo professor.
#
# A ideia de separar este código em um arquivo próprio é deixar
# o projeto mais organizado:
#
# - o arquivo main.py vai cuidar da interação com o usuário;
# - este arquivo llm_client.py vai cuidar da comunicação com a IA;
# - outros arquivos poderão usar este arquivo sem precisar saber
#   os detalhes da API.
#
# Em resumo:
# este arquivo é como a "ponte" entre o nosso sistema e o Gemma.
# ============================================================
#endregion

#region importações
# ------------------------------------------------------------
# Importamos a biblioteca "os".
#
# A biblioteca os permite acessar informações do ambiente do
# sistema operacional.
#
# No nosso caso, vamos usá-la para pegar valores que estão no
# arquivo .env, como:
#
# - GEMMA_BASE_URL
# - GEMMA_API_KEY
# - GEMMA_MODEL
#
# Esses valores ficam no .env para não precisarmos escrever a
# chave da API diretamente dentro do código.
# ------------------------------------------------------------
import os


# ------------------------------------------------------------
# Importamos a função load_dotenv da biblioteca python-dotenv.
#
# Essa função lê o arquivo .env e carrega as variáveis que estão
# escritas nele.
#
# Sem essa função, o Python não saberia automaticamente o que é:
#
# GEMMA_BASE_URL
# GEMMA_API_KEY
# GEMMA_MODEL
# ------------------------------------------------------------
from dotenv import load_dotenv


# ------------------------------------------------------------
# Importamos o cliente OpenAI.
#
# Mesmo que o nosso modelo seja o Gemma, o professor forneceu uma
# API compatível com o formato da OpenAI.
#
# Isso significa que podemos usar a biblioteca "openai" para
# enviar mensagens ao Gemma.
#
# Pense nesse cliente como uma ferramenta pronta para conversar
# com modelos de linguagem por API.
# ------------------------------------------------------------
from openai import OpenAI, APITimeoutError, APIConnectionError, APIError


# ------------------------------------------------------------
# Importamos a biblioteca json.
#
# Ela será usada para transformar estruturas Python, como listas
# e dicionários, em texto no formato JSON.
#
# Isso será importante quando formos mostrar para a LLM quais
# ferramentas existem no sistema.
#
# Exemplo:
#
# [
#     {
#         "nome": "consultar_tarefas",
#         "descricao": "Use quando o usuário quiser listar tarefas.",
#         "parametros": {}
#     }
# ]
#
# O json.dumps(...) consegue transformar essa estrutura em um texto
# organizado para colocar dentro do prompt enviado ao Gemma.
# ------------------------------------------------------------
import json
#endregion

#region configuração do cliente
# ------------------------------------------------------------
# Aqui carregamos o arquivo .env.
#
# Depois dessa linha, o Python consegue acessar as variáveis que
# estão dentro do .env usando os.getenv().
#
# Exemplo:
#
# os.getenv("GEMMA_API_KEY")
#
# Isso busca o valor da chave GEMMA_API_KEY dentro do .env.
# ------------------------------------------------------------
load_dotenv()


# ------------------------------------------------------------
# Agora vamos criar o cliente que conversa com a API do Gemma.
#
# Pense no "client" como um telefone configurado:
#
# - base_url diz para onde esse telefone vai ligar;
# - api_key é a chave que autoriza essa ligação;
# - depois vamos usar esse client para enviar perguntas ao modelo.
# ------------------------------------------------------------
client = OpenAI(
    # --------------------------------------------------------
    # Aqui buscamos o endereço da API do Gemma.
    #
    # Esse valor vem do arquivo .env.
    #
    # No .env, temos algo como:
    #
    # GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
    #
    # Usar os.getenv evita deixar essa configuração espalhada
    # pelo código.
    # --------------------------------------------------------
    base_url=os.getenv("GEMMA_BASE_URL"),

    # --------------------------------------------------------
    # Aqui buscamos a chave/token de acesso à API.
    #
    # Esse valor também vem do arquivo .env.
    #
    # Isso é importante porque a chave não deve ser colocada
    # diretamente no código-fonte, principalmente porque o código
    # será enviado para o GitHub.
    # --------------------------------------------------------
    api_key=os.getenv("GEMMA_API_KEY"),

    # --------------------------------------------------------
    # Aqui definimos um timeout padrão para as requisições.
    # O timeout é o tempo máximo que o client vai esperar por uma resposta
    # antes de desistir e lançar um erro.
    # Definir um timeout é importante para evitar que o sistema fique travado esperando uma resposta que pode nunca chegar.
    # O valor de 10 segundos é um exemplo, mas pode ser ajustado conforme necessário.
    # ---------------------------------------------------------
    timeout=10
)
#endregion

#region chamar_llm (intermediária, envia mensagem para a LLM e retorna resposta em texto)

# ------------------------------------------------------------
# Função: chamar_llm
# ------------------------------------------------------------
# Esta função envia uma mensagem para a LLM e devolve a resposta
# gerada pelo modelo.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não é uma
# ferramenta chamada diretamente pelo usuário final.
#
# Por que precisamos tratar erros aqui?
#
# Porque a chamada para a LLM depende de conexão com um serviço
# externo.
#
# Às vezes o modelo pode demorar demais, a internet pode oscilar
# ou a API pode falhar temporariamente.
#
# Antes, quando isso acontecia, o programa quebrava e mostrava um
# erro gigante no terminal.
#
# Agora, vamos capturar esses erros e devolver uma mensagem mais
# amigável para o usuário.
# ------------------------------------------------------------
def chamar_llm(mensagem: str) -> str:
    # --------------------------------------------------------
    # O parâmetro "mensagem" representa o texto que será enviado
    # para o modelo.
    #
    # Exemplo:
    #
    # "Explique rapidamente o que é uma LLM."
    #
    # A função vai enviar essa mensagem para o Gemma e devolver
    # o texto da resposta.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Usamos try/except porque chamadas externas podem falhar.
    #
    # O try representa:
    #
    # "tente executar este código normalmente".
    #
    # Se der certo, a resposta da LLM será retornada.
    #
    # Se der erro, o Python pula para algum dos except abaixo.
    # --------------------------------------------------------
    try:
        # ----------------------------------------------------
        # Aqui fazemos a chamada real para o modelo.
        #
        # client.chat.completions.create(...)
        #
        # envia uma conversa para a LLM e pede uma resposta.
        #
        # model=os.getenv("GEMMA_MODEL")
        #
        # pega do arquivo .env o nome do modelo que estamos usando.
        #
        # messages=[...]
        #
        # representa a lista de mensagens enviadas para o modelo.
        #
        # Neste caso, mandamos apenas uma mensagem do usuário.
        # ----------------------------------------------------
        resposta = client.chat.completions.create(
            model=os.getenv("GEMMA_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": mensagem
                }
            ]
        )

        # ----------------------------------------------------
        # A resposta da API vem dentro de uma estrutura maior.
        #
        # Para pegar apenas o texto gerado pelo modelo, usamos:
        #
        # resposta.choices[0].message.content
        #
        # Esse é o texto final que queremos devolver para quem
        # chamou a função.
        # ----------------------------------------------------
        texto_resposta = resposta.choices[0].message.content

        # ----------------------------------------------------
        # Por fim, devolvemos a resposta textual da LLM.
        # ----------------------------------------------------
        return texto_resposta

    except APITimeoutError:
        # ----------------------------------------------------
        # Este erro acontece quando a API demora demais para
        # responder.
        #
        # Foi exatamente o tipo de erro que apareceu no seu teste:
        #
        # Request timed out.
        #
        # Em vez de quebrar o programa, devolvemos uma mensagem
        # amigável.
        # ----------------------------------------------------
        return (
            "O modelo demorou demais para responder e a chamada atingiu o tempo limite. "
            "Tente novamente em alguns instantes."
        )

    except APIConnectionError:
        # ----------------------------------------------------
        # Este erro acontece quando o programa não consegue se
        # conectar corretamente ao serviço da LLM.
        #
        # Pode ser internet, instabilidade do serviço ou problema
        # temporário de conexão.
        # ----------------------------------------------------
        return (
            "Não consegui conectar ao serviço da LLM agora. "
            "Verifique sua internet ou tente novamente em alguns instantes."
        )

    except APIError as erro:
        # ----------------------------------------------------
        # Este erro representa outros problemas vindos da API.
        #
        # Guardamos o erro na variável "erro" para mostrar uma
        # mensagem útil durante o desenvolvimento.
        # ----------------------------------------------------
        return f"Ocorreu um erro na API da LLM: {erro}"

    except Exception as erro:
        # ----------------------------------------------------
        # Este bloco captura qualquer outro erro inesperado.
        #
        # Ele serve como uma proteção final para evitar que o
        # programa quebre sem uma mensagem controlada.
        # ----------------------------------------------------
        return f"Ocorreu um erro inesperado ao chamar a LLM: {erro}"

#endregion

#region decidir_chamada_ferramenta (intermediária, pede para a LLM decidir se deve chamar uma ferramenta)

# ------------------------------------------------------------
# Função: decidir_chamada_ferramenta
# ------------------------------------------------------------
# Esta função pede para a LLM decidir se a mensagem do usuário
# precisa ou não de uma ferramenta.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque o trabalho exige que a decisão de chamada de ferramenta
# seja feita pela LLM, e não apenas por regras fixas no código.
#
# Então, em vez de fazermos algo como:
#
# if "tarefa" in mensagem:
#     chamar consultar_tarefas()
#
# vamos pedir para o Gemma analisar a mensagem do usuário e escolher
# se alguma ferramenta deve ser usada.
#
# Exemplo:
#
# Usuário:
# "Liste minhas tarefas."
#
# A LLM deve responder algo como:
#
# {
#     "usar_ferramenta": true,
#     "nome_ferramenta": "consultar_tarefas",
#     "entrada": {}
# }
#
# Outro exemplo:
#
# Usuário:
# "Adicione uma tarefa para estudar RAG."
#
# A LLM deve responder algo como:
#
# {
#     "usar_ferramenta": true,
#     "nome_ferramenta": "adicionar_tarefa",
#     "entrada": {
#         "titulo": "Estudar RAG",
#         "descricao": ""
#     }
# }
#
# Outro exemplo:
#
# Usuário:
# "Explique brevemente o que é uma LLM."
#
# Se essa pergunta não precisar de uma ferramenta local, a LLM
# pode responder:
#
# {
#     "usar_ferramenta": false,
#     "nome_ferramenta": null,
#     "entrada": {}
# }
#
# Importante:
#
# Esta função ainda NÃO executa a ferramenta.
#
# Ela apenas pede ao Gemma para decidir qual ferramenta deveria
# ser chamada.
#
# A execução real será feita depois pelo tools.py, usando a função:
#
# executar_ferramenta(...)
# ------------------------------------------------------------
def decidir_chamada_ferramenta(mensagem_usuario: str, descricoes_ferramentas: list) -> str:
    # --------------------------------------------------------
    # O parâmetro "mensagem_usuario" representa aquilo que o usuário
    # digitou no chat.
    #
    # Exemplo:
    #
    # "O que tenho hoje?"
    #
    # ou:
    #
    # "Adicione uma tarefa para estudar embeddings."
    #
    # A LLM vai analisar essa mensagem para decidir se precisa
    # chamar alguma ferramenta.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "descricoes_ferramentas" representa a lista de
    # ferramentas disponíveis no sistema.
    #
    # Essa lista vem da função carregar_descricoes_ferramentas(),
    # que criamos no arquivo tools.py.
    #
    # Exemplo de item dessa lista:
    #
    # {
    #     "nome": "consultar_tarefas",
    #     "descricao": "Use quando o usuário quiser listar tarefas.",
    #     "parametros": {}
    # }
    #
    # A LLM precisa receber essas descrições para saber quais
    # ferramentas existem e quando deve usar cada uma.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, transformamos a lista de descrições em texto JSON.
    #
    # Por que fazer isso?
    #
    # Porque a LLM recebe texto no prompt.
    #
    # A lista Python precisa virar um texto organizado para ser
    # incluída na mensagem enviada ao Gemma.
    #
    # json.dumps(...) faz essa transformação.
    #
    # ensure_ascii=False:
    #   mantém acentos corretamente.
    #
    # indent=2:
    #   deixa o JSON mais organizado e mais fácil para a LLM ler.
    # --------------------------------------------------------
    ferramentas_em_json = json.dumps(
        descricoes_ferramentas,
        ensure_ascii=False,
        indent=2
    )

    # --------------------------------------------------------
    # Agora montamos o prompt de decisão.
    #
    # Esse prompt é a instrução que vamos enviar para o Gemma.
    #
    # O objetivo é deixar muito claro que ele deve responder apenas
    # em JSON, porque depois o nosso sistema vai tentar interpretar
    # essa resposta automaticamente.
    #
    # Se o Gemma responder com texto solto, tipo:
    #
    # "Claro, vou consultar suas tarefas"
    #
    # isso fica ruim para o código interpretar.
    #
    # Por isso pedimos uma resposta estruturada.
    # --------------------------------------------------------
    prompt = f"""
Você é o módulo de decisão de ferramentas do JARVIS Acadêmico.

Sua tarefa é analisar a mensagem do usuário e decidir se alguma ferramenta do sistema deve ser chamada.

Ferramentas disponíveis:

{ferramentas_em_json}

Mensagem do usuário:

{mensagem_usuario}

Responda APENAS com um JSON válido, sem explicações fora do JSON.

O JSON deve seguir exatamente este formato:

{{
  "usar_ferramenta": true ou false,
  "nome_ferramenta": "nome_da_ferramenta" ou null,
  "entrada": {{}}
}}

Regras:

1. Se a mensagem do usuário puder ser respondida melhor usando agenda, tarefas ou materiais, use uma ferramenta.

2. Se o usuário quiser ver tarefas, use "consultar_tarefas".

3. Se o usuário quiser adicionar/criar/anotar uma tarefa, use "adicionar_tarefa".

4. Se o usuário quiser concluir, finalizar, marcar como feita ou dizer que terminou uma tarefa, use "concluir_tarefa_por_descricao".

A entrada deve ser:

{{
  "descricao_tarefa": "descrição textual da tarefa mencionada pelo usuário"
}}

Exemplos:

Usuário:
"conclua a tarefa de terminar o trabalho de ia"

Resposta esperada:
{{
  "usar_ferramenta": true,
  "nome_ferramenta": "concluir_tarefa_por_descricao",
  "entrada": {{
    "descricao_tarefa": "terminar o trabalho de ia"
  }}
}}

Usuário:
"terminei o README"

Resposta esperada:
{{
  "usar_ferramenta": true,
  "nome_ferramenta": "concluir_tarefa_por_descricao",
  "entrada": {{
    "descricao_tarefa": "README"
  }}
}}

Usuário:
"conclua a tarefa 5"

Resposta esperada:
{{
  "usar_ferramenta": true,
  "nome_ferramenta": "concluir_tarefa_por_descricao",
  "entrada": {{
    "descricao_tarefa": "tarefa 5"
  }}
}}

5. Se o usuário perguntar o que tem hoje, use "consultar_agenda_hoje".

6. Se o usuário perguntar o que tem amanhã, use "consultar_agenda_amanha".

7. Se o usuário perguntar o que tem na semana atual, use "consultar_agenda_semana_atual".

8. Se o usuário informar uma data específica no formato AAAA-MM-DD, use "consultar_agenda_por_data".

9. Se nenhuma ferramenta for necessária, use:
{{
  "usar_ferramenta": false,
  "nome_ferramenta": null,
  "entrada": {{}}
}}

10. Não invente nomes de ferramentas. Use apenas os nomes listados em Ferramentas disponíveis.

11. A chave "entrada" deve conter exatamente os parâmetros esperados pela ferramenta escolhida.
"""

    # --------------------------------------------------------
    # Agora enviamos o prompt para o Gemma.
    #
    # Como essa chamada depende de um serviço externo, ela pode
    # falhar ou demorar demais.
    #
    # Por isso usamos try/except.
    #
    # Se der certo, devolvemos o texto gerado pela LLM.
    #
    # Se der timeout ou erro de conexão, devolvemos uma decisão
    # segura dizendo que nenhuma ferramenta deve ser usada.
    #
    # Essa decisão segura será devolvida em formato JSON textual,
    # porque esta função normalmente retorna texto.
    #
    # Depois, a função interpretar_decisao_ferramenta(...) vai
    # transformar esse texto em dicionário Python.
    # --------------------------------------------------------
    try:
        resposta = client.chat.completions.create(
            model=os.getenv("GEMMA_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            #trecho para evitar respostas muito criativas, que podem fugir do formato JSON esperado
            temperature=0,
            max_tokens=250
        )

        # ----------------------------------------------------
        # Pegamos o texto da resposta da LLM.
        #
        # Esse texto deve ser um JSON.
        # ----------------------------------------------------
        decisao_texto = resposta.choices[0].message.content

        # ----------------------------------------------------
        # Devolvemos o texto da decisão.
        # ----------------------------------------------------
        return decisao_texto

    except APITimeoutError:
        # ----------------------------------------------------
        # Se a LLM demorou demais para decidir a ferramenta,
        # devolvemos uma decisão segura.
        #
        # Decisão segura:
        #
        # não usar ferramenta.
        #
        # Isso evita que o programa quebre.
        # ----------------------------------------------------
        return json.dumps(
            {
                "usar_ferramenta": False,
                "nome_ferramenta": None,
                "entrada": {}
            },
            ensure_ascii=False
        )

    except APIConnectionError:
        # ----------------------------------------------------
        # Se não conseguimos conectar ao serviço da LLM, também
        # devolvemos uma decisão segura.
        # ----------------------------------------------------
        return json.dumps(
            {
                "usar_ferramenta": False,
                "nome_ferramenta": None,
                "entrada": {}
            },
            ensure_ascii=False
        )

    except APIError:
        # ----------------------------------------------------
        # Se a API respondeu com algum erro, também não tentamos
        # chamar ferramenta.
        # ----------------------------------------------------
        return json.dumps(
            {
                "usar_ferramenta": False,
                "nome_ferramenta": None,
                "entrada": {}
            },
            ensure_ascii=False
        )

    except Exception:
        # ----------------------------------------------------
        # Proteção final para qualquer erro inesperado.
        #
        # Em todos esses casos, é mais seguro não chamar ferramenta
        # do que tentar executar algo incorreto.
        # ----------------------------------------------------
        return json.dumps(
            {
                "usar_ferramenta": False,
                "nome_ferramenta": None,
                "entrada": {}
            },
            ensure_ascii=False
        )

#endregion

#region interpretar_decisao_ferramenta (intermediária, recebe texto da LLM e tenta transformar em dicionário Python)

# ------------------------------------------------------------
# Função: interpretar_decisao_ferramenta
# ------------------------------------------------------------
# Esta função recebe a resposta textual da LLM e tenta transformar
# essa resposta em um dicionário Python.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque a função decidir_chamada_ferramenta(...) pede ao Gemma
# para responder em JSON.
#
# Porém, a resposta vem como texto.
#
# Exemplo de resposta textual:
#
# {
#   "usar_ferramenta": true,
#   "nome_ferramenta": "consultar_tarefas",
#   "entrada": {}
# }
#
# Para o Python usar essa resposta de verdade, precisamos converter
# esse texto em um dicionário.
#
# Para isso, usamos:
#
# json.loads(...)
#
# Se a conversão der certo, teremos algo assim:
#
# {
#     "usar_ferramenta": True,
#     "nome_ferramenta": "consultar_tarefas",
#     "entrada": {}
# }
#
# Repare:
#
# No JSON:
#   true
#   false
#   null
#
# No Python:
#   True
#   False
#   None
#
# Essa conversão é feita automaticamente pelo json.loads().
#
# Também precisamos tratar erros, porque às vezes a LLM pode devolver
# um JSON inválido ou colocar texto extra.
#
# Se a resposta não puder ser interpretada, vamos devolver uma
# decisão segura dizendo que nenhuma ferramenta deve ser usada.
# ------------------------------------------------------------
def interpretar_decisao_ferramenta(decisao_texto: str) -> dict:
    # --------------------------------------------------------
    # O parâmetro "decisao_texto" representa o texto devolvido pela
    # LLM na função decidir_chamada_ferramenta().
    #
    # Esse texto deveria ser um JSON válido.
    #
    # Exemplo:
    #
    # '{"usar_ferramenta": true, "nome_ferramenta": "consultar_tarefas", "entrada": {}}'
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, criamos uma decisão padrão segura.
    #
    # Essa decisão será usada se alguma coisa der errado.
    #
    # Por exemplo:
    #
    # - se a LLM devolver um JSON inválido;
    # - se a LLM devolver texto vazio;
    # - se faltar alguma chave importante;
    # - se o formato não for o esperado.
    #
    # A decisão segura é:
    #
    # não usar ferramenta.
    #
    # Isso evita que o sistema tente executar algo errado.
    # --------------------------------------------------------
    decisao_padrao = {
        "usar_ferramenta": False,
        "nome_ferramenta": None,
        "entrada": {}
    }

    # --------------------------------------------------------
    # Agora verificamos se a resposta veio vazia.
    #
    # Se decisao_texto estiver vazio, None ou algo equivalente,
    # não há nada para interpretar.
    #
    # Nesse caso, devolvemos a decisão padrão.
    # --------------------------------------------------------
    if not decisao_texto:
        return decisao_padrao

    # --------------------------------------------------------
    # Agora limpamos espaços em branco do começo e do final.
    #
    # strip() remove espaços, quebras de linha e tabulações das
    # extremidades do texto.
    #
    # Exemplo:
    #
    # "   texto   " vira "texto"
    # --------------------------------------------------------
    texto_limpo = decisao_texto.strip()

    # --------------------------------------------------------
    # Algumas LLMs podem devolver o JSON dentro de um bloco Markdown.
    #
    # Exemplo:
    #
    # ```json
    # {
    #   "usar_ferramenta": true,
    #   "nome_ferramenta": "consultar_tarefas",
    #   "entrada": {}
    # }
    # ```
    #
    # Isso é ruim para json.loads(), porque os símbolos ``` não
    # fazem parte do JSON.
    #
    # Então vamos remover esses marcadores se eles aparecerem.
    # --------------------------------------------------------
    if texto_limpo.startswith("```"):
        # ----------------------------------------------------
        # Aqui removemos o começo do bloco Markdown.
        #
        # Primeiro removemos ```json, caso exista.
        # Depois removemos ``` simples, caso exista.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.replace("```json", "", 1)
        texto_limpo = texto_limpo.replace("```", "", 1)

        # ----------------------------------------------------
        # Agora removemos o fechamento do bloco Markdown, se ele
        # ainda estiver no final do texto.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.replace("```", "")

        # ----------------------------------------------------
        # Limpamos espaços novamente depois de remover os marcadores.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.strip()

    # --------------------------------------------------------
    # Agora tentamos converter o texto limpo em dicionário Python.
    #
    # Como essa operação pode dar erro se o JSON estiver inválido,
    # usamos try/except.
    # --------------------------------------------------------
    try:
        # ----------------------------------------------------
        # json.loads(texto_limpo) tenta interpretar o texto como JSON.
        #
        # Se o texto for um JSON válido, ele será convertido para
        # estruturas Python.
        #
        # Exemplo:
        #
        # texto:
        # {"usar_ferramenta": true, "nome_ferramenta": "consultar_tarefas", "entrada": {}}
        #
        # vira:
        #
        # {
        #     "usar_ferramenta": True,
        #     "nome_ferramenta": "consultar_tarefas",
        #     "entrada": {}
        # }
        # ----------------------------------------------------
        decisao = json.loads(texto_limpo)

    except json.JSONDecodeError:
        # ----------------------------------------------------
        # Se o texto não for um JSON válido, caímos aqui.
        #
        # Em vez de quebrar o programa, devolvemos a decisão segura:
        #
        # não usar ferramenta.
        # ----------------------------------------------------
        return decisao_padrao

    # --------------------------------------------------------
    # Agora verificamos se o resultado realmente é um dicionário.
    #
    # O formato esperado é:
    #
    # {
    #     "usar_ferramenta": ...,
    #     "nome_ferramenta": ...,
    #     "entrada": ...
    # }
    #
    # Se json.loads() devolver outra coisa, como uma lista ou string,
    # não serve para nosso fluxo.
    # --------------------------------------------------------
    if not isinstance(decisao, dict):
        return decisao_padrao

    # --------------------------------------------------------
    # Agora garantimos que a chave "usar_ferramenta" existe e é um
    # valor booleano.
    #
    # Booleano significa:
    #
    # True ou False.
    #
    # Se a chave não existir ou vier em formato errado, usamos False.
    # --------------------------------------------------------
    usar_ferramenta = decisao.get("usar_ferramenta", False)

    if not isinstance(usar_ferramenta, bool):
        usar_ferramenta = False

    # --------------------------------------------------------
    # Agora recuperamos o nome da ferramenta.
    #
    # Esse valor pode ser:
    #
    # - uma string, como "consultar_tarefas";
    # - None, se nenhuma ferramenta deve ser usada.
    #
    # Se vier outro tipo de dado, vamos transformar em None.
    # --------------------------------------------------------
    nome_ferramenta = decisao.get("nome_ferramenta")

    if nome_ferramenta is not None and not isinstance(nome_ferramenta, str):
        nome_ferramenta = None

    # --------------------------------------------------------
    # Agora recuperamos a entrada da ferramenta.
    #
    # A entrada deve ser um dicionário.
    #
    # Exemplos:
    #
    # {}
    #
    # ou:
    #
    # {
    #     "titulo": "Estudar RAG",
    #     "descricao": ""
    # }
    #
    # Se a entrada vier faltando ou vier em outro formato, usamos
    # um dicionário vazio.
    # --------------------------------------------------------
    entrada = decisao.get("entrada", {})

    if not isinstance(entrada, dict):
        entrada = {}

    # --------------------------------------------------------
    # Agora montamos uma decisão normalizada.
    #
    # Normalizada significa:
    #
    # "mesmo que a LLM tenha devolvido algo meio estranho, vamos
    # devolver para o restante do sistema um formato previsível".
    #
    # Isso deixa o restante do código mais seguro.
    # --------------------------------------------------------
    decisao_normalizada = {
        "usar_ferramenta": usar_ferramenta,
        "nome_ferramenta": nome_ferramenta,
        "entrada": entrada
    }

    # --------------------------------------------------------
    # Por fim, devolvemos a decisão interpretada e normalizada.
    # --------------------------------------------------------
    return decisao_normalizada

#endregion

#region recuperar_decisao_ferramenta (intermediária, pede decisão à LLM e retorna dicionário normalizado)

# ------------------------------------------------------------
# Função: recuperar_decisao_ferramenta
# ------------------------------------------------------------
# Esta função junta duas etapas importantes do fluxo de tool calling.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque, até agora, temos duas funções separadas:
#
# 1. decidir_chamada_ferramenta(...)
#    -> envia a mensagem do usuário para o Gemma;
#    -> pede para a LLM decidir se deve chamar ferramenta;
#    -> recebe uma resposta em texto, idealmente no formato JSON.
#
# 2. interpretar_decisao_ferramenta(...)
#    -> recebe esse texto;
#    -> tenta transformar o texto em um dicionário Python;
#    -> se houver erro, devolve uma decisão segura.
#
# Esta nova função combina essas duas etapas.
#
# Assim, outras partes do sistema poderão chamar apenas:
#
# recuperar_decisao_ferramenta(...)
#
# E já receberão uma decisão pronta para uso.
#
# Exemplo de retorno esperado:
#
# {
#     "usar_ferramenta": True,
#     "nome_ferramenta": "consultar_tarefas",
#     "entrada": {}
# }
#
# Essa função ainda NÃO executa a ferramenta.
#
# Ela apenas recupera a decisão já interpretada.
#
# A execução real continuará sendo responsabilidade do tools.py,
# usando a função executar_ferramenta(...).
# ------------------------------------------------------------
def recuperar_decisao_ferramenta(mensagem_usuario: str, descricoes_ferramentas: list) -> dict:
    # --------------------------------------------------------
    # O parâmetro "mensagem_usuario" representa o texto digitado
    # pelo usuário no chat.
    #
    # Exemplo:
    #
    # "Liste minhas tarefas."
    #
    # ou:
    #
    # "O que tenho hoje?"
    #
    # ou:
    #
    # "Adicione uma tarefa para estudar RAG."
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "descricoes_ferramentas" representa a lista com
    # as descrições das ferramentas disponíveis.
    #
    # Essa lista vem da função carregar_descricoes_ferramentas(),
    # que está no arquivo tools.py.
    #
    # A LLM precisa dessa lista para saber quais ferramentas existem
    # e quando deve usar cada uma.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, pedimos ao Gemma para decidir se alguma ferramenta
    # deve ser usada.
    #
    # A função decidir_chamada_ferramenta(...) devolve uma string.
    #
    # Essa string deveria estar em formato JSON.
    #
    # Exemplo de string devolvida:
    #
    # {
    #   "usar_ferramenta": true,
    #   "nome_ferramenta": "consultar_tarefas",
    #   "entrada": {}
    # }
    # --------------------------------------------------------
    decisao_texto = decidir_chamada_ferramenta(
        mensagem_usuario=mensagem_usuario,
        descricoes_ferramentas=descricoes_ferramentas
    )

    # --------------------------------------------------------
    # Agora interpretamos o texto devolvido pela LLM.
    #
    # A função interpretar_decisao_ferramenta(...) tenta converter
    # o texto JSON em um dicionário Python.
    #
    # Se der certo, recebemos algo como:
    #
    # {
    #     "usar_ferramenta": True,
    #     "nome_ferramenta": "consultar_tarefas",
    #     "entrada": {}
    # }
    #
    # Se der errado, ela devolve uma decisão segura:
    #
    # {
    #     "usar_ferramenta": False,
    #     "nome_ferramenta": None,
    #     "entrada": {}
    # }
    # --------------------------------------------------------
    decisao = interpretar_decisao_ferramenta(decisao_texto)

    # --------------------------------------------------------
    # Por fim, devolvemos a decisão já normalizada.
    #
    # Isso significa que quem chamar esta função não precisa se
    # preocupar em interpretar JSON manualmente.
    #
    # A decisão já vem pronta para o fluxo principal do sistema.
    # --------------------------------------------------------
    return decisao

#endregion

#region decidir_tarefa_por_descricao (intermediária, pede para a LLM identificar uma tarefa a partir de uma descrição)

# ------------------------------------------------------------
# Função: decidir_tarefa_por_descricao
# ------------------------------------------------------------
# Esta função pede para a LLM identificar qual tarefa corresponde
# melhor a uma descrição textual fornecida pelo usuário.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque o usuário normalmente não vai dizer:
#
# "concluir tarefa 5"
#
# Ele provavelmente vai dizer algo como:
#
# "conclua a tarefa de terminar o trabalho de IA"
#
# ou:
#
# "terminei aquela tarefa do README"
#
# Então precisamos comparar a descrição dada pelo usuário com as
# tarefas cadastradas no sistema.
#
# A LLM é útil aqui porque ela consegue comparar textos de forma
# mais flexível do que uma busca simples por palavra exata.
#
# Exemplo:
#
# Descrição do usuário:
# "terminar o trabalho de IA"
#
# Tarefas existentes:
#
# [1] Estudar RAG
# [2] Fazer README
# [5] terminar o trabalho de ia
#
# A LLM deve perceber que a descrição corresponde melhor à tarefa
# de id 5.
#
# Importante:
#
# Esta função ainda NÃO conclui a tarefa.
#
# Ela apenas pede para a LLM identificar qual id parece corresponder
# à descrição.
#
# A conclusão real da tarefa continuará sendo feita pela função
# concluir_tarefa_por_id(...), dentro do arquivo tarefas.py.
# ------------------------------------------------------------
def decidir_tarefa_por_descricao(descricao_tarefa: str, tarefas: list) -> str:
    # --------------------------------------------------------
    # O parâmetro "descricao_tarefa" representa o texto que o
    # usuário usou para descrever a tarefa que quer concluir.
    #
    # Exemplo:
    #
    # "terminar o trabalho de ia"
    #
    # Esse texto será comparado com as tarefas cadastradas.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista de tarefas carregada
    # do arquivo data/tarefas.json.
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
    #
    # Vamos enviar essa lista para a LLM para que ela consiga
    # comparar a descrição do usuário com as tarefas existentes.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Agora transformamos a lista de tarefas em JSON organizado.
    #
    # Por que fazer isso?
    #
    # Porque a LLM recebe texto no prompt.
    #
    # A lista Python precisa virar um texto estruturado para que
    # o Gemma consiga ler claramente os ids, títulos, descrições
    # e status das tarefas.
    #
    # ensure_ascii=False mantém acentos corretamente.
    #
    # indent=2 deixa o JSON mais fácil de ler.
    # --------------------------------------------------------
    tarefas_em_json = json.dumps(
        tarefas,
        ensure_ascii=False,
        indent=2
    )

    # --------------------------------------------------------
    # Agora montamos o prompt que será enviado ao Gemma.
    #
    # O objetivo do prompt é pedir que ele compare:
    #
    # 1. a descrição da tarefa dada pelo usuário;
    # 2. a lista de tarefas cadastradas.
    #
    # E devolva uma decisão em JSON.
    #
    # Pedimos JSON porque o Python vai precisar interpretar essa
    # resposta automaticamente depois.
    # --------------------------------------------------------
    prompt = f"""
Você é o módulo de identificação de tarefas do JARVIS Acadêmico.

Sua tarefa é comparar a descrição dada pelo usuário com a lista de tarefas cadastradas e identificar qual tarefa o usuário provavelmente quer concluir.

Descrição dada pelo usuário:

{descricao_tarefa}

Tarefas cadastradas:

{tarefas_em_json}

Responda APENAS com um JSON válido, sem explicações fora do JSON.

O JSON deve seguir exatamente este formato:

{{
  "encontrou": true ou false,
  "id_tarefa": número_do_id ou null,
  "ambigua": true ou false,
  "ids_possiveis": [],
  "mensagem": "explicação curta da decisão"
}}

Regras:

1. Se existir uma tarefa claramente correspondente à descrição do usuário, use:
{{
  "encontrou": true,
  "id_tarefa": id_da_tarefa,
  "ambigua": false,
  "ids_possiveis": [],
  "mensagem": "A descrição corresponde à tarefa de id X."
}}

2. Se houver mais de uma tarefa parecida e não for seguro escolher uma só, use:
{{
  "encontrou": false,
  "id_tarefa": null,
  "ambigua": true,
  "ids_possiveis": [lista_de_ids_possiveis],
  "mensagem": "Encontrei mais de uma tarefa possível."
}}

3. Se nenhuma tarefa parecer corresponder à descrição, use:
{{
  "encontrou": false,
  "id_tarefa": null,
  "ambigua": false,
  "ids_possiveis": [],
  "mensagem": "Não encontrei tarefa correspondente."
}}

4. Não escolha uma tarefa já concluída, a menos que a descrição do usuário indique claramente essa tarefa.

5. Não invente ids. Use apenas ids que aparecem na lista de tarefas cadastradas.

6. Se a descrição do usuário for vaga demais, marque como ambígua ou não encontrada.
"""

    # --------------------------------------------------------
    # Agora enviamos o prompt para o Gemma.
    #
    # Esta chamada também depende de um serviço externo.
    #
    # Isso significa que ela pode:
    #
    # - demorar demais;
    # - falhar por instabilidade de internet;
    # - falhar por instabilidade da API;
    # - retornar algum erro inesperado.
    #
    # Por isso, também usamos try/except aqui.
    #
    # Se der certo, devolvemos o JSON textual gerado pela LLM.
    #
    # Se der erro, devolvemos uma decisão segura dizendo que
    # nenhuma tarefa foi identificada.
    #
    # Essa decisão segura ainda é devolvida como texto JSON,
    # porque esta função normalmente retorna texto.
    #
    # Depois, a função interpretar_decisao_tarefa_por_descricao(...)
    # transforma esse texto em dicionário Python.
    # --------------------------------------------------------
    try:
        # ----------------------------------------------------
        # Aqui fazemos a chamada real para a LLM.
        #
        # model=os.getenv("GEMMA_MODEL")
        #   pega o nome do modelo definido no arquivo .env.
        #
        # messages=[...]
        #   envia o prompt para o modelo.
        #
        # temperature=0
        #   deixa a resposta mais determinística, ou seja, menos
        #   criativa e mais direta.
        #
        # max_tokens=250
        #   limita o tamanho da resposta.
        #
        # Como queremos apenas um JSON pequeno, não precisamos
        # permitir uma resposta muito grande.
        # ----------------------------------------------------
        resposta = client.chat.completions.create(
            model=os.getenv("GEMMA_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            #trecho para evitar respostas muito criativas, que podem fugir do formato JSON esperado
            temperature=0,
            max_tokens=250
        )

        # ----------------------------------------------------
        # Pegamos o texto da resposta da LLM.
        #
        # Esse texto deve ser um JSON em formato de string.
        # ----------------------------------------------------
        decisao_texto = resposta.choices[0].message.content

        # ----------------------------------------------------
        # Devolvemos a decisão textual.
        # ----------------------------------------------------
        return decisao_texto

    except APITimeoutError:
        # ----------------------------------------------------
        # Este erro acontece quando a LLM demora demais para
        # responder.
        #
        # Nesse caso, não podemos identificar a tarefa com
        # segurança.
        #
        # Então devolvemos uma decisão segura:
        #
        # encontrou = False
        # id_tarefa = None
        # ambigua = False
        #
        # Isso evita que o programa quebre.
        # ----------------------------------------------------
        return json.dumps(
            {
                "encontrou": False,
                "id_tarefa": None,
                "ambigua": False,
                "ids_possiveis": [],
                "mensagem": "A LLM demorou demais para identificar a tarefa."
            },
            ensure_ascii=False
        )

    except APIConnectionError:
        # ----------------------------------------------------
        # Este erro acontece quando o programa não consegue se
        # conectar ao serviço da LLM.
        #
        # Pode ser internet, instabilidade temporária do serviço
        # ou algum problema de conexão.
        # ----------------------------------------------------
        return json.dumps(
            {
                "encontrou": False,
                "id_tarefa": None,
                "ambigua": False,
                "ids_possiveis": [],
                "mensagem": "Não foi possível conectar à LLM para identificar a tarefa."
            },
            ensure_ascii=False
        )

    except APIError:
        # ----------------------------------------------------
        # Este erro representa outros problemas retornados pela API.
        #
        # Por segurança, também devolvemos uma decisão dizendo que
        # a tarefa não foi identificada.
        # ----------------------------------------------------
        return json.dumps(
            {
                "encontrou": False,
                "id_tarefa": None,
                "ambigua": False,
                "ids_possiveis": [],
                "mensagem": "A API da LLM retornou um erro ao identificar a tarefa."
            },
            ensure_ascii=False
        )

    except Exception:
        # ----------------------------------------------------
        # Este bloco captura qualquer outro erro inesperado.
        #
        # É uma proteção final.
        #
        # Melhor devolver uma decisão segura do que deixar o
        # programa quebrar no meio do uso.
        # ----------------------------------------------------
        return json.dumps(
            {
                "encontrou": False,
                "id_tarefa": None,
                "ambigua": False,
                "ids_possiveis": [],
                "mensagem": "Ocorreu um erro inesperado ao identificar a tarefa."
            },
            ensure_ascii=False
        )

#endregion

#region interpretar_decisao_tarefa_por_descricao (intermediária, recebe texto da LLM e tenta transformar em dicionário Python)

# ------------------------------------------------------------
# Função: interpretar_decisao_tarefa_por_descricao
# ------------------------------------------------------------
# Esta função recebe a resposta textual da LLM sobre identificação
# de tarefa e tenta transformar essa resposta em um dicionário
# Python.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque a função decidir_tarefa_por_descricao(...) pede para a LLM
# responder em JSON.
#
# Porém, a resposta da LLM chega como texto.
#
# Exemplo de resposta textual esperada:
#
# {
#   "encontrou": true,
#   "id_tarefa": 5,
#   "ambigua": false,
#   "ids_possiveis": [],
#   "mensagem": "A descrição corresponde à tarefa de id 5."
# }
#
# Para o Python usar essa resposta, precisamos converter esse texto
# para um dicionário Python.
#
# Depois da conversão, teremos algo assim:
#
# {
#     "encontrou": True,
#     "id_tarefa": 5,
#     "ambigua": False,
#     "ids_possiveis": [],
#     "mensagem": "A descrição corresponde à tarefa de id 5."
# }
#
# Repare:
#
# No JSON:
#   true, false, null
#
# No Python:
#   True, False, None
#
# Essa conversão é feita com json.loads(...).
#
# Também vamos tratar erros, porque a LLM pode devolver um JSON
# inválido, texto extra ou algum campo em formato errado.
#
# Se algo der errado, esta função devolve uma decisão segura dizendo
# que não encontrou a tarefa.
# ------------------------------------------------------------
def interpretar_decisao_tarefa_por_descricao(decisao_texto: str) -> dict:
    # --------------------------------------------------------
    # O parâmetro "decisao_texto" representa o texto devolvido
    # pela LLM.
    #
    # Esse texto deveria estar no formato JSON.
    #
    # Exemplo:
    #
    # '{"encontrou": true, "id_tarefa": 5, "ambigua": false, "ids_possiveis": [], "mensagem": "..."}'
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro criamos uma decisão padrão segura.
    #
    # Essa decisão será usada se alguma coisa der errado.
    #
    # Por exemplo:
    #
    # - se a LLM devolver texto vazio;
    # - se a LLM devolver JSON inválido;
    # - se faltar alguma chave importante;
    # - se algum campo vier em formato errado.
    #
    # A decisão segura é:
    #
    # não encontrei uma tarefa correspondente.
    # --------------------------------------------------------
    decisao_padrao = {
        "encontrou": False,
        "id_tarefa": None,
        "ambigua": False,
        "ids_possiveis": [],
        "mensagem": "Não consegui interpretar a identificação da tarefa."
    }

    # --------------------------------------------------------
    # Se a resposta veio vazia, não temos como interpretar nada.
    #
    # Nesse caso, devolvemos a decisão padrão.
    # --------------------------------------------------------
    if not decisao_texto:
        return decisao_padrao

    # --------------------------------------------------------
    # Agora limpamos espaços e quebras de linha no começo e no
    # final do texto.
    #
    # Isso evita erro causado por espaços desnecessários.
    # --------------------------------------------------------
    texto_limpo = decisao_texto.strip()

    # --------------------------------------------------------
    # Às vezes a LLM pode devolver o JSON dentro de um bloco
    # Markdown.
    #
    # Exemplo:
    #
    # ```json
    # {
    #   "encontrou": true,
    #   "id_tarefa": 5,
    #   "ambigua": false,
    #   "ids_possiveis": [],
    #   "mensagem": "..."
    # }
    # ```
    #
    # Esses marcadores ``` atrapalham o json.loads().
    #
    # Então removemos esses marcadores se eles aparecerem.
    # --------------------------------------------------------
    if texto_limpo.startswith("```"):
        # ----------------------------------------------------
        # Remove o marcador inicial ```json, se existir.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.replace("```json", "", 1)

        # ----------------------------------------------------
        # Remove o marcador inicial ``` simples, se existir.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.replace("```", "", 1)

        # ----------------------------------------------------
        # Remove qualquer marcador ``` restante.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.replace("```", "")

        # ----------------------------------------------------
        # Limpa novamente espaços e quebras de linha.
        # ----------------------------------------------------
        texto_limpo = texto_limpo.strip()

    # --------------------------------------------------------
    # Agora tentamos converter o texto limpo em dicionário Python.
    #
    # Se o texto for um JSON válido, json.loads(...) fará a
    # conversão.
    #
    # Se o texto não for um JSON válido, cairá no except.
    # --------------------------------------------------------
    try:
        decisao = json.loads(texto_limpo)

    except json.JSONDecodeError:
        # ----------------------------------------------------
        # Se a LLM devolveu algo que não é JSON válido, devolvemos
        # a decisão segura.
        # ----------------------------------------------------
        return decisao_padrao

    # --------------------------------------------------------
    # Agora verificamos se o resultado realmente é um dicionário.
    #
    # O formato esperado é:
    #
    # {
    #     "encontrou": ...,
    #     "id_tarefa": ...,
    #     "ambigua": ...,
    #     "ids_possiveis": ...,
    #     "mensagem": ...
    # }
    #
    # Se veio lista, texto ou outro tipo, não serve para nosso fluxo.
    # --------------------------------------------------------
    if not isinstance(decisao, dict):
        return decisao_padrao

    # --------------------------------------------------------
    # Agora recuperamos o campo "encontrou".
    #
    # Esse campo deve ser booleano:
    #
    # True  -> a LLM encontrou uma tarefa correspondente.
    # False -> a LLM não encontrou uma tarefa correspondente.
    #
    # Se vier em formato errado, usamos False.
    # --------------------------------------------------------
    encontrou = decisao.get("encontrou", False)

    if not isinstance(encontrou, bool):
        encontrou = False

    # --------------------------------------------------------
    # Agora recuperamos o campo "id_tarefa".
    #
    # Esse campo deve ser:
    #
    # - um número inteiro, se uma tarefa foi encontrada;
    # - None, se nenhuma tarefa foi encontrada.
    #
    # Porém, a LLM pode devolver o id como texto:
    #
    # "5"
    #
    # Então vamos tentar converter para inteiro quando possível.
    # --------------------------------------------------------
    id_tarefa = decisao.get("id_tarefa")

    if id_tarefa is not None:
        try:
            id_tarefa = int(id_tarefa)

        except ValueError:
            # ------------------------------------------------
            # Se não for possível converter para inteiro, o id
            # não é confiável.
            # ------------------------------------------------
            id_tarefa = None
            encontrou = False

        except TypeError:
            # ------------------------------------------------
            # Se veio um tipo estranho, também descartamos o id.
            # ------------------------------------------------
            id_tarefa = None
            encontrou = False

    # --------------------------------------------------------
    # Agora recuperamos o campo "ambigua".
    #
    # Esse campo indica se a LLM encontrou mais de uma tarefa
    # possível e não conseguiu escolher com segurança.
    #
    # Deve ser booleano.
    # --------------------------------------------------------
    ambigua = decisao.get("ambigua", False)

    if not isinstance(ambigua, bool):
        ambigua = False

    # --------------------------------------------------------
    # Agora recuperamos o campo "ids_possiveis".
    #
    # Esse campo deve ser uma lista com ids candidatos quando
    # houver ambiguidade.
    #
    # Exemplo:
    #
    # [5, 6, 7]
    #
    # Se vier em formato errado, usamos lista vazia.
    # --------------------------------------------------------
    ids_possiveis = decisao.get("ids_possiveis", [])

    if not isinstance(ids_possiveis, list):
        ids_possiveis = []

    # --------------------------------------------------------
    # Agora vamos normalizar os ids possíveis.
    #
    # Isso significa tentar transformar cada item da lista em
    # número inteiro.
    #
    # Se algum item não puder virar inteiro, ele será ignorado.
    # --------------------------------------------------------
    ids_possiveis_normalizados = []

    for id_possivel in ids_possiveis:
        try:
            ids_possiveis_normalizados.append(int(id_possivel))

        except ValueError:
            # ------------------------------------------------
            # Se o valor não puder virar inteiro, ignoramos.
            # ------------------------------------------------
            pass

        except TypeError:
            # ------------------------------------------------
            # Se o tipo for inválido, também ignoramos.
            # ------------------------------------------------
            pass

    # --------------------------------------------------------
    # Agora recuperamos a mensagem explicativa da LLM.
    #
    # Essa mensagem deve ser um texto curto.
    #
    # Se vier em formato errado, usamos uma mensagem padrão.
    # --------------------------------------------------------
    mensagem = decisao.get("mensagem", "Decisão de tarefa interpretada.")

    if not isinstance(mensagem, str):
        mensagem = "Decisão de tarefa interpretada."

    # --------------------------------------------------------
    # Agora montamos uma decisão normalizada.
    #
    # Isso garante que o restante do sistema sempre receba o mesmo
    # formato, mesmo que a LLM tenha devolvido algo imperfeito.
    # --------------------------------------------------------
    decisao_normalizada = {
        "encontrou": encontrou,
        "id_tarefa": id_tarefa,
        "ambigua": ambigua,
        "ids_possiveis": ids_possiveis_normalizados,
        "mensagem": mensagem
    }

    # --------------------------------------------------------
    # Por fim, devolvemos a decisão normalizada.
    # --------------------------------------------------------
    return decisao_normalizada

#endregion

#region recuperar_decisao_tarefa_por_descricao (intermediária, pede decisão à LLM e retorna dicionário normalizado)

# ------------------------------------------------------------
# Função: recuperar_decisao_tarefa_por_descricao
# ------------------------------------------------------------
# Esta função junta duas etapas importantes do processo de
# identificação de tarefa por descrição.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque, para concluir uma tarefa usando uma descrição textual,
# precisamos fazer duas coisas:
#
# 1. pedir para a LLM comparar a descrição do usuário com as
#    tarefas cadastradas;
#
# 2. interpretar a resposta da LLM e transformar essa resposta em
#    um dicionário Python seguro.
#
# Antes desta função, essas duas etapas estavam separadas:
#
# decidir_tarefa_por_descricao(...)
#   -> envia a descrição e a lista de tarefas para o Gemma;
#   -> recebe uma resposta textual, idealmente em JSON.
#
# interpretar_decisao_tarefa_por_descricao(...)
#   -> recebe o texto devolvido pelo Gemma;
#   -> tenta converter em dicionário Python;
#   -> normaliza os campos;
#   -> se houver erro, devolve uma decisão segura.
#
# Esta função combina essas duas etapas.
#
# Assim, outras partes do sistema poderão chamar apenas:
#
# recuperar_decisao_tarefa_por_descricao(...)
#
# E já receberão uma decisão pronta para uso.
#
# Exemplo de retorno quando encontra uma tarefa:
#
# {
#     "encontrou": True,
#     "id_tarefa": 5,
#     "ambigua": False,
#     "ids_possiveis": [],
#     "mensagem": "A descrição corresponde à tarefa de id 5."
# }
#
# Exemplo de retorno quando há ambiguidade:
#
# {
#     "encontrou": False,
#     "id_tarefa": None,
#     "ambigua": True,
#     "ids_possiveis": [5, 6],
#     "mensagem": "Encontrei mais de uma tarefa possível."
# }
#
# Exemplo de retorno quando não encontra:
#
# {
#     "encontrou": False,
#     "id_tarefa": None,
#     "ambigua": False,
#     "ids_possiveis": [],
#     "mensagem": "Não encontrei tarefa correspondente."
# }
#
# Importante:
#
# Esta função ainda NÃO conclui a tarefa.
#
# Ela apenas identifica qual tarefa parece corresponder à descrição.
#
# A conclusão real será feita depois no arquivo tarefas.py, chamando
# a função intermediária:
#
# concluir_tarefa_por_id(...)
# ------------------------------------------------------------
def recuperar_decisao_tarefa_por_descricao(descricao_tarefa: str, tarefas: list) -> dict:
    # --------------------------------------------------------
    # O parâmetro "descricao_tarefa" representa a descrição textual
    # informada pelo usuário.
    #
    # Exemplo:
    #
    # "terminar o trabalho de ia"
    #
    # Essa descrição será comparada com a lista de tarefas
    # cadastradas.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "tarefas" representa a lista de tarefas carregada
    # do arquivo data/tarefas.json.
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
    #
    # A LLM vai usar essa lista para tentar descobrir qual tarefa
    # o usuário quis dizer.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, pedimos ao Gemma para decidir qual tarefa parece
    # corresponder à descrição.
    #
    # A função decidir_tarefa_por_descricao(...) devolve texto.
    #
    # Esse texto deveria estar em formato JSON.
    # --------------------------------------------------------
    decisao_texto = decidir_tarefa_por_descricao(
        descricao_tarefa=descricao_tarefa,
        tarefas=tarefas
    )

    # --------------------------------------------------------
    # Agora interpretamos o texto devolvido pela LLM.
    #
    # A função interpretar_decisao_tarefa_por_descricao(...) tenta
    # converter o texto JSON em um dicionário Python.
    #
    # Se a conversão der certo, recebemos uma decisão normalizada.
    #
    # Se der errado, recebemos uma decisão segura indicando que a
    # tarefa não foi identificada.
    # --------------------------------------------------------
    decisao = interpretar_decisao_tarefa_por_descricao(decisao_texto)

    # --------------------------------------------------------
    # Por fim, devolvemos a decisão já interpretada.
    #
    # Quem chamar esta função não precisa lidar diretamente com
    # texto JSON da LLM.
    # --------------------------------------------------------
    return decisao

#endregion