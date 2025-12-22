import json

def load_config(filePath):
    with open(filePath, 'r') as f:
        return json.load(f)