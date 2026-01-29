import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.constants import *

logger = logging.getLogger(__name__)


def problem_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Starting problem analysis...")

    problem_statement = state.get(PROBLEM_STATEMENT, "")

    template = load_prompt_template(PROMPT_TEMPLATE_PROBLEM_ANALYZER)
    prompt = template.format(problem_statement=problem_statement)

    llm = ChatOpenAI(
        model=state.get(MODEL, DEFAULT_MODEL), temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE)
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    analysis = response.content

    logger.info("Problem analysis completed")

    return {**state, PROBLEM_ANALYSIS : analysis}
