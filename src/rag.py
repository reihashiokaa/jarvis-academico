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
#     "arquivo": "aula_embeddings.pdf",
#     "conteudo": "conteúdo extraído do arquivo..."
#   },
#   {
#     "arquivo": "resumo_rag.txt",
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
                "arquivo": caminho_doc.name,
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
