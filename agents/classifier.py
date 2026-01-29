import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.constants import *

logger = logging.getLogger(__name__)


def classifier_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Starting algorithm classification...")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    solution_code = state.get(SOLUTION_CODE, "")

    template = load_prompt_template(PROMPT_TEMPLATE_CLASSIFIER)
    prompt = template.format(
        problem_statement=problem_statement, solution_code=solution_code
    )

    llm = ChatOpenAI(
        model=state.get(MODEL, DEFAULT_MODEL), temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE)
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    algorithm_type = response.content.strip().lower()

    if algorithm_type not in VALID_ALGORITHM_TYPES:
        logger.warning(
            f"Invalid algorithm type '{algorithm_type}', defaulting to 'other'"
        )
        algorithm_type = OTHER

    logger.info(f"Algorithm classified as: {algorithm_type}")

    return {**state, ALGORITHM_TYPE: algorithm_type}
