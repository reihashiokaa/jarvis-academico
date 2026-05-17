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
#
# Por enquanto, este arquivo vai criar um chat simples no terminal.
# O usuário digita uma mensagem, o sistema envia essa mensagem
# para a LLM e depois mostra a resposta na tela.
# ============================================================
#





# ------------------------------------------------------------
# Aqui importamos a função chamar_llm.
#
# Essa função está no arquivo llm_client.py.
#
# Lembra?
# O arquivo llm_client.py é o responsável por conversar com o
# Gemma 12B.
#
# Então, quando o main.py quiser mandar uma mensagem para a IA,
# ele não precisa saber todos os detalhes da API.
#
# Ele só chama:
#
# chamar_llm(mensagem)
#
# Isso deixa o projeto mais organizado.
# ------------------------------------------------------------
from llm_client import chamar_llm




# AGORA A FUNÇÃO PRINCIPAL DO PROGRAMA
# QUE VAI CONTROLAR O FLUXO DE CONVERSA COM O USUÁRIO E A LLM

# ------------------------------------------------------------
# Função: main
# ------------------------------------------------------------
# Esta função representa o fluxo principal do programa.
#
# Ela será responsável por:
#
# - iniciar o chat;
# - receber mensagens do usuário;
# - enviar essas mensagens para a LLM;
# - imprimir a resposta da LLM;
# - encerrar o programa quando o usuário digitar "sair".
# ------------------------------------------------------------
def main():
    # --------------------------------------------------------
    # Aqui mostramos uma mensagem inicial no terminal.
    #
    # Isso serve para avisar ao usuário que o sistema começou
    # corretamente.
    #
    # O comando print(...) mostra texto na tela.
    # --------------------------------------------------------
    print("JARVIS Acadêmico iniciado.")
    print("Digite 'sair' para encerrar o programa.")

    # --------------------------------------------------------
    # Aqui começa um loop infinito.
    #
    # Um loop é uma repetição.
    #
    # while True significa:
    #
    # "repita isso para sempre, até que alguma parte do código
    # mande parar".
    #
    # Usamos isso porque um chat precisa continuar funcionando
    # enquanto o usuário quiser conversar.
    # --------------------------------------------------------
    while True:
        # ----------------------------------------------------
        # O comando input(...) espera o usuário digitar algo
        # no terminal.
        #
        # O texto "Você: " aparece só para indicar onde o usuário
        # deve escrever a mensagem.
        #
        # Tudo que o usuário digitar será guardado na variável
        # chamada "mensagem".
        # ----------------------------------------------------
        mensagem = input("\nVocê: ")

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
            # ------------------------------------------------
            print("JARVIS: Até mais!")

            # ------------------------------------------------
            # O break serve para interromper o loop.
            #
            # Como o loop estava repetindo para sempre, o break
            # é o comando que manda parar.
            # ------------------------------------------------
            break

        # ----------------------------------------------------
        # Se o usuário não digitou "sair", então vamos enviar
        # a mensagem para a LLM.
        #
        # A função chamar_llm(...) recebe o texto digitado pelo
        # usuário e devolve a resposta gerada pelo Gemma.
        # ----------------------------------------------------
        resposta = chamar_llm(mensagem)

        # ----------------------------------------------------
        # Aqui mostramos a resposta da LLM no terminal.
        #
        # O f antes das aspas indica uma f-string.
        #
        # Uma f-string permite colocar variáveis dentro do texto
        # usando chaves { }.
        #
        # Neste caso, {resposta} será substituído pelo texto que
        # veio do Gemma.
        # ----------------------------------------------------
        print(f"\nJARVIS: {resposta}")




# ------------------------------------------------------------
# Esta parte indica que a função main() deve ser executada
# quando rodarmos este arquivo diretamente.
#
# Parece estranho no começo, mas a ideia é simples:
#
# Se eu rodar:
#
# python src/main.py
#
# então o Python executa o main().
#
# Isso é uma prática muito comum em projetos Python.
# ------------------------------------------------------------
if __name__ == "__main__":
    main()