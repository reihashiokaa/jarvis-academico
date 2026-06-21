# Avaliação do Sistema

Esta seção apresenta a avaliação do JARVIS Acadêmico com perguntas feitas ao sistema. O objetivo é verificar se o sistema consegue recuperar documentos relevantes, gerar respostas adequadas e lidar com diferentes tipos de perguntas.

## Critério de classificação

* Correta: a resposta está alinhada com os documentos recuperados e responde adequadamente à pergunta.
* Parcialmente correta: a resposta tem informações relevantes, mas está incompleta, genérica ou apresenta alguma imprecisão.
* Incorreta: a resposta não responde corretamente à pergunta, usa documentos inadequados ou apresenta informação errada.

## Perguntas avaliadas

### Pergunta 1

Pergunta:

O que é Inteligência Artificial?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 15, similaridade 0.709: trecho sobre a Inteligência Artificial como ramo da Ciência da Computação, seu objetivo de fazer computadores pensarem ou se comportarem de forma inteligente, áreas relacionadas e aplicações.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 11, similaridade 0.699: trecho introdutório sobre a origem da IA, sua relação com o raciocínio humano, subcampos da área e as quatro linhas de pensamento para definir Inteligência Artificial.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 19, similaridade 0.534: trecho de referências e resumo do artigo, com contexto geral sobre o estudo da IA e sua origem.

Resposta do sistema:

Inteligência Artificial (IA) é um ramo da Ciência da Computação cujo interesse é fazer com que os computadores pensem ou se comportem de forma inteligente. A IA também está relacionada com outras áreas científicas como psicologia, biologia, lógica matemática, linguística, engenharia e filosofia. Ela busca fornecer ao computador a habilidade de realizar funções que apenas o cérebro humano é capaz de resolver. A IA pode ser definida de várias formas, incluindo sistemas que pensam como seres humanos, que agem como seres humanos, que pensam racionalmente e que agem racionalmente.

Classificação:

Correta.

Justificativa:

A resposta está coerente com os documentos recuperados. Ela apresenta a definição central de Inteligência Artificial, menciona sua relação com outras áreas científicas e inclui as quatro linhas de pensamento citadas no material. Apesar de ser uma resposta resumida, ela cobre os principais pontos necessários para responder à pergunta.

### Pergunta 2

Pergunta:

Quais são as quatro linhas de pensamento da Inteligência Artificial?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 15, similaridade 0.741: trecho sobre a Inteligência Artificial como ramo da Ciência da Computação, áreas relacionadas e aplicações.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 11, similaridade 0.711: trecho que apresenta diretamente as quatro linhas de pensamento da Inteligência Artificial.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 12, similaridade 0.686: trecho que complementa a explicação sobre pensamento, comportamento e racionalidade.

Resposta do sistema:

As quatro linhas de pensamento da Inteligência Artificial são:

I. Sistemas que pensam como seres humanos.

II. Sistemas que atuam como seres humanos.

III. Sistemas que pensam racionalmente.

IV. Sistemas que atuam racionalmente.

O sistema também explicou que as linhas I e III se referem ao processo de pensamento e raciocínio, enquanto as linhas II e IV focam no comportamento. Além disso, indicou que as linhas I e II medem o sucesso em relação ao desempenho humano, enquanto as linhas III e IV se baseiam no conceito de racionalidade.

Classificação:

Correta.

Justificativa:

A resposta está correta porque recuperou documentos diretamente relacionados à pergunta e apresentou as quatro linhas de pensamento citadas no material. Além disso, a resposta não apenas listou as linhas, mas também explicou a diferença geral entre elas, usando informações coerentes com os trechos recuperados.

### Pergunta 3

Pergunta:

O que significa um sistema agir racionalmente?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 12, similaridade 0.665: trecho que explica a ideia de racionalidade na Inteligência Artificial e afirma que um sistema racional é aquele que “faz tudo certo” com os dados que possui.
* `Redes_neurais_artificiais_principios_bas.pdf`, chunk 31, similaridade 0.510: trecho sobre funções de ativação e aprendizagem de redes neurais. Esse trecho não está diretamente relacionado à pergunta.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 13, similaridade 0.459: trecho sobre a história da IA, Teste de Turing e sistemas baseados em conhecimento.

Resposta do sistema:

Um sistema é considerado agir racionalmente se “faz tudo certo”, com base nos dados que possui. Isso significa que o sistema toma decisões ou realiza ações que são ótimas ou ideais com relação ao contexto em que opera. O termo “racional” neste sentido compara o desempenho do sistema a um conceito ideal de racionalidade, em vez de simplesmente medir a fidelidade ao desempenho humano.

Classificação:

Correta.

Justificativa:

A resposta está correta porque explica o conceito de agir racionalmente conforme o principal documento recuperado. O sistema identificou que a racionalidade está relacionada a tomar decisões adequadas com base nos dados disponíveis. Apesar de um dos chunks recuperados não estar diretamente relacionado à pergunta, isso não prejudicou a resposta final.

### Pergunta 4

Pergunta:

Qual é a diferença entre sistemas que pensam como humanos e sistemas que pensam racionalmente?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 12, similaridade 0.678: trecho que explica a diferença entre abordagens centradas no ser humano e abordagens centradas na racionalidade, além de tratar do conceito de racionalidade.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 13, similaridade 0.491: trecho sobre a história da IA, Teste de Turing e sistemas baseados em conhecimento.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 19, similaridade 0.475: trecho de referências e resumo do artigo, com contexto geral sobre o estudo da IA.

Resposta do sistema:

Segundo os trechos fornecidos, sistemas que pensam como humanos e sistemas que pensam racionalmente diferem principalmente em seus critérios de sucesso e em sua abordagem filosófica.

Sistemas que pensam como humanos buscam medir seu sucesso comparando-se ao desempenho humano. Já sistemas que pensam racionalmente são avaliados em relação a um conceito ideal de racionalidade. Nesse caso, o objetivo não é apenas imitar o ser humano, mas aplicar princípios lógicos e matemáticos para chegar a decisões corretas.

O sistema também mencionou que existe uma tensão entre abordagens centradas nos seres humanos e abordagens centradas na racionalidade.

Classificação:

Correta.

Justificativa:

A resposta está coerente com os documentos recuperados. Ela diferencia corretamente a abordagem baseada no pensamento humano da abordagem baseada na racionalidade. Embora pudesse citar de forma mais direta as quatro linhas de pensamento apresentadas no material, a explicação responde adequadamente à pergunta.

### Pergunta 5

Pergunta:

O que é um agente inteligente?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 15, similaridade 0.574: trecho sobre Inteligência Artificial, áreas relacionadas, aplicações, sistemas especialistas e robótica.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 11, similaridade 0.532: trecho introdutório sobre IA, incluindo a ideia de construir entidades inteligentes e as quatro linhas de pensamento da Inteligência Artificial.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 12, similaridade 0.528: trecho que menciona sistemas que atuam racionalmente e associa Inteligência Computacional ao estudo do projeto de agentes inteligentes.

Resposta do sistema:

Um agente inteligente, conforme mencionado no texto fornecido, é definido como “A Inteligência Computacional é o estudo do projeto de agentes inteligentes.” Isso significa que um agente inteligente é um sistema projetado para agir racionalmente em um ambiente, tomando decisões com base em objetivos específicos e interagindo com seu ambiente através de percepção e ação. O objetivo desses sistemas é realizar tarefas de maneira eficiente e inteligente, muitas vezes utilizando técnicas de aprendizagem automática e tomada de decisão.

Classificação:

Parcialmente correta.

Justificativa:

A resposta está relacionada ao conteúdo recuperado, pois os documentos mencionam agentes inteligentes dentro da linha de sistemas que atuam racionalmente. Porém, os trechos recuperados não apresentam uma definição detalhada de agente inteligente com percepção, ação, ambiente e objetivos. Essa parte da resposta parece ter sido complementada com conhecimento geral da LLM. Por isso, a resposta é útil e coerente, mas não totalmente apoiada pelos documentos recuperados.

### Pergunta 6

Pergunta:

Como a Inteligência Artificial se relaciona com modelos computacionais?

Documentos recuperados:

* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 15, similaridade 0.750: trecho sobre a Inteligência Artificial como ramo da Ciência da Computação, suas áreas relacionadas e aplicações.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 11, similaridade 0.694: trecho introdutório sobre IA e suas quatro linhas de pensamento, incluindo a relação com modelos computacionais.
* `Inteligencia_Artificial_Conceitos_e_Apli.pdf`, chunk 12, similaridade 0.621: trecho que menciona sistemas que pensam racionalmente como o estudo das faculdades mentais pelo uso de modelos computacionais.

Resposta do sistema:

A Inteligência Artificial se relaciona com modelos computacionais através do estudo das faculdades mentais utilizando modelos computacionais. Isso significa que a IA utiliza modelos computacionais para estudar e simular processos mentais, permitindo uma análise mais precisa e detalhada desses processos.

Classificação:

Correta.

Justificativa:

A resposta está correta porque se baseia nos documentos recuperados, especialmente na definição de sistemas que pensam racionalmente. A resposta é breve, mas responde diretamente à pergunta e mantém coerência com o material.

### Pergunta 7

Pergunta:

Explique, com base nos materiais, o que é aprendizado de máquina.

Documentos recuperados:

* `What_are_embeddings.pdf`, chunk 138, similaridade 0.724: trecho sobre sistemas de aprendizado de máquina, incluindo dados de entrada, engenharia e seleção de características, construção do modelo, disponibilização do modelo e tipos de tarefas de machine learning.
* `What_are_embeddings.pdf`, chunk 142, similaridade 0.622: trecho sobre sistemas de recomendação e tarefas de aprendizado de máquina relacionadas a recomendação e recuperação de informação.
* `What_are_embeddings.pdf`, chunk 127, similaridade 0.615: trecho de sumário do documento, com tópicos sobre formulação de problemas de machine learning, características, vetores numéricos, Word2Vec, redes neurais e Transformers.

Resposta do sistema:

Baseado nos materiais fornecidos, aprendizado de máquina refere-se ao processo de construção de sistemas que podem aprender com dados sem serem explicitamente programados para realizar uma tarefa específica. O processo geral envolve entrada de dados, engenharia e seleção de características, construção do modelo e serviço do modelo. A resposta também explicou que o aprendizado de máquina pode ser aplicado a tarefas como previsão, recomendação, aprendizado supervisionado, não supervisionado e por reforço.

Classificação:

Correta.

Justificativa:

A resposta está correta porque usa os principais pontos recuperados do material. Ela explica o fluxo de um sistema de aprendizado de máquina e apresenta os tipos de tarefas mencionados nos documentos. Apesar de um dos chunks recuperados ser apenas um sumário, os demais trechos foram suficientes para gerar uma resposta adequada.


### Pergunta 8

Pergunta:

O que são embeddings?

Documentos recuperados:

* `What_are_embeddings.pdf`, chunk 130, similaridade 0.633: trecho que define embeddings como dados transformados em matrizes n-dimensionais para uso em computações de deep learning, além de explicar vetores, tensores, grafos e compressão da informação.
* `What_are_embeddings.pdf`, chunk 126, similaridade 0.567: trecho introdutório que apresenta embeddings como representações numéricas de características de machine learning usadas como entrada para modelos de deep learning.
* `What_are_embeddings.pdf`, chunk 132, similaridade 0.513: trecho que explica embeddings em espaços multidimensionais e sua utilidade para comparar itens, como palavras, em um espaço compartilhado.

Resposta do sistema:

Em termos simples, embeddings são representações numéricas de características de machine learning usadas como entrada para modelos de aprendizado profundo. Eles transformam dados multimodais em representações mais fáceis de computação intensiva, geralmente na forma de vetores, tensores ou grafos. O processo de criação de embeddings comprime a informação de entrada para uso em tarefas de aprendizado de máquina, como resumir documentos ou identificar etiquetas para postagens. Além disso, embeddings podem criar um espaço de representação específico para os dados em que foram treinados e também generalizar para outras tarefas e domínios por meio do aprendizado de transferência.

Classificação:

Correta.

Justificativa:

A resposta está correta porque recupera documentos diretamente relacionados à pergunta e explica embeddings de forma compatível com o material. A resposta menciona representação numérica, vetores, compressão de informação, uso em machine learning e espaço de embeddings, que são pontos presentes nos trechos recuperados.


### Pergunta 9

Pergunta:

Explique o que é RAG.

Documentos recuperados:

* `Redes_neurais_artificiais_principios_bas.pdf`, chunk 34, similaridade 0.339: trecho sobre redes neurais, propagação, retropropagação, benefícios e desvantagens das RNAs.
* `What_are_embeddings.pdf`, chunk 130, similaridade 0.326: trecho sobre embeddings, vetores, tensores, compressão de informação e espaço de embeddings.
* `What_are_embeddings.pdf`, chunk 178, similaridade 0.299: trecho sobre BERT, GPT, embeddings em produção e modelos de linguagem.

Resposta do sistema:

Os trechos fornecidos não contêm informações sobre o que é RAG. Portanto, não posso fornecer uma explicação baseada nestes materiais específicos.

Classificação:

Parcialmente correta.

Justificativa:

A resposta não explica o que é RAG, portanto não atende completamente à pergunta. Porém, o sistema agiu de forma adequada ao reconhecer que os documentos recuperados não continham informação suficiente sobre o tema, evitando gerar uma resposta sem base nos materiais. O problema principal está na recuperação ou na ausência de material sobre RAG na base de documentos.


### Pergunta 10

Pergunta:

Qual é a diferença entre recuperação de informação e geração de resposta?

Documentos recuperados:

* `Regressão Logística_e_suas_Aplicações.pdf`, chunk 43, similaridade 0.533: trecho sobre mineração de dados, regressão logística e análise de dados de resposta categórica.
* `Redes_neurais_artificiais_principios_bas.pdf`, chunk 34, similaridade 0.525: trecho sobre redes neurais, propagação, retropropagação e benefícios das RNAs.
* `Regressão Logística_e_suas_Aplicações.pdf`, chunk 48, similaridade 0.510: trecho sobre mineração de dados, tarefas de previsão e definição de regressão logística.

Resposta do sistema:

Os trechos fornecidos não contêm informação suficiente para explicar a diferença entre recuperação de informação e geração de resposta.

Classificação:

Parcialmente correta.

Justificativa:

A resposta não explica a diferença solicitada, portanto não atende completamente à pergunta. Porém, o sistema foi adequado ao reconhecer que os documentos recuperados não continham informação suficiente sobre o tema. O problema principal está na recuperação de documentos pouco relacionados e/ou na ausência de materiais específicos sobre recuperação de informação e geração de resposta na base.

# Análise de Erros

Durante a avaliação do sistema, foram identificadas algumas limitações relacionadas à recuperação de documentos, à geração de respostas e à cobertura da base de conhecimento.

## Falha 1

Tipo:

Recuperação.

Causa:

Em algumas perguntas, o sistema recuperou chunks que não estavam diretamente relacionados ao tema principal da pergunta. Por exemplo, na pergunta sobre agir racionalmente, um dos documentos recuperados tratava de redes neurais e funções de ativação, embora a pergunta fosse sobre racionalidade em Inteligência Artificial. Mesmo que a resposta final tenha sido correta, houve ruído na recuperação.

Possível solução:

Melhorar o processo de recuperação com um filtro mínimo de similaridade, reordenação dos chunks recuperados ou uso de metadados dos documentos. Outra possibilidade é descartar automaticamente trechos com baixa relação semântica antes de enviar o contexto para a LLM.

---

## Falha 2

Tipo:

Geração.

Causa:

Na pergunta sobre agente inteligente, a resposta foi coerente, mas incluiu explicações que não estavam totalmente explícitas nos documentos recuperados, como percepção, ação, ambiente e objetivos. Isso indica que a LLM complementou a resposta com conhecimento geral, indo além dos trechos disponíveis.

Possível solução:

Ajustar o prompt do RAG para deixar mais claro que a resposta deve se limitar aos documentos recuperados. Quando a informação não estiver explícita nos documentos, o sistema deve informar essa limitação em vez de completar com conhecimento geral.

---

## Falha 3

Tipo:

Cobertura da base de conhecimento / recuperação.

Causa:

Nas perguntas sobre RAG e sobre a diferença entre recuperação de informação e geração de resposta, o sistema não recuperou documentos específicos sobre esses temas. Em vez disso, recuperou trechos sobre redes neurais, embeddings ou regressão logística. Como consequência, o sistema não conseguiu responder diretamente às perguntas.

Possível solução:

Adicionar à pasta de materiais documentos específicos sobre RAG, recuperação de informação, geração de respostas e funcionamento de sistemas baseados em LLM. Também seria útil organizar melhor os documentos por tema ou adicionar metadados para ajudar o sistema a recuperar materiais mais adequados.
