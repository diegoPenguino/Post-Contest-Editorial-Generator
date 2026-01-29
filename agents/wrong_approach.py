import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.constants import *

logger = logging.getLogger(__name__)


def wrong_approach_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Generating wrong approach analysis...")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    algorithm_explanation = state.get(ALGORITHM_EXPLANATION, "")

    template = load_prompt_template(PROMPT_TEMPLATE_WRONG_APPROACH)
    prompt = template.format(
        problem_statement=problem_statement, algorithm_explanation=algorithm_explanation
    )

    llm = ChatOpenAI(
        model=state.get(MODEL, DEFAULT_MODEL), temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE)
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    wrong_approaches = response.content

    logger.info("Wrong approach analysis completed")
    return {**state, WRONG_APPROACHES : wrong_approaches}
