from tabnanny import verbose
from dotenv import load_dotenv, find_dotenv                         # Carrega variáveis de ambiente de um arquivo .env
from langchain import hub                                           # Importa o hub do LangChain para acessar templates e outros recursos
from langchain_openai import ChatOpenAI                             # Importa a classe ChatOpenAI para interagir com o modelo OpenAI
from langchain.agents import create_react_agent, AgentExecutor     # Importa funções para criar e executar agentes
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonAstREPLTool          # Importa a ferramenta PythonAstREPLTool para executar código Python
from langchain_core.tools import Tool
from typing import Any
import qrcode                                                       # Importa a biblioteca qrcode para gerar QR codes


load_dotenv(find_dotenv())


def main ():
   
    print ("Starting ...")

    instructions = """You are an agent designed to write and execute Python code to answer questions.
    You have access to a Python REPL, which you can use to execute Python code.
    The 'qrcode' package is already installed. Always ensure that the library is imported before generating QR codes.
    If you get an error, debug your code and try again. Only use the output of your code to answer the question.
    """

    # 1. Puxa um template de prompt base do LangChain AI hub.
    # 2. Preenche parcialmente o prompt base com as instruções definidas.
    
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonAstREPLTool()] # Define a ferramenta PythonAstREPLTool como a ferramenta a ser utilizada

    ############################ FIRST AGENT EXECUTOR ########################################
    python_agent = create_react_agent(   # Cria um agente reativo
        prompt=prompt,            
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), # Define o modelo de linguagem como GPT-4 Turbo
        tools=tools, # Define as ferramentas a serem utilizadas
    )

    python_agent_executor = AgentExecutor(agent=python_agent, tools=tools, verbose=True) # Cria um executor de agente

    ############################ SECOND AGENT EXECUTOR ########################################
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="episode_info.csv",
        verbose = True,
        allow_dangerous_code=True, # Permite a execução de código arbitrário
    )

    ################################ Router Grand Agent ########################################################

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    TOOLS = [
        Tool(
            name="Python Agent",
            func=lambda x: python_agent_executor.invoke({"input": x}),
            description="Executes Python code based on natural language input.",
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent.invoke,
            description="""Useful when you need to transform natural language to CSV and execute the CSV code,
                           returning the results of the code execution. Does not accept code as input.""",
        ),
    ]

    prompt = base_prompt.partial(instructions="")

    grand_agent = create_react_agent(
        prompt=prompt, 
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), 
        tools=TOOLS
        )
    
    grand_agent_executor = AgentExecutor(agent=grand_agent, tools=TOOLS, verbose=True)

    print(
        grand_agent_executor.invoke(
            {
                "input": "which season has the most episodes?",
            }
        )
    )

    print(
        grand_agent_executor.invoke(
            {
            "input": "Generate and save 15 QR codes pointing to 'www.udemy.com/course/langchain in the cQRCodes directory'",
        }

        )
    )

    print ("Fishing the instructions ...")

if __name__ == "__main__":
    main ()
