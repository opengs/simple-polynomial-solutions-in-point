import json
from typing import List
from json import load, JSONDecodeError

class ImportException(Exception):
    '''Raised on import error'''
    pass

class ImportedData():
    def __init__(self, coefitients: List[float], value: float) -> None:
        self.coefitients = coefitients
        self.value = value

def import_from_file(path: str) -> ImportedData:
    try:
        with open(path, 'r') as fp:
            data = json.load(fp)
            coefitients = data.get("coefitients")
            value = data.get("value")

            if coefitients is None: raise ImportException("No coefitients in data file.")
            if value is None: raise ImportException("No value in data file.")

            return ImportedData(coefitients, value)
    except (IOError, FileNotFoundError):
        raise ImportException("IO error. Maybe file does not exist")
    except JSONDecodeError:
        raise ImportException("File is not in json format")