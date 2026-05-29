#initializing the model

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_openai import ChatOpenAI
from app.agents.state import AgentState
from langchain_core.prompts import ChatPromptTemplate

import config 

def create_research_plan(state:AgentState):
    llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-120b:free",
    api_key=config.gpt_oss_key,
    temperature=0.4,
)

    out_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_template( """
        You are a Knowledge architect and you are tasked with creating a research plan for the topic: {topic}.
        The research plan should include the following sections:
        Breaks a topic into structured parts
        Organizes information hierarchically
        Ensures the parts are complete and non-overlapping
        Designs the structure so it’s easy to learn, teach, or analyze
        Acts a bit like an “engineer of ideas,” not just an explainer
        Note: Return in comma separated format, without any additional text. The output should be a list of the main parts of the topic,
        organized hierarchically if applicable.
    """)

    chain = prompt | llm | out_parser
    result = chain.invoke({
        "topic": state["input_query"]
    })

    current = state["retry_count"]
    new_state_value = current + 1
    return (
        {
            "subquery": result,
            "retry_count": new_state_value
        }
    )
    
        