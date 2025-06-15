import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from typing import Any
from box import ConfigBox
from pathlib import Path
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox object.
    
    Args:
        path_to_yaml (Path): Path to the YAML file.
        
    Returns:
        ConfigBox: Content of the YAML file as a ConfigBox object.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfully.")
            return ConfigBox(content)
    except BoxValueError as e:
        logger.error(f"Error reading YAML file {path_to_yaml}: {e}")
        raise e


# NEW, CORRECTED VERSION
@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """Creates list of directories.

    Args:
        path_to_directories (list): list of path of directories
        verbose (bool, optional): ignore if multiple dirs is to be created. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
        
@ensure_annotations
def get_size(path: Path) -> str:
    """
    Calculates the size of a file and returns it in a human-readable format (KB).

    Args:
        path (Path): The path to the file.

    Returns:
        str: A string describing the file size (e.g., "~5 KB").
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~{size_in_kb} KB"