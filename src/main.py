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
#
# Por enquanto, este arquivo vai criar um chat simples no terminal.
# O usuário digita uma mensagem, o sistema envia essa mensagem
# para a LLM e depois mostra a resposta na tela.
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

#endregion

#region função main
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
            # ------------------------------------------------
            print(f"\nJARVIS: {resposta}")

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
            # Mostramos a resposta normal da LLM no terminal.
            # ------------------------------------------------
            print(f"\nJARVIS: {resposta}")

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