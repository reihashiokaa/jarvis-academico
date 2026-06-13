#region explicação do arquivo

# ============================================================
# Arquivo: aprendizado.py
# ------------------------------------------------------------
# Este arquivo é responsável por lidar com as funcionalidades
# voltadas ao aprendizado.
#
# A ideia principal dessas funcionalidades é permitir que o
# assistente gere exercícios com base nos materiais de estudo
# carregados no projeto, como PDFs, textos e anotações.
#
# A lógica geral deste arquivo é:
#
# 1. enviar tema com contexto recuperado a partir das funções
# de RAG, importadas do arquivo rag.py, para a LLM;
# 2. devolver uma lista de exercícios com gabarito baseada
# nos materiais.
#
# A organização das funções segue o padrão usado no projeto:
#
# gerar_...
#   -> gera prompts ou respostas.
#
# consultar_...
#   -> executa o processo completo e devolve uma resposta pronta.
#
# A função final deste arquivo é:
#
# gerar_exercicios(tema, qtde)
#
# Essa função será cadastrada no tools.py como ferramenta
# disponível para tool calling.
# ============================================================
#endregion

#region importações
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


# ------------------------------------------------------------
# Importamos as funções recuperar_chunks_relevantes,
# formatar_chunks_recuperados.
#
# Essas funções estão no arquivo rag.py são responsáveis por
# recuperar chunks (trechos) relevantes a partir dos materiais
# disponíveis no projeto e formatar esses chunks recuperados
# tornando-os mais legíveis e organizados.
# ------------------------------------------------------------
from src.rag import recuperar_chunks_relevantes, formatar_chunks_recuperados
#endregion

#region gerar_exercicios_com_contexto (intermediária, envia o tema e contexto para a LLM e retorna a resposta)

# ------------------------------------------------------------
# Função: gerar_exercicios_com_contexto
# ------------------------------------------------------------
# Esta função recebe o tema decidido pelo usuário e o contexto
# recuperado dos materiais.
#
# Esta é uma função intermediária.
#
# Isso significa que ela ajuda o sistema por dentro, mas não será
# chamada diretamente pelo usuário final.
#
# Por que precisamos desta função?
#
# Porque não devemos simplesmente mandar a solicitação do usuário
# solta para a LLM.
#
# Ele deve mandar:
#
# 1. o tema do usuário;
# 2. os trechos relevantes recuperados dos documentos;
# 3. a quantidade de exercícios que deverão ser gerados;
# 4. uma instrução dizendo para gerar exercícios com base nesses
# trechos.
#
# Assim, os exercícios gerados ficam orientados pelos materiais de estudo,
# e não apenas pelo conhecimento geral do modelo.
# ------------------------------------------------------------
def gerar_exercicios_com_contexto(tema:str, contexto:str, qtde):
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
            "Não encontrei trechos relevantes nos materiais para gerar exercícios sobre esse tema."
        )
    
    prompt = f"""
    Você é o JARVIS Acadêmico, um assistente de estudos.

    Gere exercícios com resposta para estudo, usando como referência apenas ou principalmente os trechos fornecidos abaixo.
    A quantidade de exercícios será definida pelo usuário. Se não for específicado nenhuma quantidade, gere no mínimo cinco (5) exercícios.

    Trechos recuperados dos materiais:

    {contexto}

    Tema (conteúdo) pedido pelo usuário:

    {tema}

    Quantidade de exercícios:

    {qtde}
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

#region gerar_exercicios (FINAL, será uma ferramenta)

# ------------------------------------------------------------
# Função: gerar_exercicios
# ------------------------------------------------------------
# Esta função executa o processo completo para gerar exercícios.
#
# Esta é uma função FINAL.
#
# Isso significa que ela será cadastrada depois no tools.py como
# uma ferramenta disponível para a LLM.
#
# Ela faz o fluxo completo:
#
# 1. recebe o tema do usuário;
# 2. recupera os chunks mais relevantes;
# 3. formata esses chunks como contexto;
# 4. envia tema + contexto + qtde para o Gemma;
# 5. recebe os exercícios gerados;
# 6. devolve a resposta final para o usuário.
# ------------------------------------------------------------
def gerar_exercicios(tema: str, qtde:int=None):
    # --------------------------------------------------------
    # Recupera os chunks (trechos) releventas sobre o tema a
    # partir dos materiais de estudo.
    # --------------------------------------------------------
    chunks_relevantes = recuperar_chunks_relevantes(tema)

    # --------------------------------------------------------
    # Formata os chunks recuperados, de forma que fique organizado
    # e estruturado em uma única string.
    # --------------------------------------------------------
    contexto = formatar_chunks_recuperados(chunks_relevantes)

    # --------------------------------------------------------
    # Gera os exercícios com base no tema solicitado pelo usuário,
    # no contexto recuperado e com base na quantidade solicitada.
    # --------------------------------------------------------
    resposta = gerar_exercicios_com_contexto(tema, contexto, qtde)

    # --------------------------------------------------------
    # Por fim, devolvemos a resposta gerada pela LLM.
    # --------------------------------------------------------
    return resposta
#endregion