import os
import warnings

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.prompts.system import SYSTEM_PROMPT
from src.tools.calculator import calculator
from src.tools.weather import get_weather
from src.tools.crypto import get_crypto_price


def create_assistant():
    """Cria o assistente de IA com capacidades de tool calling."""

    # Desabilita warnings do LangSmith se não tiver API key para monitoramento
    if not os.getenv("LANGSMITH_API_KEY"):
        os.environ["LANGSMITH_TRACING"] = "false"
        warnings.filterwarnings("ignore", module="langsmith")

    # Cria o cliente LLM usando o wrapper do LangChain
    llm = ChatOpenAI(
        model="gpt-5-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Cria o agente com as ferramentas e o prompt usando o create_react_agent do LangGraph
    agent = create_react_agent(
        model=llm,
        tools=[calculator, get_weather, get_crypto_price],
        prompt=SYSTEM_PROMPT,
    )

    return agent


def run_query(agent, question: str) -> str:
    """Executa uma pergunta do usuário no agente."""
    result = agent.invoke({"messages": [("user", question)]})
    return result["messages"][-1].content