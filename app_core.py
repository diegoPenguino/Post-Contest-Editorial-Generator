import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from graphs import create_editorial_graph
from utils import save_editorial, setup_logging

BASE_DIR = Path(__file__).parent
DEFAULT_PROBLEM_FILE = BASE_DIR / "input" / "problem_content.txt"
DEFAULT_SOLUTION_FILE = BASE_DIR / "input" / "problem_solution.cpp"


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file and return its contents."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Required file not found: {path}"
        ) from exc


def load_environment() -> dict:
    """Load runtime configuration from the environment."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment. "
            "Please create a .env file based on .env.example"
        )

    return {
        "model": os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        "temperature": float(os.getenv("OPENAI_TEMPERATURE", "1")),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }


def load_default_inputs() -> tuple[str, str]:
    """Load the bundled sample problem and solution files."""
    problem = read_text_file(DEFAULT_PROBLEM_FILE)
    solution = read_text_file(DEFAULT_SOLUTION_FILE)
    return problem, solution


def generate_editorial(
    problem_statement: str,
    solution_code: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    log_level: Optional[str] = None,
    save_output: bool = True,
) -> str:
    """Run the editorial workflow and return the final Markdown editorial."""
    config = load_environment()

    model = model or config["model"]
    temperature = temperature if temperature is not None else config["temperature"]
    log_level = log_level or config["log_level"]

    setup_logging(log_level)
    app = create_editorial_graph()

    initial_state = {
        "problem_statement": problem_statement,
        "solution_code": solution_code,
        "model": model,
        "temperature": temperature,
    }

    result = app.invoke(initial_state)
    final_editorial = result.get("final_editorial", "")

    if not final_editorial:
        raise RuntimeError("No editorial was generated.")

    if save_output:
        save_editorial(final_editorial)

    return final_editorial
