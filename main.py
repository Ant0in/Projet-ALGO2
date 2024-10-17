
from src.python.solver import Solver
from src.python.core.reader import GridReader



if __name__ == '__main__':

    lampGrid: list = GridReader.read(filepath='./resources/exemple1.txt', use_raw_data=False)
    s: int = Solver.fastMAX2SAT_clustering(lamps=lampGrid)
    print(s)