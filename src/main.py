#region descrição do arquivo
# ============================================================
# Arquivo: main.py
# ------------------------------------------------------------
# Este é o arquivo principal do nosso sistema.
#
# Ele é chamado de "principal" porque será o ponto de entrada
# do programa.
#
# Em outras palavras:
# quando quisermos iniciar o JARVIS Acadêmico, vamos rodar este
# arquivo.
# ============================================================


# ------------------------------------------------------------
# Importamos o objeto Application e a função gerenciar_comunicação
# do arquivo telegram.py.
# ------------------------------------------------------------
from src.telegram import application, gerenciar_comunicacao


# ------------------------------------------------------------
# Importamos as classe MessageHandler e filters do submódulo
# telegram.ext.
#
# A classe MessageHandler é utilizada para lidar com mensagens
# que não são comandos (ex: texto comum enviado pelo usuário).
# Ela permite definir qual função será executada quando uma
# mensagem for recebida.
#
# O módulo filters fornece filtros prontos que permitem selecionar
# quais tipos de mensagens o handler deve processar, como por
# exemplo apenas texto, apenas comandos, imagens, etc.
# ------------------------------------------------------------
from telegram.ext import MessageHandler, filters
#endregion

#region função main
# ------------------------------------------------------------
# Função: main
# ------------------------------------------------------------
# 
# ------------------------------------------------------------
def main():
    # ------------------------------------------------------------
    # Aqui configuramos para que quando o usuário enviar uma mensagem
    # de texto que não seja um comando, execute a função 
    # gerenciar_comunicacao.
    #
    # application.add_handler() é responsável por adicionar uma
    # regra de comportamento (add_handler registra um handler no bot).
    #
    # MessageHandler é a classe utilizada para tratar mensagens
    # comuns. Ela precisa de um filtro que determinará quando
    # a função deverá ser executada e uma função que será executada
    # quando as condições forem satisfeitas.
    #
    # filter.TEXT seleciona apenas mensagens que são textos e
    # ~filter.COMMAND seleciona tudo que não é comando ('~' indica
    # negação).
    #
    # Assim, a função gerenciar_comunicacao será executada quando
    # a condição do filtro, que nesse caso é para quando as mensagens
    # são textos comuns E (&) não são comandos, for satisfeito.
    # ------------------------------------------------------------
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerenciar_comunicacao))

    # ------------------------------------------------------------
    # Imprimimos uma mensagem para avisar que o bot está pronto
    # para comunicação.
    # ------------------------------------------------------------
    print("Bot integrado e rodando...")

    # ------------------------------------------------------------
    # Aqui inicializamos o bot e o event loop, isto é, fazemos com
    # que o bot fique perguntando repetidamente para o Telegram se
    # há uma mensagem nova. Assim, quando uma mensagem é recebida,
    # cria-se um Update e o envia para o handler correto.
    # ------------------------------------------------------------
    application.run_polling()
            
#endregion

#region execução do programa
# ------------------------------------------------------------
# Esta parte indica que a função main() deve ser executada
# quando rodarmos este arquivo diretamente.
#
# Parece estranho no começo, mas a ideia é simples:
#
# Se eu rodar:
#
# python -m src.main
#
# então o Python executa o main().
#
# Isso é uma prática muito comum em projetos Python.
# ------------------------------------------------------------
if __name__ == "__main__":
    main()

#endregion