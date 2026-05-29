import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.llm import create_llm, log_llm_response, report_progress
from utils.constants import *

logger = logging.getLogger(__name__)


def classifier_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Starting algorithm classification...")
    report_progress(state, "Phase: Classifying the algorithm")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    solution_code = state.get(SOLUTION_CODE, "")

    template = load_prompt_template(PROMPT_TEMPLATE_CLASSIFIER)
    prompt = template.format(
        problem_statement=problem_statement, solution_code=solution_code
    )
    logger.info(
        "Classifier prompt prepared: chars=%d model=%s temperature=%s",
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
    response_text = log_llm_response("classifier_node", response)
    algorithm_type = response_text.strip().lower()
    logger.info("Classifier normalized response: %r", algorithm_type)

    if algorithm_type not in VALID_ALGORITHM_TYPES:
        logger.warning(
            f"Invalid algorithm type '{algorithm_type}', defaulting to 'other'"
        )
        algorithm_type = OTHER

    logger.info(f"Algorithm classified as: {algorithm_type}")

    return {**state, ALGORITHM_TYPE: algorithm_type}
