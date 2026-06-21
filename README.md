# JARVIS Acadêmico

JARVIS Acadêmico é um assistente acadêmico em Python com suporte a LLM, tool calling, gerenciamento de agenda, tarefas, consulta a materiais de estudo com RAG e funcionalidades de apoio ao aprendizado.

O sistema foi desenvolvido para permitir que o usuário interaja em linguagem natural pelo bot do Telegram, enquanto a LLM decide quando deve responder diretamente ou acionar uma ferramenta interna do projeto.

## Funcionalidades

* Chat acadêmico com LLM;
* Consulta de agenda acadêmica;
* Gerenciamento de tarefas;
* Conclusão de tarefas por descrição textual;
* Consulta a materiais com RAG;
* Geração de exercícios com base nos materiais;
* Active recall com pergunta, resposta do usuário e avaliação automática;
* Tool calling com decisão feita pela LLM;
* Registro de chamadas de ferramentas em log;
* Avaliação do sistema com perguntas, documentos recuperados, respostas e análise de erros.

## Estrutura do projeto

```txt
jarvis-academico/
│
├── data/
│   ├── agenda.json
│   ├── tarefas.json
│   ├── active_recall.json
│   └── materiais/
│
├── logs/
│   └── tool_calls.jsonl
│
├── src/
│   ├── agenda.py
│   ├── aprendizado.py
│   ├── tarefas.py
│   ├── rag.py
│   ├── tools.py
│   ├── logger.py
│   ├── llm_client.py
│   ├── telegram.py
│   └── main.py
│
├── testes_terminal/
│
├── AVALIACAO_SISTEMA.md
├── requirements.txt
├── README.md
└── .env
```

O arquivo `data/active_recall.json` é usado para guardar temporariamente a sessão ativa de active recall. Ele é gerado durante a execução do sistema.

## Requisitos

* Python 3.10 ou superior;
* Ambiente virtual Python;
* Chave de acesso a uma API compatível com OpenAI;
* Arquivos de materiais em `.pdf` ou `.txt` para uso do RAG;
* Conta ativa no Telegram para interação com o bot;
* Acesso ao Telegram Web, aplicativo desktop ou mobile para envio de mensagens ao bot.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/reihashiokaa/jarvis-academico
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

Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias para acessar a LLM e o bot do Telegram.

Exemplo:

```txt
GEMMA_API_KEY=sua_chave_aqui
GEMMA_BASE_URL=url_da_api_compativel_openai_aqui
GEMMA_MODEL=nome_do_modelo_aqui

TOKEN_TELEGRAM=token_telegram_aqui
```

As variáveis mantêm o prefixo `GEMMA_` por compatibilidade com o código, mas podem apontar para outra API compatível com OpenAI.

O arquivo `.env` não deve ser versionado no Git.

## Execução

Para iniciar o programa:

```bash
python -m src.main
```

Quando a mensagem "Bot integrado e rodando..." aparecer, o bot já estará disponível para interação no Telegram.

Para encerrar o programa, digite o seguinte comando na conversa com o bot:

```txt
sair
```

## Como acessar o bot no Telegram

Após executar o projeto, aguarde a mensagem "Bot integrado e rodando...".

Em seguida, acesse o Telegram pelo aplicativo ou pelo navegador via `https://web.telegram.org`.

Para localizar o bot, é possível buscá-lo de duas formas:

1. Pelo link:

```txt
https://t.me/jarvisAcademico_bot
```

2. Pelo identificador:

```txt
@jarvisAcademico_bot
```

Encontrado o bot, clique em `Iniciar` ou digite o comando `/start`.

Após isso, o bot já estará pronto para responder e processar solicitações.

## Agenda acadêmica

A agenda permite consultar compromissos cadastrados em `data/agenda.json`.

Consultas disponíveis:

* compromissos de hoje;
* compromissos de amanhã;
* compromissos da semana atual;
* compromissos por data específica.

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

* listar tarefas;
* adicionar tarefas;
* concluir tarefas por descrição textual.

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

* `.pdf`
* `.txt`

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
Explique o que são embeddings.
```

```txt
O que é Inteligência Artificial?
```

## Melhorias de aprendizado

O projeto implementa funcionalidades voltadas ao apoio ao aprendizado do usuário.

As melhorias implementadas são:

* Geração de exercícios com base nos materiais de estudo;
* Perguntas ao usuário no formato de active recall.

### Geração de exercícios

A geração de exercícios permite que o usuário solicite uma lista de questões sobre um tema relacionado aos materiais carregados no sistema.

O sistema usa o RAG para recuperar trechos relevantes dos materiais e, em seguida, envia esse contexto para a LLM gerar exercícios com respostas.

Exemplo de uso:

```txt
gere exercícios sobre Inteligência Artificial
```

ou:

```txt
gere 5 exercícios sobre regressão logística
```

### Active recall

A funcionalidade de active recall é interativa.

Nesse fluxo, o sistema faz uma pergunta ao usuário, aguarda a resposta e depois avalia o desempenho.

Fluxo geral:

1. O usuário pede para ser testado sobre um tema;
2. O sistema recupera trechos relevantes dos materiais com RAG;
3. A LLM gera uma pergunta e uma resposta esperada;
4. O sistema apresenta apenas a pergunta ao usuário;
5. O usuário responde usando o formato `resposta: ...`;
6. O sistema compara a resposta do usuário com a resposta esperada;
7. O sistema devolve uma avaliação com classificação, feedback, resposta ideal e sugestão de revisão.

Exemplo de uso:

```txt
me faça uma pergunta sobre Inteligência Artificial
```

Depois que o sistema fizer a pergunta, o usuário pode responder:

```txt
resposta: minha resposta aqui
```

Essa funcionalidade atende ao requisito de melhoria de aprendizado interativa, pois o sistema pergunta, recebe a resposta do usuário e realiza uma avaliação.

## Tool calling

O sistema utiliza tool calling para permitir que a LLM selecione ferramentas internas conforme a intenção do usuário.

Ferramentas disponíveis:

* `consultar_agenda_por_data`
* `consultar_agenda_hoje`
* `consultar_agenda_amanha`
* `consultar_agenda_semana_atual`
* `consultar_tarefas`
* `adicionar_tarefa`
* `concluir_tarefa_por_descricao`
* `consultar_material_rag`
* `gerar_exercicios`
* `iniciar_active_recall`
* `responder_active_recall`

## Avaliação do sistema

A avaliação do sistema está documentada no arquivo:

```txt
AVALIACAO_SISTEMA.md
```

Esse documento contém:

* 10 perguntas feitas ao sistema;
* documentos recuperados pelo RAG;
* resposta gerada pela LLM;
* classificação da resposta como correta, parcialmente correta ou incorreta;
* análise de erros identificados durante a avaliação.

A avaliação mostrou que o sistema responde melhor quando os documentos recuperados estão diretamente relacionados à pergunta. Também foram observadas limitações quando a base de conhecimento não possui material específico sobre o tema solicitado.

## Logs

As chamadas de ferramentas são registradas em:

```txt
logs/tool_calls.jsonl
```

Cada registro contém:

* data e hora;
* ferramenta chamada;
* entrada recebida;
* saída devolvida.

## Testes

Os comandos de teste estão organizados na pasta:

```txt
testes_terminal/
```

Os arquivos dessa pasta incluem testes para:

* agenda;
* tarefas;
* logger;
* tools;
* LLM;
* main;
* RAG;
* geração de exercícios;
* active recall.

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

```bash
python -c "from src.aprendizado import iniciar_active_recall; print(iniciar_active_recall('Inteligência Artificial'))"
```

## Dependências principais

* `openai`
* `python-dotenv`
* `pypdf`
* `sentence-transformers`
* `scikit-learn`
* `numpy`

As dependências completas estão em `requirements.txt`.

## IAs utilizadas

Durante o desenvolvimento do projeto, foram utilizadas as seguintes IAs:

* Qwen2.5-14B-Instruct-AWQ: modelo usado pelo assistente por meio de API compatível com OpenAI;
* ChatGPT: apoio ao desenvolvimento, depuração, organização do código, documentação e revisão das funcionalidades.

## Observações

A primeira execução do RAG pode ser mais lenta devido ao carregamento do modelo de embeddings.

Em alguns ambientes, pode aparecer um aviso do Hugging Face sobre requisições não autenticadas. Esse aviso não impede a execução do sistema.

Caso a API da LLM esteja lenta ou instável, o sistema possui tratamento de timeout para evitar encerramento inesperado.

## Autores

Projeto desenvolvido para a disciplina de Inteligência Artificial.

Integrantes:

* Amanda Ayumi Koga Kikuta
* Reinaldo Andrade Hashioka
