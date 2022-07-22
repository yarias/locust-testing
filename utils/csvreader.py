import csv
from importlib.resources import path

class CSVReader:
    def __init__(self, path) -> None:
        self.path = path
        
    def read_date(self):
        data = []
        reader = csv.DictReader(open(self.path, "r"))
        
        for item in reader:
            data.append(item)
            
        return data
