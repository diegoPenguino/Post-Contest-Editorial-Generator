import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.llm import create_llm, log_llm_response, report_progress
from utils.constants import *

logger = logging.getLogger(__name__)


def composer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Creating final editorial...")
    report_progress(state, "Phase: Composing the final editorial")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    problem_analysis = state.get(PROBLEM_ANALYSIS, "")
    algorithm_explanation = state.get(ALGORITHM_EXPLANATION, "")
    complexity_analysis = state.get(COMPLEXITY_ANALYSIS, "")
    wrong_approaches = state.get(WRONG_APPROACHES, "")

    template = load_prompt_template(PROMPT_TEMPLATE_COMPOSER)
    prompt = template.format(
        problem_statement=problem_statement,
        problem_analysis=problem_analysis,
        algorithm_explanation=algorithm_explanation,
        complexity_analysis=complexity_analysis,
        wrong_approaches=wrong_approaches,
    )
    logger.info(
        "Composer prompt prepared: chars=%d model=%s temperature=%s",
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
    final_editorial = log_llm_response("composer_node", response)

    logger.info("Final editorial finished")

    return {**state, FINAL_EDITORIAL : final_editorial}
