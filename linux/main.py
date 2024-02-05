from constants import *
from app import App

import install_linux_requirements
import os

def prepare():
	# install_linux_requirements.run()
	if not os.path.isdir(CACHE_PATH):
		os.makedirs(CACHE_PATH)


if __name__ == "__main__":
	prepare()

	App().run()

