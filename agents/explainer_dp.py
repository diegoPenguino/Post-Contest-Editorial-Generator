import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.constants import *

logger = logging.getLogger(__name__)


def explainer_dp_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Generating dynamic programming explanation...")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    solution_code = state.get(SOLUTION_CODE, "")
    problem_analysis = state.get(PROBLEM_ANALYSIS, "")

    template = load_prompt_template(PROMPT_TEMPLATE_EXPLAINER_DP)
    prompt = template.format(
        problem_statement=problem_statement,
        solution_code=solution_code,
        problem_analysis=problem_analysis,
    )

    llm = ChatOpenAI(
        model=state.get(MODEL, DEFAULT_MODEL), temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE)
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    explanation = response.content

    logger.info("Dynamic programming explanation completed")

    return {**state, ALGORITHM_EXPLANATION: explanation}
