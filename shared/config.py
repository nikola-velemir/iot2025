import json

from shared.pin_validator import validated


@validated
def load_config(filePath):
    with open(filePath, 'r') as f:
        return json.load(f)