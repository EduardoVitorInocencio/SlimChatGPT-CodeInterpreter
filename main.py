from tabnanny import verbose
from dotenv import load_dotenv, find_dotenv                         # Carrega variáveis de ambiente de um arquivo .env
from langchain import hub                                           # Importa o hub do LangChain para acessar templates e outros recursos
from langchain_openai import ChatOpenAI                             # Importa a classe ChatOpenAI para interagir com o modelo OpenAI
from langchain.agents import create_react_agent, AgentExecutor     # Importa funções para criar e executar agentes
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonAstREPLTool          # Importa a ferramenta PythonAstREPLTool para executar código Python
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
    agent = create_react_agent(   # Cria um agente reativo
        prompt=prompt,            
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), # Define o modelo de linguagem como GPT-4 Turbo
        tools=tools, # Define as ferramentas a serem utilizadas
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # Cria um executor de agente

    agent_executor.invoke(
        input={
            "input": """generate and save in QRcodes working directory 15 QRcodes
                                that point to www.udemy.com/course/langchain, you have qrcode package installed already"""
        }
    )

    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="episode_info.csv",
        verbose = True,
        allow_dangerous_code=True, # Permite a execução de código arbitrário
    )

    csv_agent.invoke(
        input={
            "input": "Which writer wrote the most episodes? how many episodes did he write?"
        }
    )

    csv_agent.invoke(
        input={
            "input": "print season ascending order of the number of episodes they have"
        }
    )

    print ("Fishing the instructions ...")

if __name__ == "__main__":
    main ()
