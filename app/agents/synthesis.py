from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import config
from app.agents.state import AgentState

def synthesize_results(state:AgentState):
    llm = ChatOpenAI(
        openai_api_base = "https://openrouter.ai/api/v1",
        model = "openai/gpt-oss-120b:free",
        api_key = config.gpt_oss_key,
        temperature = 0.4,

    )

    prompt = ChatPromptTemplate.from_template("""
""")