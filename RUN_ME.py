import logging

from skellybot.__main__ import main

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.info(f"Running the main function from the file: {__file__}")

    main()

