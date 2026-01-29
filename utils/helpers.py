import logging
from pathlib import Path
from typing import Optional

from langchain_core.runnables.graph import MermaidDrawMethod, Graph

logger = logging.getLogger(__name__)

def setup_logging(level: str = "INFO") -> logging.Logger:
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="| %(levelname)s | %(asctime)s | %(name)s | %(message)s",
        force=True,
    )

    return_logger = logging.getLogger("editorial_gen")
    return return_logger


def load_prompt_template(template_name: str) -> str:
    current_file = Path(__file__)
    project_root = current_file.parent.parent
    template_path = project_root / "prompts" / f"{template_name}.txt"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def save_editorial(content: str, output_path: Optional[str] = None) -> str:
    logger.info("Saving editorial file...")
    if output_path is None:
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "editorial.md"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Editorial file saved.")
    return str(output_path)

def visualize_graph(graph : Graph, output_path: Optional[str] = "graph_visualization.png") -> str:
    logger.info("Visualizing graph...")
    image_data = graph.draw_mermaid_png(draw_method=MermaidDrawMethod.API)

    if output_path is None:
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "graph_visualization.png"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as img_file:
        img_file.write(image_data)

    logger.info(f"Graph visualization saved as {output_path}")
    return str(output_path)