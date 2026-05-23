# JARVIS Acadêmico

O JARVIS Acadêmico é um assistente acadêmico desenvolvido em Python para apoiar estudantes na organização de compromissos, tarefas e consultas a materiais de estudo.

O sistema utiliza uma LLM compatível com a API da OpenAI, configurada para acessar o modelo Gemma fornecido para o trabalho. Além de responder mensagens comuns, o projeto também implementa tool calling, permitindo que a LLM escolha quando deve chamar funções internas do sistema.

## Funcionalidades

O projeto possui três funcionalidades principais:

1. consulta de agenda acadêmica;
2. gerenciamento de tarefas;
3. consulta a materiais de estudo com RAG.

## Agenda acadêmica

A agenda acadêmica permite consultar compromissos cadastrados no sistema.

As consultas disponíveis são:

- consultar compromissos por data específica;
- consultar compromissos de hoje;
- consultar compromissos de amanhã;
- consultar compromissos da semana atual.

Os dados da agenda ficam armazenados em:

```txt
data/agenda.json
```

Exemplos de uso no chat:

```txt
o que tenho hoje?
```

```txt
o que tenho amanhã?
```

```txt
quais compromissos tenho esta semana?
```

```txt
tenho algo em 2026-05-15?
```

## Lista de tarefas

A lista de tarefas permite ao usuário registrar e acompanhar atividades acadêmicas.

As funcionalidades disponíveis são:

- listar tarefas cadastradas;
- adicionar novas tarefas;
- concluir tarefas por descrição textual.

Os dados das tarefas ficam armazenados em:

```txt
data/tarefas.json
```

Exemplos de uso no chat:

```txt
liste minhas tarefas
```

```txt
adicione uma tarefa para revisar o projeto jarvis
```

```txt
conclua a tarefa de revisar o projeto jarvis
```

A conclusão de tarefas é feita por descrição textual. Isso significa que o usuário não precisa informar diretamente o ID da tarefa. O sistema usa a LLM para comparar a descrição fornecida com as tarefas cadastradas e identificar qual tarefa deve ser marcada como concluída.

## RAG

O projeto implementa RAG, que significa Retrieval-Augmented Generation.

Essa funcionalidade permite que o assistente responda perguntas com base nos materiais de estudo disponíveis no projeto.

Os materiais ficam armazenados em:

```txt
data/materiais
```

Formatos aceitos:

- `.txt`
- `.pdf`

O fluxo do RAG é:

1. carregar documentos da pasta `data/materiais`;
2. extrair o texto dos documentos;
3. dividir os textos em chunks;
4. gerar embeddings dos chunks;
5. gerar embedding da pergunta do usuário;
6. comparar a pergunta com os chunks;
7. recuperar os trechos mais relevantes;
8. enviar a pergunta e os trechos recuperados para a LLM;
9. gerar uma resposta baseada nos materiais.

Exemplos de uso no chat:

```txt
Explique regressão logística com base nos materiais
```

```txt
Explique o padrão Singleton com base nos materiais disponíveis
```

```txt
Quais são os principais pontos do padrão Adapter?
```

## Tool calling

O projeto utiliza tool calling para permitir que a LLM escolha quando uma função interna deve ser chamada.

O fluxo geral é:

1. o usuário digita uma mensagem no chat;
2. a LLM analisa a mensagem;
3. a LLM decide se alguma ferramenta deve ser usada;
4. o sistema executa a ferramenta escolhida;
5. a resposta da ferramenta é exibida ao usuário;
6. a chamada é registrada em log.

As ferramentas disponíveis são:

- `consultar_agenda_por_data`
- `consultar_agenda_hoje`
- `consultar_agenda_amanha`
- `consultar_agenda_semana_atual`
- `consultar_tarefas`
- `adicionar_tarefa`
- `concluir_tarefa_por_descricao`
- `consultar_material_rag`

## Logs

As chamadas de ferramentas são registradas no arquivo:

```txt
logs/tool_calls.jsonl
```

Cada registro contém:

- data e hora da chamada;
- nome da ferramenta chamada;
- entrada recebida;
- saída devolvida.

Esse registro permite verificar quais ferramentas foram acionadas durante a execução do sistema.

## Estrutura do projeto

```txt
jarvis-academico/
│
├── data/
│   ├── agenda.json
│   ├── tarefas.json
│   └── materiais/
│
├── logs/
│   └── tool_calls.jsonl
│
├── src/
│   ├── agenda.py
│   ├── tarefas.py
│   ├── rag.py
│   ├── tools.py
│   ├── logger.py
│   ├── llm_client.py
│   └── main.py
│
├── testes_terminal/
│
├── requirements.txt
├── README.md
└── .env
```

## Instalação

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta do projeto:

```bash
cd jarvis-academico
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No CMD:

```bash
.venv\Scripts\activate
```

No PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias para acessar a API da LLM.

Exemplo:

```txt
GEMMA_API_KEY=sua_chave_aqui
GEMMA_BASE_URL=url_da_api_aqui
GEMMA_MODEL=nome_do_modelo_aqui
```

O arquivo `.env` não deve ser enviado para o GitHub.

## Execução

Para iniciar o chat principal, rode:

```bash
python -m src.main
```

Depois disso, o sistema abrirá o chat no terminal.

Para encerrar o programa, digite:

```txt
sair
```

## Exemplos de uso

Mensagem comum:

```txt
olá
```

Consultar tarefas:

```txt
liste minhas tarefas
```

Adicionar tarefa:

```txt
adicione uma tarefa para revisar o projeto jarvis
```

Concluir tarefa:

```txt
conclua a tarefa de revisar o projeto jarvis
```

Consultar agenda de hoje:

```txt
o que tenho hoje?
```

Consultar agenda de amanhã:

```txt
o que tenho amanhã?
```

Consultar agenda da semana:

```txt
quais compromissos tenho esta semana?
```

Consultar materiais com RAG:

```txt
Explique regressão logística com base nos materiais
```

## Dependências

As principais bibliotecas utilizadas são:

- `openai`
- `python-dotenv`
- `pypdf`
- `sentence-transformers`
- `scikit-learn`
- `numpy`

As dependências completas estão listadas em:

```txt
requirements.txt
```

## Testes

O projeto possui arquivos com comandos de teste na pasta:

```txt
testes_terminal/
```

Esses arquivos contêm comandos para testar individualmente:

- agenda;
- tarefas;
- logger;
- tools;
- LLM;
- main;
- RAG.

Alguns exemplos de testes:

```bash
python -c "from src.agenda import consultar_agenda_hoje; print(consultar_agenda_hoje())"
```

```bash
python -c "from src.tarefas import consultar_tarefas; print(consultar_tarefas())"
```

```bash
python -c "from src.rag import consultar_material_rag; print(consultar_material_rag('Explique regressão logística com base nos materiais'))"
```

## IAs utilizadas

Durante o desenvolvimento do projeto, foram utilizadas as seguintes IAs:

- Gemma 12B, utilizado como modelo principal do assistente;
- ChatGPT, utilizado como apoio no desenvolvimento, explicação de conceitos, organização do código, depuração e documentação.

## Observações

A primeira execução do RAG pode demorar, pois o modelo de embeddings precisa ser carregado.

Também pode aparecer um aviso do Hugging Face informando que requisições estão sendo feitas sem autenticação. Esse aviso não impede o funcionamento do sistema, mas indica que o uso autenticado poderia oferecer limites melhores.

Caso a API da LLM esteja lenta ou instável, o sistema pode retornar uma mensagem de timeout controlado em vez de quebrar com erro no terminal.

## Autores

Projeto desenvolvido para a disciplina de Inteligência Artificial.

Integrantes:

- Amanda Ayumi Koga Kikuta
- Reinaldo Andrade Hashioka