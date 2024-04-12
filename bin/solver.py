
from reader import gridReader
from graph import Graph, Switch, Edge



class Grapher:

    def __init__(self, filename: str) -> None:
        
        self._filename = filename
        self._grid = gridReader(filename)






g = Grapher(r'../resources/exemple1.txt')