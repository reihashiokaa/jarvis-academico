#region explicação do arquivo

# ============================================================
# Arquivo: logger.py
# ------------------------------------------------------------
# Este arquivo será responsável por registrar logs das chamadas
# de ferramentas do JARVIS.
#
# O trabalho exige que o sistema registre logs contendo:
#
# - ferramenta chamada;
# - entrada recebida pela ferramenta;
# - saída devolvida pela ferramenta.
#
# Esses logs são importantes porque ajudam a mostrar que o sistema
# realmente está usando tool calling.
#
# Também ajudam a analisar o comportamento do sistema durante os
# testes e durante a apresentação do trabalho.
#
# Neste arquivo, vamos gravar os registros no arquivo:
#
# logs/tool_calls.jsonl
#
# O formato .jsonl significa JSON Lines.
#
# Isso quer dizer que cada linha do arquivo será um JSON separado.
#
# Exemplo:
#
# {"ferramenta": "consultar_tarefas", "entrada": {}, "saida": "..."}
# {"ferramenta": "adicionar_tarefa", "entrada": {"titulo": "Estudar RAG"}, "saida": "..."}
#
# Esse formato é bom para logs porque permite adicionar uma nova
# linha no final do arquivo sem precisar reescrever tudo.
#
# A lógica geral usada neste arquivo será:
#
# registrar_...
#   -> grava algum tipo de registro no arquivo de logs.
#
# Como este arquivo será usado internamente pelo sistema, suas
# funções serão intermediárias.
# ============================================================

#endregion

#region importações

# ------------------------------------------------------------
# Importamos a biblioteca json.
#
# Ela será usada para transformar dicionários Python em texto no
# formato JSON.
#
# Isso é necessário porque cada log será salvo como uma linha JSON
# dentro do arquivo logs/tool_calls.jsonl.
# ------------------------------------------------------------
import json


# ------------------------------------------------------------
# Importamos Path da biblioteca pathlib.
#
# O Path ajuda a trabalhar com caminhos de arquivos e pastas de
# forma mais organizada.
#
# Neste arquivo, vamos usar Path para encontrar o arquivo:
#
# logs/tool_calls.jsonl
#
# sem depender de escrever o caminho completo manualmente.
# ------------------------------------------------------------
from pathlib import Path


# ------------------------------------------------------------
# Importamos datetime da biblioteca datetime.
#
# Essa ferramenta será usada para registrar o momento em que a
# chamada de ferramenta aconteceu.
#
# Assim, cada log poderá guardar também uma informação de data e
# hora.
#
# Isso não foi pedido explicitamente pelo professor, mas é uma boa
# prática, porque deixa o log mais útil para depuração e análise.
# ------------------------------------------------------------
from datetime import datetime

#endregion

#region caminho do arquivo de logs

# ------------------------------------------------------------
# Aqui definimos o caminho até o arquivo tool_calls.jsonl.
#
# Vamos entender com calma:
#
# __file__
#   representa o caminho deste arquivo atual, ou seja:
#   src/logger.py
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
#   Como logger.py está dentro de src/, subir uma pasta nos leva
#   para a pasta principal do projeto:
#   jarvis-academico/
#
# Depois juntamos:
#   "logs" / "tool_calls.jsonl"
#
# Resultado final:
#   jarvis-academico/logs/tool_calls.jsonl
# ------------------------------------------------------------
CAMINHO_LOGS_FERRAMENTAS = Path(__file__).resolve().parent.parent / "logs" / "tool_calls.jsonl"

#endregion

#region registrar_chamada_ferramenta (intermediária, recebe dados de uma chamada de ferramenta e grava no arquivo de logs)

# ------------------------------------------------------------
# Função: registrar_chamada_ferramenta
# ------------------------------------------------------------
# Esta função registra uma chamada de ferramenta no arquivo de logs.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque o trabalho exige que o sistema registre logs contendo:
#
# - ferramenta chamada;
# - entrada recebida pela ferramenta;
# - saída devolvida pela ferramenta.
#
# Exemplo:
#
# ferramenta chamada:
#   "consultar_tarefas"
#
# entrada:
#   {}
#
# saída:
#   "Você tem 2 tarefa(s) cadastrada(s)..."
#
# Esses dados serão salvos no arquivo:
#
# logs/tool_calls.jsonl
#
# Cada chamada de ferramenta será registrada em uma linha separada
# do arquivo.
# ------------------------------------------------------------
def registrar_chamada_ferramenta(nome_ferramenta: str, entrada, saida):
    # --------------------------------------------------------
    # O parâmetro "nome_ferramenta" representa o nome da ferramenta
    # que foi chamada.
    #
    # Exemplos:
    #
    # "consultar_tarefas"
    # "adicionar_tarefa"
    # "concluir_tarefa"
    # "consultar_agenda_hoje"
    #
    # Usamos str porque o nome da ferramenta será um texto.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "entrada" representa os dados que foram enviados
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
    # Para concluir tarefa:
    #
    # {
    #     "id_tarefa": 2
    # }
    #
    # Não colocamos um tipo fixo aqui porque a entrada pode variar:
    # às vezes pode ser um dicionário, às vezes uma string, às vezes
    # um número.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # O parâmetro "saida" representa aquilo que a ferramenta
    # devolveu depois de executar.
    #
    # Exemplo:
    #
    # "Tarefa adicionada com sucesso: [2] Fazer README"
    #
    # Também não colocamos um tipo fixo aqui porque, no futuro,
    # algumas ferramentas podem devolver textos, listas ou outros
    # tipos de dados.
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Primeiro, vamos criar um dicionário chamado registro.
    #
    # Esse dicionário representa uma linha de log.
    #
    # Ele terá as informações principais da chamada de ferramenta:
    #
    # - data_hora;
    # - ferramenta;
    # - entrada;
    # - saida.
    # --------------------------------------------------------
    registro = {
        # ----------------------------------------------------
        # Aqui registramos a data e hora da chamada.
        #
        # datetime.now() pega o momento atual do computador.
        #
        # isoformat() transforma esse momento em texto organizado.
        #
        # Exemplo:
        #
        # "2026-05-15T20:30:10.123456"
        #
        # Isso ajuda a saber quando a ferramenta foi chamada.
        # ----------------------------------------------------
        "data_hora": datetime.now().isoformat(),

        # ----------------------------------------------------
        # Aqui registramos o nome da ferramenta chamada.
        # ----------------------------------------------------
        "ferramenta": nome_ferramenta,

        # ----------------------------------------------------
        # Aqui registramos a entrada enviada para a ferramenta.
        # ----------------------------------------------------
        "entrada": entrada,

        # ----------------------------------------------------
        # Aqui registramos a saída devolvida pela ferramenta.
        # ----------------------------------------------------
        "saida": saida
    }

    # --------------------------------------------------------
    # Agora abrimos o arquivo de logs em modo de acréscimo.
    #
    # O modo "a" significa append, ou seja:
    #
    # "adicione no final do arquivo".
    #
    # Isso é diferente do modo "w", que substitui o conteúdo antigo.
    #
    # Para logs, queremos sempre acrescentar uma nova linha, sem
    # apagar os registros anteriores.
    # --------------------------------------------------------
    with open(CAMINHO_LOGS_FERRAMENTAS, "a", encoding="utf-8") as arquivo:
        # ----------------------------------------------------
        # json.dumps(registro, ...) transforma o dicionário Python
        # em um texto no formato JSON.
        #
        # ensure_ascii=False permite salvar acentos corretamente.
        #
        # Exemplo de resultado:
        #
        # {"data_hora": "...", "ferramenta": "consultar_tarefas", ...}
        # ----------------------------------------------------
        linha_json = json.dumps(registro, ensure_ascii=False)

        # ----------------------------------------------------
        # Agora escrevemos essa linha JSON dentro do arquivo.
        #
        # O "\n" no final significa quebra de linha.
        #
        # Isso é importante porque o arquivo .jsonl usa uma linha
        # separada para cada registro.
        # ----------------------------------------------------
        arquivo.write(linha_json + "\n")

#endregion