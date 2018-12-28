import sys
import os

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(FILE_PATH, '..'))

# Allows the kernel to "see" the project during initialization. This
# FILE_PATH corresponds to Jupyter's "notebook-dir", but we want notebooks to
# behave as though they resided in the base directory to allow for clean
# imports.
# print("sys.path BEFORE = {}".format(sys.path))
sys.path.insert(1, PROJECT_BASE_PATH)
# print("sys.path AFTER = {}".format(sys.path))

c = get_config()

c.InteractiveShellApp.exec_lines = [
    "import pandas as pd",
    "from umap.uhelper import pd_result, set_log, end_log",
    "from datetime import datetime, timedelta",
    "from tqdm._tqdm_notebook import tqdm_notebook",
    "from django.db.models import Max, Avg, Count",
    "import numpy as np",
    'import matplotlib.pyplot as plt'
]