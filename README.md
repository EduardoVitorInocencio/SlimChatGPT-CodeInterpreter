# Gerador de Agentes e QR Codes com Python, LangChain e OpenAI

Este projeto utiliza a biblioteca LangChain para criar e gerenciar agentes que interagem com modelos de linguagem da OpenAI e executam tarefas baseadas em entradas de linguagem natural. Além disso, é utilizada a biblioteca `qrcode` para gerar códigos QR. O código ilustra como combinar ferramentas e agentes para criar soluções dinâmicas e escaláveis.

---

## Tecnologias Utilizadas

- **LangChain**: Framework para construir pipelines de linguagem natural e integrar modelos de IA.
- **OpenAI GPT-4**: Modelo de linguagem avançado utilizado como base para os agentes.
- **PythonAstREPLTool**: Ferramenta para executar código Python dinamicamente.
- **qrcode**: Biblioteca para gerar QR Codes.
- **dotenv**: Gerenciamento de variáveis de ambiente a partir de arquivos `.env`.

---

## Estrutura do Código

### 1. Carregamento de Variáveis de Ambiente

As variáveis de ambiente, como chaves de API, são carregadas usando `dotenv`. Isso garante a segurança e modularidade do código:

```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

### 2. Configuração dos Agentes

#### Agente Reativo com GPT-4

Um agente reativo é configurado com:

- **Prompt Base**: Importado do hub do LangChain.
- **Modelo GPT-4 Turbo**: Configurado com temperatura 0 (para respostas determinísticas).
- **Ferramenta PythonAstREPLTool**: Permite execução de código Python dinâmico.

```python
tools = [PythonAstREPLTool()]

python_agent = create_react_agent(
    prompt=prompt,
    llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
    tools=tools,
)

python_agent_executor = AgentExecutor(agent=python_agent, tools=tools, verbose=True)
```

#### Agente para Processar CSV

Um agente especializado em manipular arquivos CSV é criado usando a função `create_csv_agent`. Ele permite a execução de código arbitrário para processar e analisar arquivos CSV.

```python
csv_agent = create_csv_agent(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    path="episode_info.csv",
    verbose=True,
    allow_dangerous_code=True,
)
```

### 3. Criação do Agente Principal (Grand Agent)

O agente principal funciona como um roteador, delegando tarefas aos agentes especializados (Python e CSV). É configurado com ferramentas que direcionam as entradas para os agentes apropriados.

```python
TOOLS = [
    Tool(
        name="Python Agent",
        func=lambda x: python_agent_executor.invoke({"input": x}),
        description="Executa código Python baseado em entrada de linguagem natural.",
    ),
    Tool(
        name="CSV Agent",
        func=csv_agent.invoke,
        description="""Útil quando você precisa transformar linguagem natural em código CSV e executar o código CSV,
                       retornando os resultados da execução do código. Não aceita código como entrada.""",
    ),
]

grand_agent = create_react_agent(
    prompt=prompt, 
    llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), 
    tools=TOOLS
)

grand_agent_executor = AgentExecutor(agent=grand_agent, tools=TOOLS, verbose=True)
```

---

## Funcionalidades

### 1. Processar CSV

O agente CSV é utilizado para responder a perguntas relacionadas a arquivos CSV. Por exemplo:

```python
grand_agent_executor.invoke({
    "input": "which season has the most episodes?"
})
```

### 2. Gerar QR Codes

O agente Python gera 15 QR Codes para um URL específico:

```python
grand_agent_executor.invoke({
    "input": "Generate and save 15 QR codes pointing to 'www.udemy.com/course/langchain' in the 'QRCodes' directory",
})
```

---

## Destaques do Código

- **Uso de Ferramentas Personalizadas**: A integração com PythonAstREPLTool permite executar qualquer código Python.
- **Criação de Prompt Dinâmico**: Através do hub do LangChain, o código utiliza templates predefinidos e os adapta com instruções personalizadas.
- **Delegação de Tarefas**: O grand_agent organiza o roteamento das tarefas para o agente mais adequado.

---

## Como Executar

1. Clone o repositório e instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

2. Crie um arquivo `.env` com suas credenciais de API para o OpenAI:

    ```makefile
    OPENAI_API_KEY=your_api_key
    ```

3. Coloque o arquivo CSV chamado `episode_info.csv` no mesmo diretório do script.

4. Execute o script:

    ```bash
    python main.py
    ```

---

## Pontos de Atenção

- **Segurança**: A opção `allow_dangerous_code=True` no agente CSV permite a execução de código arbitrário. Use com cuidado em ambientes controlados.
- **Estrutura do Input**: Certifique-se de que os inputs estejam no formato esperado, como:

    ```python
    {"input": "sua pergunta ou tarefa"}
    ```

---

## Próximos Passos

- Adicionar suporte para mais tipos de agentes.
- Melhorar a interface do usuário para configurar e executar tarefas.
- Implementar logs avançados para monitorar as execuções.

---

## Autor

Desenvolvido por Eduardo Inocêncio.

- **E-mail**: eduardo@ascending.solutions
- **GitHub**: [EduardoVitorInocencio](https://github.com/EduardoVitorInocencio)





