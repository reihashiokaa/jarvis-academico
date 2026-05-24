# DATASET

Este dataset foi construído com o objetivo de fornecer uma base de conhecimento para um sistema de Retrieval-Augmented Generation (RAG), focado em conceitos de Inteligência Artificial e Aprendizado de Máquina.

## Estrutura

Os documentos estão armazenados na pasta `/data/materiais` do repositório.

Cada arquivo corresponde a um documento individual utilizado como fonte para a funcionalidade do RAG.

## Descrição dos documentos

### Regressão Logística e suas Aplicações
- Origem: UFMA (TCC)
- Tipo: Acadêmico
- Limitações: escopo restrito, poucos exemplos, possível desatualização

### Ranking de Dimensiones en Vectores Densos para Recuperación Eficiente
- Origem: Conferência JAIIO
- Tipo: Artigo científico
- Limitações: conteúdo em espanhol, altamente técnico, problema específico

### What are embeddings
- Origem: Blog técnico (https://vickiboykis.com/what_are_embeddings/)
- Tipo: Explicativo
- Limitações: conteúdo em inglês, simplificado, possível viés do autor

### Redes Neurais Artificiais: Princípios Básicos
- Origem: Artigo acadêmico
- Tipo: Científico introdutório
- Limitações: conteúdo introdutório, possível desatualização

### Inteligência Artificial: Conceitos e Aplicações
- Origem: Revista Olhar Científico
- Tipo: Artigo científico
- Limitações: conteúdo muito geral, pouca profundidade, possível desatualização

### Regressão Linear Simples
- Origem: USP (IME)
- Tipo: Material didático
- Limitações: exemplos simplificados, cobertura limitada

### Deep Learning
- Origem: UFMG
- Tipo: Material didático
- Limitações: conteúdo resumido, dependente de contexto

### Regressão Logística (gerado por IA)
- Origem: Conteúdo gerado por Inteligência Artificial
- Tipo: Texto sintético
- Limitações: possíveis erros, alucinações, sem fonte, superficial, viés do modelo

## Estratégia

A estratégia de chunking adotada divide os documentos em trechos de 500 palavras com sobreposição de 100 palavras, preservando o contexto entre partes consecutivas e reduzindo a perda de informação relevante. Inicialmente, foi utilizada uma abordagem baseada em tokens de caracteres. No entanto, foi observado um problema na recuperação, em que o RAG priorizava a ocorrência de termos em vez da similaridade semântica. Após a mudança para chunking por palavras, houve melhora significativa na recuperação semântica dos trechos. Além disso, durante a busca utilizou-se Top-K igual a 5, selecionando os cinco chunks mais relevantes. Essa abordagem melhorou a qualidade das respostas ao equilibrar o contexto e a relevância, embora limitações como conteúdo técnico, escopo restrito ou idioma dos documentos ainda possam impactar o desempenho do sistema.