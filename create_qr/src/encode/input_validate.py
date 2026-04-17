import os
from .domain_errors import InputValidationDE

def validate_parent_dir(path):
    if not os.path.exists(os.path.dirname((path))):
        raise InputValidationDE(f"{path} parent doesnt exist")

def validate_is_file(path):
    if not os.path.isfile(path):
        raise InputValidationDE(f"{path} isnt file")

def validate_is_dir(path):
    if not os.path.isdir(path):
        raise InputValidationDE(f"{path} isnt dir")

def validate_abs_path(path: str) -> None:
    if not os.path.isabs(path):
        raise InputValidationDE(f"Path is not absolute: {path}")

def validate_exists(path):
    if not os.path.exists(path):
        raise InputValidationDE(f"{path} doesnt exist")