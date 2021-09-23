import os
import shutil
from pathlib import Path


def clean_files(path):
    directory = 'temporary_data'
    path = os.path.join(path, directory)
    shutil.rmtree(path)


def create_temporary_cache(path):
    directory = 'temporary_data'
    dir_path = os.path.join(path, directory)
    results_path = Path(dir_path)
    if not results_path.exists():
        results_path.mkdir()
    return path
