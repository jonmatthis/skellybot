# __main__.py
import sys
from pathlib import Path

base_package_path = Path(__file__).parent.parent
print(f"adding base_package_path: {base_package_path} : to sys.path")
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path

import logging

logger = logging.getLogger(__name__)

from gui.qt_main import qt_main

def main():
    qt_main()

if __name__ == '__main__':
    logger.info(f"Running as a script")
    main()
