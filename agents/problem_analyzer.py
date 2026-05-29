import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.llm import create_llm, log_llm_response, report_progress
from utils.constants import *

logger = logging.getLogger(__name__)


def problem_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Starting problem analysis...")
    report_progress(state, "Phase: Analyzing the problem statement")

    problem_statement = state.get(PROBLEM_STATEMENT, "")

    template = load_prompt_template(PROMPT_TEMPLATE_PROBLEM_ANALYZER)
    prompt = template.format(problem_statement=problem_statement)
    logger.info(
        "Problem analyzer prompt prepared: chars=%d model=%s temperature=%s",
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
    analysis = log_llm_response("problem_analyzer_node", response)

    logger.info("Problem analysis completed")

    return {**state, PROBLEM_ANALYSIS : analysis}
