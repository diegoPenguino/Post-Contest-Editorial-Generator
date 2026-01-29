DEFAULT_MODEL = "gpt-5-nano"
DEFAULT_TEMPERATURE = 1

# Constants for state keys
PROBLEM_STATEMENT = "problem_statement"
SOLUTION_CODE = "solution_code"
MODEL = "model"
TEMPERATURE = "temperature"
PROBLEM_ANALYSIS = "problem_analysis"
ALGORITHM_TYPE = "algorithm_type"
ALGORITHM_EXPLANATION = "algorithm_explanation"
COMPLEXITY_ANALYSIS = "complexity_analysis"
WRONG_APPROACHES = "wrong_approaches"
FINAL_EDITORIAL = "final_editorial"

# Valid algorithm types
GREEDY = "greedy"
DYNAMIC_PROGRAMMING = "dynamic_programming"
GRAPH = "graph"
OTHER = "other"
VALID_ALGORITHM_TYPES = (GREEDY, DYNAMIC_PROGRAMMING, GRAPH, OTHER)

# Routing map for explainer nodes
ROUTE_MAP = {
    GREEDY: "explainer_greedy",
    DYNAMIC_PROGRAMMING: "explainer_dp",
    GRAPH: "explainer_graph",
}

# File names for prompt templates
PROMPT_TEMPLATE_COMPOSER = "composer"
PROMPT_TEMPLATE_CLASSIFIER = "classifier"
PROMPT_TEMPLATE_COMPLEXITY = "complexity"
PROMPT_TEMPLATE_PROBLEM_ANALYZER = "problem_analyzer"
PROMPT_TEMPLATE_EXPLAINER_GREEDY = "explainer_greedy"
PROMPT_TEMPLATE_EXPLAINER_DP = "explainer_dp"
PROMPT_TEMPLATE_EXPLAINER_GRAPH = "explainer_graph"
PROMPT_TEMPLATE_WRONG_APPROACH = "wrong_approach"
PROMPT_TEMPLATE_EXPLAINER_OTHER = "explainer_other"