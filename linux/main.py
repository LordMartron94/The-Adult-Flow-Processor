from constants import CACHE_PATH
from src.app import App

# import install_linux_requirements
import os


def _prepare():
    # install_linux_requirements.run()
    if not os.path.isdir(CACHE_PATH):
        os.makedirs(CACHE_PATH)


if __name__ == "__main__":
    _prepare()

    App().run()
