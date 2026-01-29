import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.constants import *

logger = logging.getLogger(__name__)


def complexity_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Starting complexity analysis...")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    solution_code = state.get(SOLUTION_CODE, "")
    algorithm_explanation = state.get(ALGORITHM_EXPLANATION, "")

    template = load_prompt_template(PROMPT_TEMPLATE_COMPLEXITY)
    prompt = template.format(
        problem_statement=problem_statement,
        solution_code=solution_code,
        algorithm_explanation=algorithm_explanation,
    )

    llm = ChatOpenAI(
        model=state.get(MODEL, DEFAULT_MODEL), temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE)
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    analysis = response.content

    logger.info("Complexity analysis completed")

    return {**state, COMPLEXITY_ANALYSIS: analysis}
