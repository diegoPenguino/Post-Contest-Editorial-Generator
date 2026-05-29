import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.llm import create_llm, log_llm_response, report_progress
from utils.constants import *

logger = logging.getLogger(__name__)


def wrong_approach_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Generating wrong approach analysis...")
    report_progress(state, "Phase: Summarizing wrong approaches")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    algorithm_explanation = state.get(ALGORITHM_EXPLANATION, "")

    template = load_prompt_template(PROMPT_TEMPLATE_WRONG_APPROACH)
    prompt = template.format(
        problem_statement=problem_statement, algorithm_explanation=algorithm_explanation
    )
    logger.info(
        "Wrong-approach prompt prepared: chars=%d model=%s temperature=%s",
        len(prompt),
        state.get(MODEL, DEFAULT_MODEL),
        state.get(TEMPERATURE, DEFAULT_TEMPERATURE),
    )

    llm = create_llm(
        model=state.get(MODEL, DEFAULT_MODEL),
        temperature=state.get(TEMPERATURE, DEFAULT_TEMPERATURE),
        api_key=state.get("api_key"),
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    wrong_approaches = log_llm_response("wrong_approach_node", response)

    logger.info("Wrong approach analysis completed")
    return {**state, WRONG_APPROACHES : wrong_approaches}
