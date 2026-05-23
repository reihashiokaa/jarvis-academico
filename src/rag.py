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
# 
# ------------------------------------------------------------
import numpy as np


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
# Importamos PdfReader da biblioteca pypdf.
#
# O PdfReader ajuda a abrir e ler arquivos PDFs.
#
# Ele é um objeto que dá acesso ao conteúdo interno de um PDF,
# assim permitindo extrair o texto do arquivo, entre outras
# funções.
# ------------------------------------------------------------
from pypdf import PdfReader


# ------------------------------------------------------------
# Importamos a biblioteca re.
#
# Ela é uma biblioteca padrão utilizada para trabalhar com
# expressões regulares, isto é, sequências especiais de
# caracteres que definem um formato fixo, como por exemplo
# '\{4}' que descreve a regra: "procure exatamente quatro
# números que estejam juntos".
#
# Essa biblioteca permitirá que um determinado padrão seja
# encontrado em uma string e possivelmente substituído por
# outro valor.
# ------------------------------------------------------------
import re


# ------------------------------------------------------------
# Importamos SentenceTransformer da biblioteca sentence-transformers.
#
# SentenceTransformer é uma classe que carrega um modelo de embeddings
# e transforma textos em vetores numéricos.
#
# Internamente, ele baixa o modelo pré-treinado da internet (caso não
# ainda não esteja disponível localmente), carrega esse modelo na memória
# e utiliza redes neurais para deixá-lo pronto para inferência.
# ------------------------------------------------------------
from sentence_transformers import SentenceTransformer


# ------------------------------------------------------------
# 
# ------------------------------------------------------------
from sklearn.metrics.pairwise import cosine_similarity
#endregion

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

#region formatar_texto (intermediária, formata o texto recuperado dos arquivos de texto)

# ------------------------------------------------------------
# Função: formatar_texto
# ------------------------------------------------------------
# Esta função recebe uma string com o texto recuperado dos arquivos
# e formata a string removendo as quebras de linha e espaços
# duplicados, de forma a retornar uma string mais limpa e legível
# para trabalhar.
# ------------------------------------------------------------
def formatar_texto(texto):
    # --------------------------------------------------------
    # Verifica se o texto passado apresenta conteúdo ou não.
    # 
    # Se texto apresentar uma string, ela será interpretada
    # como True e não entrará no bloco condicional por causa
    # da negação.
    #
    # Caso contrário, se texto não apresentar valor (None) ou 
    # for uma string vazia, então entrará no bloco condicional
    # visto que None ou string vazia é interpretado como False,
    # mas como está sendo negado pela notação "not", então 
    # será considerado como True e entrará no bloco.
    #
    # De forma resumida ele pergunta "O texto apresenta conteúdo?
    # Se não, entre no bloco".
    # --------------------------------------------------------
    if not texto:
        # --------------------------------------------------------
        # Retorna uma string vazia já que texto não apresenta nenhum
        # conteúdo para ser formatado.
        # --------------------------------------------------------
        return ""

    # --------------------------------------------------------
    # Aqui substituímos as quebras de linha por espaço, evitando
    # que as frases fiquem quebradas no meio.
    #
    # O método replace substitui partes específicas de uma string
    # por um novo texto. Ele procura por 'substrings' que correspondem
    # ao valor informado no parâmetro e as trocam por um novo texto,
    # este também informado no parâmetro, assim retornando uma
    # nova string modificada.
    # --------------------------------------------------------
    texto = texto.replace("\n", " ")
    
    # --------------------------------------------------------
    # Aqui substituímos um padrão por um espaço em branco (" ").
    #
    # O método sub da biblioteca re substitui ocorrências de um
    # padrão específico encontrado em uma string por um novo 
    # texto.
    #
    # Nesse caso, o padrão r"\s+" significa:
    #
    #  - r"": raw string, um tipo literal de texto que trata
    #  barras invertidas ('\') como caracteres literais, ignorando
    #  sequências de escape, isto é, combinações de caracteres
    #  utilizadas para representar caracteres especiais, não
    #  imprimíveis ou de controle, como por exemplo '\t' para
    #  tabulações;
    #
    #  - \s: significa qualquer caractere de espaço, seja ele
    #  um espaço (" "), tabulação ('\t'), quebra de linha ('\n')
    #  ou outros espaços invisíveis;
    #
    #  - +: determina que seja uma ou mais ocorrências de um padrão,
    #  em outras palavras, para um ou mais espaços de qualquer
    #  tipo.
    #
    # Assim, para qualquer ocorrência de caracteres de espaço com
    # um ou mais espaços encontrado na string, será substituído
    # por um único espaço (" ").
    #
    # Exemplo:
    #
    # "Regressão logística\n\nrefere-se\ta..."
    # 
    # Será substituído por:
    #
    # "Regressão logística refere-se a..."
    # --------------------------------------------------------
    texto = re.sub(r"\s+", " ", texto)

    # --------------------------------------------------------
    # Por fim, retorna o texto limpo, sem quebra de linhas ou
    # espaços repetidos em branco.
    # --------------------------------------------------------
    return texto
#endregion

#region carregar_texto_txt (intermediária, retorna o conteúdo textual de um arquivo .txt)

# ------------------------------------------------------------
# Função: carregar_texto_txt
# ------------------------------------------------------------
# Esta função lê o documento informado pelo caminho especificado
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
    # função como uma string formatada, sem quebras de linhas ou
    # espaços duplicados por meio da chamada da função formatar_texto.
    # --------------------------------------------------------
    return formatar_texto(texto)
#endregion

#region carregar_texto_pdf (intermediária, retorna o conteúdo textual de um arquivo .pdf)

# ------------------------------------------------------------
# Função: carregar_texto_pdf
# ------------------------------------------------------------
# Esta função extrai o texto de um documento PDF, informado a
# partir do caminho do arquivo na pasta data/materiais e retorna
# o conteúdo dele para o restante do programa.
#
# Se o conteúdo do documento estiver vazio, então esta função
# devolverá uma string vazia.
#
# Se o documento tiver conteúdo, ela devolverá o texto em formato
# de string.
# ------------------------------------------------------------
def carregar_texto_pdf(caminho_documento: Path) -> str:
    # --------------------------------------------------------
    # Aqui inicializamos uma string vazia, que acumulará todo o 
    # texto extraído do arquivo PDF.
    # --------------------------------------------------------
    texto_completo = ""
    
    # --------------------------------------------------------
    # Inicia um bloco de tratamente de erro.
    # 
    # Utilizado para garantir que o programa não quebre caso
    # surgir um problema ao tentar abrir o arquivo PDF.
    # 
    # Se surgir um erro, esse erro será capturado e tratado no
    # bloco except, caso contrário, o bloco try rodará normalmente.
    # --------------------------------------------------------
    try:
        # --------------------------------------------------------
        # Aqui abre o arquivo PDF.
        # 
        # PdfReader(caminho_documento) basicamente abre o arquivo e 
        # lê a estrutura interna dele, retornando um objeto do tipo
        # PdfReader.
        # 
        # Esse objeto interpreta a estrutura do PDF, que é composto
        # por:
        # 
        #  - Header (versão do PDF)
        #  - Tabela de Referências (xref) 
        #  - Objetos internos (páginas, fontes, imagens)
        #  - Trailer (informações finais)
        #
        # E então mapeia a estrutura interna do arquivo como um
        # objeto, contendo a lista de páginas (leitor.pages), os
        # metadados (leitor.metadata) e objetos do documento.
        #
        # É importante enfatizar que nessa etapa o texto ainda não
        # está sendo extraído.
        # --------------------------------------------------------
        leitor = PdfReader(caminho_documento)
        
        # --------------------------------------------------------
        # Aqui iteramos sobre todas as páginas do PDF.
        #
        # .pages é uma lista de páginas, onde cada página vira um
        # objeto, contendo o conteúdo bruto da página, instruções
        # de renderização e referências a fontes.
        #
        # "for pagina in leitor.pages:" significa:
        #
        # para cada página do objeto PdfReader leitor, execute o 
        # bloco de código abaixo.
        # --------------------------------------------------------
        for pagina in leitor.pages:
            # --------------------------------------------------------
            # Nesta parte ocorre de fato a extração do texto para cada
            # página do PDF.
            #
            # .extract_text() é um método criado para extrair o texto da
            # página e convertê-lo em uma string para que possa ser
            # processada posteriormente.
            #
            # Se houver texto para ser extraído na página, o método
            # retornará uma string.
            #
            # Se não houver texto para ser extraído, o método retorna None.
            # 
            # Ao final armazena o texto extraído na variável texto_pagina.
            # --------------------------------------------------------
            texto_pagina = pagina.extract_text()
            
            # --------------------------------------------------------
            # Verifica se existe texto na página para ser extraído.
            #
            # Se texto_pagina é None, então não havia texto para ser 
            # extraído na página, o que por consequência não entra na
            # condicional, visto que None é interpretado como False.
            #
            # Caso contrário, se houver texto na página e texto_pagina
            # apresenta uma string, entrará na condicional, pois string
            # é interpretado como True.
            # --------------------------------------------------------
            if texto_pagina:
                # --------------------------------------------------------
                # Se texto_pagina apresentar uma string, então concatenamos
                # e atribuimos à string de texto_completo, que possui o 
                # texto das páginas que extraímos até então, ou caso for a
                # primeira vez, a string vazia que foi inicializada anteriormente.
                #
                # Por exemplo:
                # 
                # texto_completo = "Regressão logística é..."
                # texto_pagina = "RAG (Retrieval Augmented Generation) é..."
                #
                # O novo valor para texto completo será:
                # "Regressão logística é...RAG (Retrieval Augmented Generation)
                # é..."
                # --------------------------------------------------------
                texto_completo += texto_pagina
        
        # --------------------------------------------------------
        # Ao terminar de rodar o for, retorna o valor de texto_completo,
        # que pode consistir em uma string não vazia caso haja texto
        # para ser extraído no PDF ou uma string vazia caso não
        # apresente nenhum texto extraivel.
        #
        # A função formatar_texto é chamada para formatar a string
        # resultante, substituindo quebras de linha e espaços duplicados
        # por um único espaço (" ").
        # --------------------------------------------------------
        return formatar_texto(texto_completo)
       
    # --------------------------------------------------------
    # Se ocorrer algum erro ao executar o bloco try, esse erro
    # será capturado e tratado no bloco except que está capturando
    # qualquer tipo de exceção e imprimindo no terminal.
    # -------------------------------------------------------- 
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        
        # --------------------------------------------------------
        # Retorna uma string vazia quando ocorrer um erro, para
        # evitar quebrar o resto do programa caso alguma função
        # a chame e espere receber uma string.
        # --------------------------------------------------------
        return ""
#endregion

#region carregar_texto_documento (intermediária, decide como carregar o texto)

# ------------------------------------------------------------
# Função: carregar_texto_documento
# ------------------------------------------------------------
# Esta função recebe um caminho de documento e decide como
# carregar o texto, dependendo se é um arquivo .txt ou PDF,
# assim centralizando a leitura de documentos.
#
# Se o arquivo for .txt chama a função carregar_texto_txt().
#
# Se o arquivo for .pdf chama a função carregar_texto_pfd().
#
# Caso não apresentar um formato suportado, retorna uma string
# vazia junto de uma mensagem controlada.
# ------------------------------------------------------------
def carregar_texto_documento(caminho_documento):
    # --------------------------------------------------------
    # Aqui verificamos a extensão do arquivo, se for .txt então
    # entra no bloco condicional.
    #
    # O método lower é utilizado para converter todos os caracteres
    # da string em caixa baixa (lowercase) para evitar erros de
    # comparação entre caracteres maiúsculos com caracteres
    # minúsculos, visto que a comparação é sensitive case, ou seja,
    # diferencia maiúsculas de minúsculas.
    #
    # endswith(".txt") serve para verificar se uma string termina
    # com um trecho específico, neste caso, ".txt", assim verificando
    # se o documento é um arquivo de texto ou não. Ele retorna 
    # True para caso o documento termine com ".txt" e False caso
    # contrário.
    #
    # Exemplo:
    # 
    # caminho_documento = "jarvis-academico/data/materiais/RAG.txt"
    #
    # O método lower transforma para:
    # "jarvis-academico/data/materiais/rag.txt"
    #
    # .name é um atributo da biblioteca pathlib que retorna uma
    # string com o nome do componente final do caminho, ou seja,
    # o nome do arquivo com sua extensão. Utilizado para verificar
    # se a extensão do arquivo é .txt.
    #
    # E o método endswith verifica se o caminho_documento termina
    # com ".txt". Como o caminho_documento termina com ".txt",
    # ele retornará True e o programa seguirá para a execução
    # do bloco condicional.
    # --------------------------------------------------------    
    if caminho_documento.name.lower().endswith(".txt"):
        # --------------------------------------------------------
        # Se entrar na condição, isso significa que o documento
        # é do tipo ".txt".
        #
        # Assim, chama a função correspondente e retorna o valor
        # da função.
        # --------------------------------------------------------
        return carregar_texto_txt(caminho_documento)
    
    # --------------------------------------------------------
    # Aqui verificamos a extensão do arquivo caso não entre
    # no bloco condicional anterior, verificando se arquivo
    # é um pdf (".pdf").
    #
    # Funciona de forma similar a condição anterior, porém
    # verificando se é um arquivo PDF em vez de arquivo de texto
    # .txt.
    # --------------------------------------------------------   
    elif caminho_documento.name.lower().endswith(".pdf"):
        # --------------------------------------------------------
        # Se entrar na condição, isso significa que o documento
        # é do tipo ".pdf".
        #
        # Assim, chama a função correspondente e retorna o valor
        # da função.
        # --------------------------------------------------------
        return carregar_texto_pdf(caminho_documento)
    
    # --------------------------------------------------------
    # Se não entrar em nenhum dos blocos condicionais anteriores,
    # entra nesse bloco, significando que o documento não apresenta
    # um formato suportado, não é nem ".txt" e nem ".pdf".
    # --------------------------------------------------------
    else:
        # --------------------------------------------------------
        # Por não ser do formato suportado, retorna uma string vazia 
        # e comunica o usuário que o documento não é de um formato
        # suportado pela função.
        #
        # f"" representa uma F-string (Formatted String Literal),
        # permitindo incluir variáveis diretamente dentro da string
        # por meio da colocação da variável dentro de chaves { }.
        #
        # .name é um atributo da biblioteca pathlib que retorna uma
        # string com o nome do componente final do caminho, ou seja,
        # o nome do arquivo com sua extensão. Utilizado para informar
        # ao usuário qual é o documento com extensão não suportada
        # pela função.
        # --------------------------------------------------------
        print(f"\nFormato não suportado {caminho_documento.name}")
        return ""
#endregion

#region carregar_documentos (intermediária, retorna o conteúdo de todos os documentos presentes)

# ------------------------------------------------------------
# Função: carregar_documentos
# ------------------------------------------------------------
# Esta função carrega e extrai todos os documentos na pasta
# data/materiais, guardando o nome do arquivo e o texto extraído.
#
# Retorna uma lista de dicionários, ignorando os documentos que
# não apresentam texto.
#
# Exemplo:
#
# [
#   {
#     "nome": "aula_embeddings.pdf",
#     "conteudo": "conteúdo extraído do arquivo..."
#   },
#   {
#     "nome": "resumo_rag.txt",
#     "conteudo": "conteúdo extraído do arquivo"
#   }
# ]
#
# Se não encontrar nenhum documento, retorna uma lista vazia.
# ------------------------------------------------------------
def carregar_documentos():
    # --------------------------------------------------------
    # Chama a função intermediária carregar_caminhos_documentos
    # que retorna uma lista com o caminho de todos os documentos
    # presentes, caso não houver documentos, retorna uma lista vazia.
    # 
    # Atribui a lista na variável caminhos_documentos.
    # --------------------------------------------------------
    caminhos_documentos = carregar_caminhos_documentos()
    
    # --------------------------------------------------------
    # Inicializamos uma lista vazia que servirá para guardar os
    # dicionários dos documentos carregados.
    # --------------------------------------------------------
    documentos = []
    
    # --------------------------------------------------------
    # Aqui iteramos sobre a lista caminhos_documentos.
    #
    # "for caminho_doc in caminhos_documentos" basicamente significa:
    #
    # para cada caminho encontrado, execute o bloco de código
    # abaixo.
    # --------------------------------------------------------
    for caminho_doc in caminhos_documentos:
        # --------------------------------------------------------
        # Chama a função intermediária carregar_texto_documento
        # que decide como o texto será carregado (.txt ou .pdf).
        # 
        # Se o documento for de uma extensão suportada retorna o
        # texto extraído do documento, caso contrário a função
        # retorna uma string vazia.
        #
        # Armazena o texto extraído na variável texto.
        # --------------------------------------------------------
        texto = carregar_texto_documento(caminho_doc)
        
        # --------------------------------------------------------
        # Verifica se o texto carregado não está vazio.
        #
        # Strings vazias ou valores None são interpretados como False,
        # então caso não apresente um texto, ele não entrará neste bloco
        # condicional.
        #
        # Dessa forma os documentos que não apresentam conteúdo,
        # estiverem vazios, não serão incluídos na lista.
        # --------------------------------------------------------
        if texto:
            # --------------------------------------------------------
            # Cria um dicionário com os dados do documento.
            #
            #  - "arquivo" refere-se ao nome do arquivo.
            #
            #  - "conteudo" refere-se ao texto do arquivo.
            #
            #  - caminho_doc.name pega a string com o nome do componente final
            #  do caminho, ou seja, o nome do arquivo.
            #
            #  - texto é o conteúdo extraído e formatado do documento.
            # --------------------------------------------------------
            documento_dic = {
                "nome": caminho_doc.name,
                "conteudo": texto
            }
            
            # --------------------------------------------------------
            # Por fim, adiciona ao final da lista documentos o dicionário
            # com os dados do arquivo.
            # --------------------------------------------------------
            documentos.append(documento_dic)

    # --------------------------------------------------------
    # Retorna a lista com os documentos carregados caso houver
    # documentos, caso contrário retorna uma lista vazia.
    # --------------------------------------------------------
    return documentos
#endregion

#region dividir_texto_em_chunks (intermediária, retorna uma lista de chunks do texto fornecido)

# ------------------------------------------------------------
# Função: dividir_texto_em_chunks
# ------------------------------------------------------------
# Esta função recebe um texto em formato de string e retorna
# uma lista de chunks, isto é, uma lista com pedaços menores do
# texto.
#
# O tamanho do pedaço do chunk e da sobreposição são passados por
# parâmetro, onde:
#  
#  - tamanho_chunk recebe um valor inteiro que define o tamanho
#  desses pedaços menores de texto, contando a quantidade de
#  palavras.
#
#  - sobreposicao recebe um valor inteiro que define quantos
#  palavras se repetem entre um chunk e o próximo.
#
# Se o texto for uma string vazia, será retornado uma lista vazia.
# ------------------------------------------------------------
def dividir_texto_em_chunks(texto, tamanho_chunk=500, sobreposicao=100):
    # ------------------------------------------------------------
    # O método split divide uma string em uma lista no qual cada
    # palavra é um item da lista.
    #
    # Inicializa um vetor vazio para guardar os chunks que foram
    # extraídos.
    # ------------------------------------------------------------
    palavras = texto.split()
    chunks = []
    
    # ------------------------------------------------------------
    # Também é inicializado uma variável que será responsável por
    # armazenar e atualizar um valor que indicará onde um chunk
    # começa.
    # ------------------------------------------------------------
    inicio = 0
    
    # ------------------------------------------------------------
    # Aqui iteramos na lista das palavras até que tenhamos percorrido
    # ela por inteiro.
    #
    # A variável inicio que foi definida anteriormente servirá como
    # índice para esse laço.
    # ------------------------------------------------------------
    while inicio < len(palavras):
        # ------------------------------------------------------------
        # O índice final de um chunk é dado pelo seu índice inicial somado
        # do tamanho do chunk.
        # 
        # Por exemplo, se o tamanho foi definido como 10, ou seja, um
        # chunk tem 10 palavras, e esse determinado chunk inicia-se na
        # palavra de posição 0, então o chunk será composto pelas palavras
        # da posição 0 até a de posição 10.
        # ------------------------------------------------------------
        fim = inicio + tamanho_chunk
        
        # ------------------------------------------------------------
        # Para separar as palavras em chunks, executamos os seguintes
        # comandos:
        #
        #  - palavras[inicio:fim] é o fatiamento do python, onde pegamos
        #  um pedaço da lista, demarcado pelo índice inicial (a partir
        #  de qual posição recortamos) e pelo índice final (até qual 
        #  posição vai o recorte). Por exemplo, se tenho uma lista 
        #  com 5 elementos e recorto da posição 0 a 3, então o pedaço
        #  retornado será uma lista com os elementos dos índices 0, 1 
        #  e 2.
        #
        #  - " ".join(chunk) transforma uma lista de palavras em uma única
        #  string, no qual " " é o separador que será colocado entre cada
        #  elemento da lista na string e .join(chunk) pega todos os 
        #  elementos da lista e junta eles com o separador. Essa parte
        #  é importante, pois é ele que junta a lista de palavras e
        #  transforma em uma única string, assim criando um chunk que
        #  realmente seja um trecho do texto e não uma lista de palavras.
        #
        #  - chunks.append adiciona o chunk extraído a lista de chunks.
        # ------------------------------------------------------------
        chunk = palavras[inicio:fim]
        chunks.append(" ".join(chunk))
        
        # ------------------------------------------------------------
        # Após extrair um chunk, atualizamos o valor da variável inicio.
        # 
        # A atualização é feita a partida da soma do valor de inicio com
        # o valor do tamanho do chunk, subtraindo o valor de sobreposição,
        # ou seja, a atualização é calculada para que o próximo chunk
        # inicie incluindo algumas palavras repetidas do chunk anterior,
        # para evitar que uma definição não seja quebrada ao meio.
        # ------------------------------------------------------------
        inicio += tamanho_chunk - sobreposicao
    
    # ------------------------------------------------------------
    # Retornamos a lista de chunks.
    # ------------------------------------------------------------
    return chunks
#endregion

#region carregar_chunks_documentos (intermediária, retorna uma lista com os chunks de todos os documentos)

# ------------------------------------------------------------
# Função: carregar_chunks_documentos
# ------------------------------------------------------------
# Esta função lê todos os documentos e retorna os seus respectivos
# chunks como uma lista de dicionários, onde cada dicionário guardará
# os seguintes dados:
#
# - id do chunk;
# - nome do arquivo de origem;
# - texto do chunk;
#
# Poderá ser retornado uma lista vazia caso não apresente nenhum
# documento.
# ------------------------------------------------------------
def carregar_chunks_documentos():
    # --------------------------------------------------------
    # Inicializa uma lista vazia para adicionarmos os chunks e
    # seus dados posteiormente.
    #
    # Adicionalmente, é inicializado um índice para os ids.
    # --------------------------------------------------------
    lista_chunks= []
    id = 0

    # --------------------------------------------------------
    # Aqui chamamos a função carregar_documentos que lê todos
    # os documentos e retorna uma lista de dicionários com os
    # textos extraídos, seguindo o formato:
    #
    # {
    #   "nome": "Nome do Arquivo",
    #   "conteudo": "Texto extraído do arquivo"
    # }
    # --------------------------------------------------------
    documentos = carregar_documentos()

    # --------------------------------------------------------
    # Iteramos sobre a lista dos documentos.
    #
    # for documento in documentos indica:
    # "Para cada documento execute o seguinte bloco de código
    # abaixo."
    # --------------------------------------------------------
    for documento in documentos:
        # --------------------------------------------------------
        # Iteramos também sobre a lista de chunks de cada documento.
        #
        # dividir_texto_em_chunks retorna a lista de chunks do texto
        # passado por parâmetro, que nesse caso é o texto do documento,
        # associado pela chave 'conteudo' no dicionário, lembrando
        # que documento é um elemento em formato de dicionário da
        # lista de documentos.
        #
        # Então, para cada chunk da lista, executamos o bloco de
        # código abaixo.
        # --------------------------------------------------------
        for chunk in dividir_texto_em_chunks(documento["conteudo"]):
            # --------------------------------------------------------
            # Nesta parte organizamos os dados de um chunk como um dicionário,
            # guardando um valor de identificação (id), o nome do arquivo
            # o qual ele pertence (arquivo_origem) e o texto desse chunk
            # (texto_chunk).
            #
            # Essas informações de rastreabilidade são importantes, pois 
            # quando o sistema recuperar um trecho, será necessário saber
            # de qual documento ele veio.
            # --------------------------------------------------------
            chunk_data = {
                "id":id,
                "arquivo_origem":documento["nome"],
                "texto_chunk":chunk
            }

            # --------------------------------------------------------
            # Adicionamos o dicionário com os dados do chunk na lista
            # de chunks.
            # --------------------------------------------------------
            lista_chunks.append(chunk_data)

            # --------------------------------------------------------
            # Incrementamos o id.
            # --------------------------------------------------------
            id += 1

    # --------------------------------------------------------
    # Por fim retornamos a lista de chunks, que poderá ser vazia
    # caso não apresente nenhum documento.
    # --------------------------------------------------------
    return lista_chunks
#endregion

#region carregar_modelo_embeddings (intermediária, carrega o modelo que transforma um texto em vetor)

# ------------------------------------------------------------
# Função: carregar_modelo_embeddings
# ------------------------------------------------------------
# Esta função carrega o modelo que transforma texto em vetor.
# ------------------------------------------------------------
def carregar_modelo_embeddings():
    # ------------------------------------------------------------
    # Carrega o modelo pré-treinado que pode ser utilizado para mapear
    # um texto e outras entradas em embeddings densos.
    #
    # Embeddings densos são representações numéricas de dados (como
    # palavras, frases ou imagens) em formato de vetores, onde a
    # maioria das posições contém valores diferentes de zero. Eles
    # codificam o significado semântico e o contexto profundo dessas
    # informações, agrupando itens com conceitos semelhantes em um
    # espaço n-dimensional.
    # ------------------------------------------------------------
    modelo = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # ------------------------------------------------------------
    # Retorna o modelo.
    # ------------------------------------------------------------
    return modelo
#endregion

#region gerar_embeddings_chunks (intermediária, retorna uma lista com os embeddings dos chunks)

# ------------------------------------------------------------
# Função: gerar_embeddings_chunks
# ------------------------------------------------------------
# Esta função recebe uma lista de chunks e gera um vetor (embedding)
# para cada chunk.
#
# Retorna uma lista de chunks e a lista de embeddings,
# com cada chunk sendo organizado por meio de dicionários
# da seguinte forma:
# 
# - id do chunk (id_chunk)
# - Texto do chunk (texto_chunk)
#
# Se passar uma lista vazia de chunks, então a função retorna
# uma lista vazia de embeddings e indica que não foi possível
# gerar os embeddings.
# ------------------------------------------------------------
def gerar_embeddings_chunks(chunks):
    # ------------------------------------------------------------
    # Verifica se não foi passada uma lista vazia de chunks.
    # ------------------------------------------------------------
    if not chunks:
        # ------------------------------------------------------------
        # Se entrar, isso significa que foi passada uma lista vazia e
        # imprime que não foi possível gerar os embeddings, retornando
        # assim um vetor vazio para embeddings.
        # ------------------------------------------------------------
        print("Não foi possível gerar embeddings.")
        return chunks, []
    
    # ------------------------------------------------------------
    # Chama a função carregar_modelo_embeddings para carregar o
    # modelo.
    # ------------------------------------------------------------
    modelo = carregar_modelo_embeddings()
    
    # ------------------------------------------------------------
    # Aqui extraímos o texto de cada chunk e armazenamos tudo em uma
    # nova lista.
    #
    # Basicamente está falando para guardar os dados associados a
    # chave "texto_chunk" para cada dicionário (chunk) da lista de
    # de chunks (lista de dicionários).
    #
    # O dicionário segue o seguinte formato:
    #
    # {
    #   "id": id,
    #   "arquivo_origem": "nome_arquivo",
    #   "texto_chunk": "texto"
    # }
    #
    # ------------------------------------------------------------
    lista_textos = [chunk["texto_chunk"] for chunk in chunks]

    # ------------------------------------------------------------
    # A partir do modelo carregado, transformamos a lista de chunks
    # (textos) em vetores numéricos para auxiliar o computador a
    # entender o significado semântico das palavras.
    #
    # O método encode() recebe uma lista de textos e converte cada
    # texto em um vetor numérico, gerando então um vetor para cada
    # chunk. No final será retornado uma lista/matriz de embeddings.
    #
    # O parâmetro 'convert_to_numpy=True' define que o resultado
    # seja um numpy array em vez de uma lista comum do python.
    # Foi aplicado esse parâmetro para facilitar cálculos matemáticos
    # rápidos e processamento de dados posteriormente.
    #
    # Já o parâmetro 'normalize_embedding=True' normaliza cada vetor
    # do resultado para a norma = 1. Este parâmetro é aplicado para
    # padronizar os dados e permitir que o cálculo de similaridade
    # de cosseno seja feito de forma muito mais rápida, além de eliminar
    # o efeito do tamanho do texto, fazendo com que um texto longo
    # e um texto curto de mesmo significado tenham vetores de
    # mesmo tamanho.
    # ------------------------------------------------------------
    embeddings = modelo.encode(lista_textos, convert_to_numpy=True, normalize_embeddings=True)

    # ------------------------------------------------------------
    # Aqui verificamos se a quantidade de embeddings é igual à quantidade
    # de chunks.
    # ------------------------------------------------------------
    if len(embeddings) != len(chunks):
        # ------------------------------------------------------------
        # Se não for, isso significa que houve um problema na geração
        # e então é lançado um erro indicando essa diferença.
        # ------------------------------------------------------------
        raise ValueError("Quantidade de embeddings diferente da quantidade de chunks.")

    # ------------------------------------------------------------
    # Por fim é retornado o vetor de chunks, que contém apenas os
    # textos dos chunks, sem os dados adicionais, e a lista de
    # embeddings.
    # ------------------------------------------------------------
    return chunks, embeddings
#endregion

#region gerar_embedding_pergunta (intermediária, retorna um vetor da pergunta)

# ------------------------------------------------------------
# Função: gerar_embedding_pergunta
# ------------------------------------------------------------
# Esta função recebe uma pergunta em formato de string e a transforma
# em um vetor.
# ------------------------------------------------------------
def gerar_embedding_pergunta(pergunta: str):
    # ------------------------------------------------------------
    # Chama a função carregar_modelo_embedding para obter o modelo
    # que será utilizado para transformar o texto em vetor.
    # ------------------------------------------------------------
    modelo = carregar_modelo_embeddings()
    
    # ------------------------------------------------------------
    # Verifica se a string não está vazia. Lembrando que uma string
    # "" é considerada como False.
    # ------------------------------------------------------------
    if pergunta:
        # ------------------------------------------------------------
        # Se a string não for vazia transforma a pergunta em um vetor
        # a partir do modelo, convertendo o resultado para numpy array
        # e normalizando o vetor para a norma = 1.
        # ------------------------------------------------------------
        embedding_pergunta = modelo.encode(pergunta, convert_to_numpy=True, normalize_embeddings=True)
        return embedding_pergunta
        
    else:
        # ------------------------------------------------------------
        # Caso contrário, for uma string vazia, será imprimido uma mensagem
        # pedindo para informar uma pergunta válida e então retorna
        # uma lista vazia.
        # ------------------------------------------------------------
        print("Informe uma pergunta válida")
        return [] 
#endregion

#region calcular_similaridade_cosseno (intermediária, retorna a similaridade entre dois vetores)

# ------------------------------------------------------------
# Função: calcular_similaridade_cosseno
# ------------------------------------------------------------
# Esta função recebe dois vetores numéricos e retorna o quanto
# eles são parecidos.
#
# Utiliza a métrica de Similaridade de Cosseno para calcular
# esse grau de semelhança.
# ------------------------------------------------------------
def calcular_similaridade_cosseno(vetor_a: list, vetor_b: list):
    # ------------------------------------------------------------
    # Nesta parte transformamos os vetores que foram passados por
    # parâmetro em matrizes com 1 linha. Isto é necessário por causa
    # que a função cosine_similiarity foi desenhada para comparar
    # listas de vários vetores ao mesmo tempo, exigindo assim o formato
    # de matriz.
    # ------------------------------------------------------------
    vetor_a = [vetor_a]
    vetor_b = [vetor_b]

    # ------------------------------------------------------------
    # A função cosine_similarity do sklearn é utilizada para calcular
    # a similaridade do cosseno entre dois vetores.
    #
    # Ela mede a proximidade das direções de dois vetores em um
    # espaço multidimensional, no qual resultados próximos a 1
    # significam que os textos tem exatamente o mesmo sentido e
    # próximos a 0 significam que os textos não têm nenhuma relação
    # de assunto.
    #
    # O resultado retornado será uma matriz bidirecional do NumPy.
    # ------------------------------------------------------------
    similaridade = cosine_similarity(vetor_a, vetor_b)

    # ------------------------------------------------------------
    # Por fim, extraímos o valor da matriz, já que o resultado segue
    # o formato [[resultado]], e então retornamos esse valor.
    # ------------------------------------------------------------
    return similaridade[0][0]
#endregion

#region recuperar_chunks_relevantes (intermediária, )

# ------------------------------------------------------------
# Função: recuperar_chunks_relevantes
# ------------------------------------------------------------
# 
# ------------------------------------------------------------
def recuperar_chunks_relevantes(pergunta, quantidade=5):
    chunks = carregar_chunks_documentos()

    chunks, embeddings_chunks = gerar_embeddings_chunks(chunks)

    embedding_pergunta = gerar_embedding_pergunta(pergunta)

    similaridades = [
        calcular_similaridade_cosseno(embedding_pergunta, emb)
        for emb in embeddings_chunks
    ]

    resultados = []

    for i, chunk in enumerate(chunks):
        resultados.append({
            "id_chunk": chunk["id"],
            "nome_arquivo": chunk.get("arquivo_origem", ""),
            "texto": chunk["texto_chunk"],
            "similaridade": float(similaridades[i])
        })

    resultados_ordenados = sorted(
        resultados,
        key=lambda x: x["similaridade"],
        reverse=True
    )

    return resultados_ordenados[:quantidade]
#endregion

#region formatar_chunks_recuperados (intermediária, )

# ------------------------------------------------------------
# Função: formatar_chunks_recuperados
# ------------------------------------------------------------
# 
# ------------------------------------------------------------
def formatar_chunks_recuperados(chunks):
    texto_formatado = ""
    
    for trecho_num, chunk in enumerate(chunks):
        arquivo = chunk.get("nome_arquivo")
        texto_chunk = chunk.get("texto")
        
        texto_formatado += f"Trecho {trecho_num + 1}\nFonte: {arquivo}\nTexto: {texto_chunk}"
        
        if trecho_num != len(chunks) - 1:
            texto_formatado += "\n\n"
        
    return texto_formatado
#endregion

#region gerar_resposta_com_contexto (intermediária, envia pergunta e contexto para a LLM e retorna a resposta)

# ------------------------------------------------------------
# Função: gerar_resposta_com_contexto
# ------------------------------------------------------------
# Esta função recebe a pergunta do usuário e o contexto recuperado
# dos materiais.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque o RAG não deve simplesmente mandar a pergunta solta para
# a LLM.
#
# Ele deve mandar:
#
# 1. a pergunta do usuário;
# 2. os trechos relevantes recuperados dos documentos;
# 3. uma instrução dizendo para responder com base nesses trechos.
#
# Assim, a resposta final fica orientada pelos materiais de estudo,
# e não apenas pelo conhecimento geral do modelo.
# ------------------------------------------------------------
def gerar_resposta_com_contexto(pergunta: str, contexto: str) -> str:
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
            "Não encontrei trechos relevantes nos materiais para responder essa pergunta."
        )

    # --------------------------------------------------------
    # Agora montamos o prompt que será enviado para a LLM.
    #
    # Esse prompt contém:
    #
    # - uma instrução de comportamento;
    # - os trechos recuperados dos materiais;
    # - a pergunta original do usuário.
    #
    # Também deixamos claro que, se os trechos não forem suficientes,
    # a LLM deve dizer isso em vez de inventar uma resposta.
    # --------------------------------------------------------
    prompt = f"""
Você é o JARVIS Acadêmico, um assistente de estudos.

Responda à pergunta do usuário usando apenas ou principalmente os trechos fornecidos abaixo.

Se os trechos não forem suficientes para responder com segurança, diga que os materiais não contêm informação suficiente.

Trechos recuperados dos materiais:

{contexto}

Pergunta do usuário:

{pergunta}
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

#region consultar_material_rag (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: consultar_material_rag
# ------------------------------------------------------------
# Esta função executa o processo completo do RAG.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será cadastrada depois no tools.py como
# uma ferramenta disponível para a LLM.
#
# Ela faz o fluxo completo:
#
# 1. recebe a pergunta do usuário;
# 2. recupera os chunks mais relevantes;
# 3. formata esses chunks como contexto;
# 4. envia pergunta + contexto para o Gemma;
# 5. recebe a resposta gerada;
# 6. devolve a resposta final para o usuário.
# ------------------------------------------------------------
def consultar_material_rag(pergunta: str) -> str:
    # --------------------------------------------------------
    # Primeiro, recuperamos os chunks mais relevantes para a
    # pergunta do usuário.
    # --------------------------------------------------------
    chunks_relevantes = recuperar_chunks_relevantes(pergunta)

    # --------------------------------------------------------
    # Agora formatamos os chunks recuperados em um texto único.
    #
    # Esse texto será usado como contexto para a LLM.
    # --------------------------------------------------------
    contexto = formatar_chunks_recuperados(chunks_relevantes)

    # --------------------------------------------------------
    # Agora enviamos a pergunta e o contexto para a LLM gerar a
    # resposta final baseada nos materiais.
    # --------------------------------------------------------
    resposta = gerar_resposta_com_contexto(pergunta, contexto)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta final.
    #
    # Essa resposta será retornada para o tools.py e, depois, para
    # o main.py mostrar no chat.
    # --------------------------------------------------------
    return resposta

#endregion