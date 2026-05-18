#region explicação do arquivo

# ============================================================
# Arquivo: rag.py
# ------------------------------------------------------------
# Este arquivo será responsável por lidar com o RAG (Retrieval-
# Augmented Generation).
#
# A implementação do RAG, isto é, a consulta orientada a materiais
# de estudo, é uma das funcionalidades obrigatórias do Trabalho 1.
#
# Ela deve permitir que o usuário faça perguntas sobre materiais
# (PDFs, textos, anotações), como por exemplo:
#
# - "Explique regressão logística"
# - "Resuma o conteúdo sobre embeddings"
# - "Quais são os principais pontos do material X?"
#
# Neste arquivo, vamos criar funções para ler os dados da agenda -> A substituir
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


#endregion

#region caminho da pasta com materiais de consulta
# ------------------------------------------------------------
# Aqui definimos o caminho até a pasta de materiais.
#
# Vamos entender com calma:
#
# __file__
#   representa o caminho deste arquivo atual, ou seja:
#   src/rag.py
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
#   Como rag.py está dentro de src/, subir uma pasta nos leva
#   para a pasta principal do projeto:
#   jarvis-academico/
#
# Depois juntamos:
#   "data" / "materiais"
#
# Resultado final:
#   jarvis-academico/data/materiais
# ------------------------------------------------------------
CAMINHO_MATERIAIS = Path(__file__).resolve().parent.parent / "data" / "materiais"
#endregion

#region carregar_caminhos_documentos (intermediária, retorna lista com os caminhos de todos os documentos)

# ------------------------------------------------------------
# Função: carregar_caminhos_documentos
# ------------------------------------------------------------
# Esta função lê a pasta data/materiais e retorna uma lista de 
# de strings com todos os arquivos encontrados.
#
# Se a pasta estiver vazia, a lista será vazia.
#
# Então esta função devolverá uma lista vazia.
#
# Se a pasta data/materiais apresentar documentos, ela devolverá
# uma lista com os caminhos dos documentos.
# ------------------------------------------------------------
def carregar_caminhos_documentos():
    # --------------------------------------------------------
    # Cria-se uma lista vazia chamada documentos.
    # 
    # Essa lista vai guardar o caminho dos documentos encontrados 
    # na pasta data/materiais.
    #
    # No começo, ela está vazia porque ainda não consultou nada.
    # --------------------------------------------------------
    caminho_documentos = []

    # --------------------------------------------------------
    # Aqui iteramos sobre tudo que estiver dentro da pasta 
    # data/materiais.
    #
    # CAMINHO_MATERIAIS é o caminho até a pasta que queremos abrir.
    #
    # O método iterdir da biblioteca pathlib retorna um iterador 
    # de objetos do tipo Path, permitindo que os itens dentro da
    # pasta possam ser percorridos.
    #
    # "for arquivo in CAMINHO_MATERIAIS.iterdir()" significa:
    #
    # para cada arquivo ou subdiretório dentro da pasta data/materiais,
    # execute o bloco de código abaixo.
    # --------------------------------------------------------
    for arquivo in CAMINHO_MATERIAIS.iterdir():
        # ----------------------------------------------------
        # Aqui verificamos se o item atual é um arquivo, ignorando
        # diretórios.
        # 
        # Exemplo:
        # 
        # Pode apresentar um diretório denominado "IA" e um arquivo
        # de texto "rag.txt".
        #
        # Será retornado uma lista de um único elemento com o caminho
        # do arquivo de texto "rag.txt" como um objeto Path.
        # ----------------------------------------------------
        if arquivo.is_file():
            # ------------------------------------------------
            # Se o item é um arquivo, então adicionamos o caminho
            # dela na lista caminho_documentos.
            #
            # append significa "adicionar ao final da lista".
            # ------------------------------------------------
            caminho_documentos.append(arquivo)

    # --------------------------------------------------------
    # Depois de consultar todos os arquivos da pasta, devolvemos
    # a lista com o caminho dos documentos encontrados.
    #
    # Se encontrou algum, a lista terá esses caminhos.
    #
    # Se não encontrou nada, a lista continuará vazia: []
    # --------------------------------------------------------
    return caminho_documentos
#endregion

#region carregar_texto_txt (intermediária, retorna o conteúdo textual de um arquivo .txt)

# ------------------------------------------------------------
# Função: carregar_texto_txt
# ------------------------------------------------------------
# Esta função lê o documento a partir do caminho especificado
# e devolve o conteúdo dele para o restante do programa.
#
# Se o conteúdo do documento estiver vazio, então esta função
# devolverá uma string vazia.
#
# Se o documento tiver conteúdo, ela devolverá o texto em formato
# de string.
# ------------------------------------------------------------
def carregar_texto_txt(caminho_documento: Path) -> str:
    # --------------------------------------------------------
    # Aqui abrimos o documento em modo de leitura.
    #
    # open(...) serve para abrir arquivos.
    #
    # caminho_documento é o caminho do documento que queremos abrir.
    #
    # "r" significa read, ou seja, leitura.
    #
    # encoding="utf-8" ajuda o Python a lidar corretamente com
    # acentos e caracteres especiais da língua portuguesa.
    #
    # O "with" é usado porque ele abre o arquivo, usa o arquivo
    # e depois fecha automaticamente.
    # --------------------------------------------------------
    with open(caminho_documento, "r", encoding="utf-8") as arquivo:
        # ----------------------------------------------------
        # .read() lê o conteúdo do arquivo como uma string.
        #
        # Se o documento estiver vazio, retorna uma string vazia.
        #
        # Caso contrário, será retornado todo o conteúdo do 
        # documento como string.
        # ----------------------------------------------------
        texto = arquivo.read()

    # --------------------------------------------------------
    # Aqui devolvemos o conteúdo do documento para quem chamou a
    # função.
    # --------------------------------------------------------
    return texto
#endregion

