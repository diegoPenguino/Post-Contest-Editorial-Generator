import os
from pathlib import Path
from logging import getLogger
from dotenv import load_dotenv

from graphs import create_editorial_graph
from utils import setup_logging, save_editorial

logger = getLogger(__name__)

BASE_DIR = Path(__file__).parent
PROBLEM_FILE = BASE_DIR / "input" / "problem_content.txt"
SOLUTION_FILE = BASE_DIR / "input" / "problem_solution.cpp"

def _read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Required sample file not found: {path}. Please create it with the problem/solution text."
        )

SAMPLE_PROBLEM = _read_text_file(PROBLEM_FILE)
SAMPLE_SOLUTION = _read_text_file(SOLUTION_FILE)

def load_environment():
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


def main():
    """Main execution function."""
    try:
        config = load_environment()

        log = setup_logging(config["log_level"])
        log.info("=" * 60)
        log.info("Post-Contest Editorial Generator")
        log.info("=" * 60)

        log.info("Initializing workflow...")
        app = create_editorial_graph()

        initial_state = {
            "problem_statement": SAMPLE_PROBLEM,
            "solution_code": SAMPLE_SOLUTION,
            "model": config["model"],
            "temperature": config["temperature"],
        }

        log.info("Starting editorial generation workflow...")
        log.info(f"Model: {config['model']}")
        log.info(f"Temperature: {config['temperature']}")
        log.info("-" * 60)

        result = app.invoke(initial_state)
        final_editorial = result.get("final_editorial", "")

        if not final_editorial:
            log.error("No editorial was generated!")
            return

        log.info("-" * 60)
        log.info("Editorial Generation Complete!")
        log.info("-" * 60)
        log.info("\nGenerated Editorial:\n")

        output_path = save_editorial(final_editorial)
        log.info(f"Editorial saved to: {output_path}")
        log.info("=" * 60)

        # visualize_graph(app.get_graph(), filename="editorial_workflow.png")
        # logger.info("Workflow graph saved to 'editorial_workflow.png'")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure you have created a .env file with your OPENAI_API_KEY")
        return 1

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
