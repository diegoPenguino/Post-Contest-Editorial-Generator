from logging import getLogger
from app_core import generate_editorial, load_default_inputs, load_environment
from utils import setup_logging

logger = getLogger(__name__)


def main():
    """Main execution function."""
    try:
        config = load_environment()
        sample_problem, sample_solution = load_default_inputs()

        log = setup_logging(config["log_level"])
        log.info("=" * 60)
        log.info("Post-Contest Editorial Generator")
        log.info("=" * 60)

        log.info("Starting editorial generation workflow...")
        log.info(f"Model: {config['model']}")
        log.info(f"Temperature: {config['temperature']}")
        log.info("-" * 60)

        generate_editorial(
            sample_problem,
            sample_solution,
            model=config["model"],
            temperature=config["temperature"],
            log_level=config["log_level"],
        )

        log.info("-" * 60)
        log.info("Editorial Generation Complete!")
        log.info("-" * 60)
        log.info("\nGenerated Editorial:\n")
        log.info("Editorial saved to: output/editorial.md")
        log.info("=" * 60)

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
