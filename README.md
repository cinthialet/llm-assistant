# LLM Assistant - PoC com Tool Calling

Assistente de IA com capacidade de identificar quando responder diretamente e quando acionar ferramentas externas.

## Ferramentas Disponíveis

| Ferramenta      | Descrição                                                                       |
| --------------- | ------------------------------------------------------------------------------- |
| **Calculadora** | Operações matemáticas (soma, subtração, multiplicação, divisão, potência, etc.) |
| **Clima**       | Consulta clima atual de qualquer cidade via [wttr.in](https://wttr.in)          |
| **Cripto**      | Consulta preço histórico de criptomoedas via API da Binance                     |

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)
- Chave de API da OpenAI

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/cinthialet/llm-assistant.git
cd llm-assistant
```

2. Crie o arquivo `.env` na raiz do projeto:

```bash
OPENAI_API_KEY=sua-chave-aqui
LANGSMITH_API_KEY=your-langsmith-api-key-here
LANGSMITH_PROJECT=llm-assistant # nome do projeto no langsmith
LANGSMITH_TRACING=true
```

> Obs: A api key da OpenAI é necessária para o projeto funcionar. A api key do Langsmith é opcional, mas adiciona funcionalidade de monitoramento e observabilidade.

3. Instale as dependências com uv:

```bash
uv sync
```

## Como Executar

### Modo Interativo (faça suas perguntas)

```bash
uv run python main.py
```

### Modo de Testes (executa uma série de perguntas para testar as funcionalidades do assistente)

```bash
uv run python main.py --test
```

## Lógica de Implementação

### Arquitetura

```
llm-assistant/
├── main.py                 # Ponto de entrada (interativo e testes)
├── src/
│   ├── agent/
│   │   └── assistant.py    # Criação do agente react LangGraph
│   ├── prompts/
│   │   └── system.py       # System prompt do assistente
│   ├── tools/
│   │   ├── calculator.py   # Ferramenta de cálculo
│   │   ├── weather.py      # Ferramenta de clima
│   │   └── crypto.py       # Ferramenta de cripto
│   └── test_demo.py        # Conjunto de testes
├── pyproject.toml
└── .env
```

### Stack Tecnológica

- **LangGraph**: Framework para criação de agentes com `create_react_agent`.
- **LangChain OpenAI**: Wrapper para comunicação com a API da OpenAI.
- **LangSmith** (opcional): Observabilidade e tracing das chamadas - monitoramento de tokens, custo, latência por chamada e acompanhamento passo a passo da execução do agente.

### Modelo Utilizado

O projeto utiliza o **gpt-5-mini** como modelo. Foi escolhido um modelo menor pois o assistente não possui grande complexidade - as tarefas são diretas (cálculos, consultas de API) e não requerem raciocínio avançado. Isso resulta em menor custo e latência mantendo a qualidade necessária para tool calling.

### Como Funciona o Tool Calling

1. O usuário faz uma pergunta
2. O LLM analisa a pergunta e decide:
   - Se for conhecimento geral → responde diretamente
   - Se for cálculo → chama `calculator`
   - Se for sobre clima → chama `get_weather`
   - Se for sobre cripto → chama `get_crypto_price`
3. Se uma ferramenta foi chamada, o resultado é processado e formatado na resposta final. Há guardrails para evitar alucinação e prints para comprovar a execução das ferramentas.

### Validação contra Alucinação

As ferramentas incluem validações para evitar respostas inventadas:

- **Calculadora**: Só aceita expressões matemáticas válidas
- **Clima**: Compara a cidade informada com a retornada pela API (evita match de cidades inexistentes com cidades similares existentes)
- **Cripto**: Valida se o par existe na Binance antes de retornar dados

## O que Aprendi

- **Robustez dos modelos modernos**: Os modelos de LLM conseguem traduzir a linguagem natural da pergunta do usuário para os parâmetros das funções das ferramentas de forma confiável, sem necessidade de intervenção com código;
- **Importância do monitoramento**: LangSmith é essencial para acompanhar performance, latência e custos das chamadas em produção; além de mostrar o passo a passo da execução do agente, facilitando debugar problemas.
- **Error handling nas ferramentas**: Um bom tratamento de erros nas ferramentas ajuda o agente a lidar com falhas e evita que ele alucine uma resposta quando algo dá errado;
- **Guardrails no prompt**: Instruções claras no system prompt (como "NUNCA invente informações" e "NUNCA faça perguntas de acompanhamento") ajudam a controlar o comportamento do agente e manter respostas consistentes sem alucinar.

## O que Faria Diferente com Mais Tempo

- **Streaming**: Implementar respostas em streaming para feedback visual mais rápido
- **Histórico de conversa**: Manter contexto entre perguntas (atualmente cada pergunta é independente, não há memória)
- **Mais ferramentas**: Integrar APIs como Wikipedia, busca na web, tradução
- **Interface web**: Criar um frontend simples com Streamlit ou similar para interação mais amigável do usuário
- **Construir um Knowledge Base**: Criar um banco de conhecimento para o assistente usar informações específicar através de uma pipeline RAG (retrieval augmented generation).

## Observabilidade (Opcional)

Para habilitar o LangSmith e visualizar traces das chamadas:

1. Crie uma conta em [smith.langchain.com](https://smith.langchain.com)
2. Adicione ao `.env`:

```bash
LANGSMITH_API_KEY=sua-chave-langsmith
LANGSMITH_PROJECT=nome-do-projeto
LANGSMITH_TRACING=true
```

#### Exemplo do trace de uma execução monitorado no langsmith: https://smith.langchain.com/public/ebabcef0-73b3-4238-9a4c-18878ae71386/r
