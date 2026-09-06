from pathlib import Path
import yaml
import os
import pickle

def get_project_root() -> Path:
    """Returns the root of the project"""
    return Path(__file__).parent.parent

def open_config():
    """Opens configuration file"""
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

