# JARVIS Acadêmico

JARVIS Acadêmico é um assistente acadêmico em Python com suporte a LLM, tool calling, gerenciamento de agenda, tarefas e consulta a materiais de estudo com RAG.

O sistema foi desenvolvido para permitir que o usuário interaja em linguagem natural pelo terminal, enquanto a LLM decide quando deve responder diretamente ou acionar uma ferramenta interna do projeto.

## Funcionalidades

- Chat acadêmico com LLM;
- Consulta de agenda acadêmica;
- Gerenciamento de tarefas;
- Conclusão de tarefas por descrição textual;
- Consulta a materiais com RAG;
- Tool calling com decisão feita pela LLM;
- Registro de chamadas de ferramentas em log.

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

## Requisitos

- Python 3.10 ou superior;
- Ambiente virtual Python;
- Chave de acesso à API compatível com OpenAI;
- Arquivos de materiais em `.pdf` ou `.txt` para uso do RAG.

## Instalação

Clone o repositório:

```bash
git clone <https://github.com/reihashiokaa/jarvis-academico>
```

Acesse a pasta do projeto:

```bash
cd jarvis-academico
```

Crie o ambiente virtual:

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

## Configuração

Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias para acessar a LLM.

Exemplo:

```txt
GEMMA_API_KEY=sua_chave_aqui
GEMMA_BASE_URL=url_da_api_aqui
GEMMA_MODEL=nome_do_modelo_aqui
```

O arquivo `.env` não deve ser versionado no Git.

## Execução

Para iniciar o assistente:

```bash
python -m src.main
```

Para encerrar o chat:

```txt
sair
```

## Agenda acadêmica

A agenda permite consultar compromissos cadastrados em `data/agenda.json`.

Consultas disponíveis:

- compromissos de hoje;
- compromissos de amanhã;
- compromissos da semana atual;
- compromissos por data específica.

Exemplos:

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

## Tarefas

As tarefas são armazenadas em `data/tarefas.json`.

Funcionalidades disponíveis:

- listar tarefas;
- adicionar tarefas;
- concluir tarefas por descrição textual.

Exemplos:

```txt
liste minhas tarefas
```

```txt
adicione uma tarefa para revisar o projeto jarvis
```

```txt
conclua a tarefa de revisar o projeto jarvis
```

A conclusão por descrição textual permite que o usuário não precise informar diretamente o ID da tarefa. O sistema usa a LLM para identificar a tarefa correspondente e, em seguida, marca a tarefa como concluída.

## RAG

O projeto implementa RAG para responder perguntas com base nos materiais armazenados em:

```txt
data/materiais
```

Formatos suportados:

- `.pdf`
- `.txt`

Fluxo geral do RAG:

1. Carregamento dos documentos;
2. Extração de texto;
3. Divisão em chunks;
4. Geração de embeddings;
5. Recuperação dos chunks mais relevantes;
6. Montagem do contexto;
7. Envio da pergunta e do contexto para a LLM;
8. Geração da resposta final.

Exemplos:

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

O sistema utiliza tool calling para permitir que a LLM selecione ferramentas internas conforme a intenção do usuário.

Ferramentas disponíveis:

- `consultar_agenda_por_data`
- `consultar_agenda_hoje`
- `consultar_agenda_amanha`
- `consultar_agenda_semana_atual`
- `consultar_tarefas`
- `adicionar_tarefa`
- `concluir_tarefa_por_descricao`
- `consultar_material_rag`

## Logs

As chamadas de ferramentas são registradas em:

```txt
logs/tool_calls.jsonl
```

Cada registro contém:

- data e hora;
- ferramenta chamada;
- entrada recebida;
- saída devolvida.

## Testes

Os comandos de teste estão organizados na pasta:

```txt
testes_terminal/
```

Os arquivos dessa pasta incluem testes para:

- agenda;
- tarefas;
- logger;
- tools;
- LLM;
- main;
- RAG.

Exemplos:

```bash
python -c "from src.agenda import consultar_agenda_hoje; print(consultar_agenda_hoje())"
```

```bash
python -c "from src.tarefas import consultar_tarefas; print(consultar_tarefas())"
```

```bash
python -c "from src.rag import consultar_material_rag; print(consultar_material_rag('Explique regressão logística com base nos materiais'))"
```

## Dependências principais

- `openai`
- `python-dotenv`
- `pypdf`
- `sentence-transformers`
- `scikit-learn`
- `numpy`

As dependências completas estão em `requirements.txt`.

## IAs utilizadas

Durante o desenvolvimento do projeto, foram utilizadas as seguintes IAs:

- Gemma 12B: modelo principal usado pelo assistente;
- ChatGPT: apoio ao desenvolvimento, depuração, organização do código, documentação e revisão das funcionalidades.

## Observações

A primeira execução do RAG pode ser mais lenta devido ao carregamento do modelo de embeddings.

Em alguns ambientes, pode aparecer um aviso do Hugging Face sobre requisições não autenticadas. Esse aviso não impede a execução do sistema.

Caso a API da LLM esteja lenta ou instável, o sistema possui tratamento de timeout para evitar encerramento inesperado.

## Autores

Projeto desenvolvido para a disciplina de Inteligência Artificial.

Integrantes:

- Amanda Ayumi Koga Kikuta
- Reinaldo Andrade Hashioka
