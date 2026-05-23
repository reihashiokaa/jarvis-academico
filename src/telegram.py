#region descrição do arquivo
# ============================================================
# Arquivo: telegram.py
# ------------------------------------------------------------
# Este arquivo será responsável por gerenciar a comunicação
# entre o usuário e o bot do Telegram.
#
# Ele define a função assíncrona que processa as mensagens
# recebidas, decide se deve utilizar alguma ferramenta
# específica ou encaminhar a mensagem para um modelo de
# linguagem (LLM), e então retorna a resposta ao usuário.
# ============================================================
#endregion

#region importações
# ------------------------------------------------------------
# Importamos a função chamar_llm.
#
# Essa função envia uma mensagem diretamente para o Gemma e recebe
# uma resposta textual.
#
# Ela será usada quando a mensagem do usuário NÃO precisar chamar
# nenhuma ferramenta.
#
# Exemplo:
#
# Usuário:
# "Explique rapidamente o que é uma LLM."
#
# Nesse caso, o sistema pode responder diretamente com a LLM, sem
# consultar agenda, tarefas ou materiais.
# ------------------------------------------------------------
from src.llm_client import chamar_llm


# ------------------------------------------------------------
# Importamos a função recuperar_decisao_ferramenta.
#
# Essa função pede ao Gemma para decidir se a mensagem do usuário
# precisa chamar alguma ferramenta.
#
# Ela devolve um dicionário Python no formato:
#
# {
#     "usar_ferramenta": True,
#     "nome_ferramenta": "consultar_tarefas",
#     "entrada": {}
# }
#
# Essa decisão será usada no fluxo principal do chat.
# ------------------------------------------------------------
from src.llm_client import recuperar_decisao_ferramenta


# ------------------------------------------------------------
# Importamos a função carregar_descricoes_ferramentas.
#
# Essa função retorna a lista de ferramentas disponíveis no sistema,
# com nome, descrição e parâmetros.
#
# O Gemma precisa receber essas descrições para saber quais
# ferramentas ele pode escolher.
# ------------------------------------------------------------
from src.tools import carregar_descricoes_ferramentas


# ------------------------------------------------------------
# Importamos a função executar_ferramenta.
#
# Essa função recebe:
#
# - nome da ferramenta;
# - entrada da ferramenta.
#
# Depois ela:
#
# - recupera a função Python correta;
# - executa essa função;
# - registra o log;
# - devolve a saída.
# ------------------------------------------------------------
from src.tools import executar_ferramenta


# ------------------------------------------------------------
# Importamos a biblioteca "os".
#
# A biblioteca os permite acessar informações do ambiente do
# sistema operacional.
#
# No nosso caso, vamos usá-la para pegar valores que estão no
# arquivo .env, como:
#
# - TOKEN_TELEGRAM
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
# TOKEN_TELEGRAM
# ------------------------------------------------------------
from dotenv import load_dotenv


# ------------------------------------------------------------
# Importamos a classe Update da biblioteca telegram.
#
# Essa classe representa qualquer nova interação que chega do
# do Telegram, seja ela uma mensagem, um clique em botão ou um
# comando.
# ------------------------------------------------------------
from telegram import Update


# ------------------------------------------------------------
# Importamos algumas classes do submódulo telegram.ext.
#
# A classe Application é o núcleo da execução do bot. Ela é a
# responsável por inicializar e gerenciar o ciclo de vida dele.
# A partir dela é possível receber atualizações do Telegram
# e encaminhar essas atualizações para os handlers apropriados.
#
# A classe ContextTypes define quais os tipos de contexto serão
# utilizados dentro do bot. Ela serve para configurar e padronizar
# o objeto context que é passado para os handlers. É esse objeto
# que contém os dados do bot, dados do usuário, dados do chat
# e as utilidades.
# ------------------------------------------------------------
from telegram.ext import Application, ContextTypes
#endregion

#region configuração do bot
# ------------------------------------------------------------
# Aqui carregamos o arquivo .env.
#
# Depois dessa linha, o Python consegue acessar as variáveis que
# estão dentro do .env usando os.getenv().
#
# Exemplo:
#
# os.getenv("TOKEN_TELEGRAM")
#
# Isso busca o valor da chave TOKEN_TELEGRAM dentro do .env.
# ------------------------------------------------------------
load_dotenv()


# ------------------------------------------------------------
# Agora configuramos o objeto principal do bot.
#
#  - Application.builder() cria um construtor configurável para
#  iniciar a configuração.
#
#  - os.getenv("TOKEN_TELEGRAM") busca a variável de ambiente
#  chamada "TOKEN_TELEGRAM", retornando o token como uma string.
#
#  - .token() passa o token para o construtor (builder), indicando
#  que esse bot vai utilizar esse token para se autenticar no
#  Telegram.
#
#  - build() constrói o objeto final Application. Internamente
#  ele inicializa a conexão com a API do Telegram, o sistema
#  de handlers, event loop (mecanismo que fica rodando
#  continuamente, esperando eventos acontecerem e executando
#  tarefas quando necessário) e a fila de updates.
#
# Por fim, atribui o objeto criado à variável application, que
# será utilizada para configurar os handlers e iniciar/controlar
# o bot.
# ------------------------------------------------------------
application = Application.builder().token(os.getenv("TOKEN_TELEGRAM")).build()
#endregion

#region função gerenciar_comunicacao

# ------------------------------------------------------------
# Função: gerenciar_comunicacao
# ------------------------------------------------------------
# Esta função é responsável por:
#
# - receber mensagens do usuário enviadas do Telegram;
# - enviar essas mensagens para a LLM;
# - receber a resposta da LLM e enviar para o Telegram;
# - encerrar o programa quando o usuário digitar "sair".
# ------------------------------------------------------------
async def gerenciar_comunicacao(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # --------------------------------------------------------
    # Agora carregamos as descrições das ferramentas disponíveis.
    #
    # Essas descrições serão enviadas para o Gemma sempre que ele
    # precisar decidir se deve chamar alguma ferramenta.
    #
    # Exemplos de ferramentas descritas:
    #
    # - consultar_tarefas;
    # - adicionar_tarefa;
    # - concluir_tarefa;
    # - consultar_agenda_hoje;
    # - consultar_agenda_amanha.
    #
    # Carregamos isso uma vez antes do loop porque a lista de
    # ferramentas não muda enquanto o programa está rodando.
    # --------------------------------------------------------
    descricoes_ferramentas = carregar_descricoes_ferramentas()

    # --------------------------------------------------------
    # Aqui pegamos a mensagem enviada pelo usuário no Telegram.
    # 
    #  - update é o objeto Update, representa o evento recebido.
    #
    #  - .message acessa a mensagem enviada pelo usuário,
    #  no qual só existe se o evento for realmente uma mensagem.
    #
    #  - .text retorna o conteúdo textual da mensagem.
    # --------------------------------------------------------
    mensagem = update.message.text

    # ----------------------------------------------------
    # Aqui verificamos se o usuário quer sair do programa.
    #
    # mensagem.lower() transforma o texto em letras minúsculas.
    #
    # Isso permite que o programa entenda:
    #
    # sair
    # SAIR
    # Sair
    # sAiR
    #
    # como a mesma coisa.
    # ----------------------------------------------------
    if mensagem.lower() == "sair":
        # ------------------------------------------------
        # Se o usuário digitou "sair", mostramos uma mensagem
        # de encerramento.
        #
        # update.message é o objeto que representa a mensagem.
        #
        # .reply_text() é o método que envia uma mensagem de
        # volta para o mesmo chat como uma resposta direta
        # à mensagem recebida.
        #
        # É importante ressaltar a utilização do await, já
        # que reply_text() é uma função assíncrona (async),
        # ou seja, sua execução envolve operações que não são
        # imediatas. O await garante que a execução aguarde
        # corretamente a conclusão dessa tarefa sem bloquear
        # o restante do programa, permitindo que o event loop
        # continue processando outras operações simultaneamente.
        # ------------------------------------------------
        await update.message.reply_text("Até mais!")

        # ------------------------------------------------
        # Após mostar a mensagem de encerramento, fazemos
        # com que o Application encerre o loop principal e
        # finalize o programa.
        #
        # context é o objeto de contexto (ContextTypes.DEFAULT_TYPE)
        # que o handler recebe. É nele que se encontram
        # várias informações úteis, como o acesso ao bot
        # e à aplicação.
        #
        # context.application acessa a instância da classe
        # Application, que é o mesmo objeto foi criado
        # com Application.builder na região de configuração
        # do bot.
        #
        # .stop_running() interrompe o event loop do bot,
        # fazendo com que o run_polling pare, assim iniciando
        # o processo de encerramento.
        # ------------------------------------------------
        context.application.stop_running()
    
    # ----------------------------------------------------
    # Caso contrário, o usuário não quiser sair, continuamos
    # a execução do programa.
    # ----------------------------------------------------
    else:
        # ----------------------------------------------------
        # Agora vamos pedir para a LLM decidir se esta mensagem
        # precisa chamar alguma ferramenta.
        #
        # Exemplos:
        #
        # "Liste minhas tarefas."
        #   -> deve usar a ferramenta consultar_tarefas.
        #
        # "O que tenho hoje?"
        #   -> deve usar a ferramenta consultar_agenda_hoje.
        #
        # "Explique rapidamente o que é uma LLM."
        #   -> talvez não precise de ferramenta.
        #
        # A função recuperar_decisao_ferramenta(...) devolve um
        # dicionário Python com a decisão da LLM.
        #
        # Exemplo:
        #
        # {
        #     "usar_ferramenta": True,
        #     "nome_ferramenta": "consultar_tarefas",
        #     "entrada": {}
        # }
        # ----------------------------------------------------
        decisao = recuperar_decisao_ferramenta(
            mensagem_usuario=mensagem,
            descricoes_ferramentas=descricoes_ferramentas
        )

        # ----------------------------------------------------
        # Agora verificamos se a LLM decidiu usar uma ferramenta.
        #
        # decisao.get("usar_ferramenta", False)
        #
        # significa:
        #
        # pegue o valor da chave "usar_ferramenta".
        #
        # Se essa chave não existir por algum motivo, use False
        # como valor padrão.
        # ----------------------------------------------------
        if decisao.get("usar_ferramenta", False):
            # ------------------------------------------------
            # Se chegamos aqui, significa que a LLM decidiu que
            # alguma ferramenta deve ser chamada.
            #
            # Agora recuperamos o nome da ferramenta escolhida.
            #
            # Exemplo:
            #
            # "consultar_tarefas"
            # ------------------------------------------------
            nome_ferramenta = decisao.get("nome_ferramenta")

            # ------------------------------------------------
            # Agora recuperamos a entrada que será enviada para a
            # ferramenta.
            #
            # Exemplo para consultar_tarefas:
            #
            # {}
            #
            # Exemplo para adicionar_tarefa:
            #
            # {
            #     "titulo": "Estudar RAG",
            #     "descricao": ""
            # }
            # ------------------------------------------------
            entrada = decisao.get("entrada", {})

            # ------------------------------------------------
            # Agora executamos a ferramenta escolhida.
            #
            # A função executar_ferramenta(...) faz várias coisas:
            #
            # 1. encontra a função Python correta;
            # 2. executa essa função com a entrada recebida;
            # 3. registra a chamada no log;
            # 4. devolve a saída da ferramenta.
            # ------------------------------------------------
            resposta = executar_ferramenta(
                nome_ferramenta=nome_ferramenta,
                entrada=entrada
            )

            # ------------------------------------------------
            # Mostramos ao usuário a resposta devolvida pela
            # ferramenta.
            #
            # update.message é o objeto que representa a mensagem.
            #
            # .reply_text() é o método que envia uma mensagem de
            # volta para o mesmo chat como uma resposta direta
            # à mensagem recebida.
            #
            # É importante ressaltar a utilização do await, já
            # que reply_text() é uma função assíncrona (async),
            # ou seja, sua execução envolve operações que não são
            # imediatas. O await garante que a execução aguarde
            # corretamente a conclusão dessa tarefa sem bloquear
            # o restante do programa, permitindo que o event loop
            # continue processando outras operações simultaneamente.
            # ------------------------------------------------
            await update.message.reply_text(resposta)

        else:
            # ------------------------------------------------
            # Se chegamos aqui, significa que a LLM decidiu que
            # nenhuma ferramenta é necessária.
            #
            # Então usamos o comportamento antigo:
            # mandamos a mensagem diretamente para o Gemma gerar
            # uma resposta normal.
            # ------------------------------------------------
            resposta = chamar_llm(mensagem)

            # ------------------------------------------------
            # Mostramos a resposta normal da LLM no Telegram.

            # update.message é o objeto que representa a mensagem.
            #
            # .reply_text() é o método que envia uma mensagem de
            # volta para o mesmo chat como uma resposta direta
            # à mensagem recebida.
            #
            # É importante ressaltar a utilização do await, já
            # que reply_text() é uma função assíncrona (async),
            # ou seja, sua execução envolve operações que não são
            # imediatas. O await garante que a execução aguarde
            # corretamente a conclusão dessa tarefa sem bloquear
            # o restante do programa, permitindo que o event loop
            # continue processando outras operações simultaneamente.
            # ------------------------------------------------
            await update.message.reply_text(resposta)
#endregion