import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from utils import load_prompt_template
from utils.llm import create_llm, log_llm_response, report_progress
from utils.constants import *

logger = logging.getLogger(__name__)


def explainer_graph_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Generating graph algorithm explanation...")
    report_progress(state, "Phase: Explaining the graph approach")

    problem_statement = state.get(PROBLEM_STATEMENT, "")
    solution_code = state.get(SOLUTION_CODE, "")
    problem_analysis = state.get(PROBLEM_ANALYSIS, "")

    template = load_prompt_template(PROMPT_TEMPLATE_EXPLAINER_GRAPH)
    prompt = template.format(
        problem_statement=problem_statement,
        solution_code=solution_code,
        problem_analysis=problem_analysis,
    )
    logger.info(
        "Graph explainer prompt prepared: chars=%d model=%s temperature=%s",
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
    explanation = log_llm_response("explainer_graph_node", response)

    logger.info("Graph algorithm explanation completed")

    return {**state, ALGORITHM_EXPLANATION: explanation}
