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
from openai import OpenAI


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
    api_key=os.getenv("GEMMA_API_KEY")
)




##FUNÇÃO PARA CHAMAR A LLM E PEGAR A RESPOSTA, QUE VAI SER USADA PELO MAIN.PY

# ------------------------------------------------------------
# Função: chamar_llm
# ------------------------------------------------------------
# Esta função é responsável por enviar uma mensagem para a LLM
# e devolver a resposta gerada pelo modelo.
#
# - ela recebe uma entrada;
# - processa essa entrada;
# - devolve uma saída.
#
# Neste caso:
#
# Entrada:
#   mensagem -> texto digitado pelo usuário
#
# Saída:
#   resposta_texto -> texto respondido pelo Gemma
# ------------------------------------------------------------
def chamar_llm(mensagem: str) -> str:
    # --------------------------------------------------------
    # O parâmetro "mensagem" representa o texto que o usuário
    # digitou no chat.
    #
    # Exemplo:
    #
    # mensagem = "Explique o que é regressão logística"
    #
    # O ": str" significa que esperamos receber uma string,
    # ou seja, um texto.
    #
    # O "-> str" indica que esta função deve devolver uma string
    # como resposta.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Aqui fazemos a chamada para a API da LLM.
    #
    # O método client.chat.completions.create(...) envia uma
    # conversa para o modelo e pede que ele gere uma resposta.
    #
    # Essa estrutura segue o formato de chat:
    #
    # - temos uma lista de mensagens;
    # - cada mensagem tem um papel, chamado "role";
    # - cada mensagem tem um conteúdo, chamado "content".
    # --------------------------------------------------------
    resposta = client.chat.completions.create(
        # ----------------------------------------------------
        # Aqui informamos qual modelo queremos usar.
        #
        # O nome do modelo está guardado no arquivo .env:
        #
        # GEMMA_MODEL=google/gemma-3-12b-it
        #
        # Usamos os.getenv("GEMMA_MODEL") para buscar esse valor
        # sem escrever diretamente no código.
        # ----------------------------------------------------
        model=os.getenv("GEMMA_MODEL"),

        # ----------------------------------------------------
        # Aqui montamos a lista de mensagens da conversa.
        #
        # Por enquanto, teremos apenas uma mensagem:
        # a mensagem do usuário.
        #
        # O role "user" significa que essa mensagem veio do
        # usuário humano.
        #
        # O content recebe o texto da variável "mensagem".
        # ----------------------------------------------------
        messages=[
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )

    # --------------------------------------------------------
    # A resposta da API vem em uma estrutura com várias partes.
    #
    # Para pegar o texto principal gerado pela LLM, usamos:
    #
    # resposta.choices[0].message.content
    #
    # Explicando aos poucos:
    #
    # resposta
    #   é o objeto inteiro retornado pela API.
    #
    # choices[0]
    #   pega a primeira resposta gerada pelo modelo.
    #
    # message.content
    #   pega o conteúdo textual dessa resposta.
    # --------------------------------------------------------
    resposta_texto = resposta.choices[0].message.content

    # --------------------------------------------------------
    # Por fim, devolvemos o texto da resposta para quem chamou
    # esta função.
    #
    # Ou seja, se outro arquivo fizer:
    #
    # resposta = chamar_llm("Olá")
    #
    # a variável "resposta" receberá o texto gerado pelo Gemma.
    # --------------------------------------------------------
    return resposta_texto

