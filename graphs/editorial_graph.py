import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from agents import (
    problem_analyzer_node,
    classifier_node,
    explainer_greedy_node,
    explainer_dp_node,
    explainer_graph_node,
    complexity_analyzer_node,
    wrong_approach_node,
    composer_node,
    explainer_other_node,
)

from utils.constants import *

logger = logging.getLogger(__name__)

class EditorialState(TypedDict):
    problem_statement: str
    solution_code: str
    model: str
    temperature: float
    problem_analysis: str
    algorithm_type: str
    algorithm_explanation: str
    complexity_analysis: str
    wrong_approaches: str
    final_editorial: str

def route_to_explainer(state: Dict[str, Any]) -> str:
    algorithm_type = state.get(ALGORITHM_TYPE, "other")

    next_node = ROUTE_MAP.get(algorithm_type, "explainer_other")
    logger.info(f"Routing to {next_node} based on algorithm type: {algorithm_type}")

    return next_node


def create_editorial_graph() -> CompiledStateGraph:
    logger.info("Creating editorial generation graph...")

    workflow = StateGraph(EditorialState)

    workflow.add_node("problem_analyzer", problem_analyzer_node)
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("explainer_greedy", explainer_greedy_node)
    workflow.add_node("explainer_dp", explainer_dp_node)
    workflow.add_node("explainer_graph", explainer_graph_node)
    workflow.add_node("explainer_other", explainer_other_node)
    workflow.add_node("complexity_analyzer", complexity_analyzer_node)
    workflow.add_node("wrong_approach", wrong_approach_node)
    workflow.add_node("composer", composer_node)

    workflow.set_entry_point("problem_analyzer")

    workflow.add_edge("problem_analyzer", "classifier")

    workflow.add_conditional_edges(
        "classifier",
        route_to_explainer,
        {
            "explainer_greedy": "explainer_greedy",
            "explainer_dp": "explainer_dp",
            "explainer_graph": "explainer_graph",
            "explainer_other": "explainer_other",
        },
    )

    workflow.add_edge("explainer_greedy", "complexity_analyzer")
    workflow.add_edge("explainer_dp", "complexity_analyzer")
    workflow.add_edge("explainer_graph", "complexity_analyzer")
    workflow.add_edge("explainer_other", "complexity_analyzer")

    workflow.add_edge("complexity_analyzer", "wrong_approach")
    workflow.add_edge("wrong_approach", "composer")

    workflow.add_edge("composer", END)

    app = workflow.compile()

    logger.info("Editorial generation graph created")

    return app
