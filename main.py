
from src.python.solver import Solver
from src.python.core.reader import GridReader



if __name__ == '__main__':

    # Usage : use GridReader to read text files with lamp grids and then use one of the following ;
    # - Solver.maxThatCanBeTurnedOn_backtracking
    # - Solver.maxThatCanBeTurnedOn_dynamic
    # - Solver.fastMAX2SAT_clustering

    lampGrid: list = GridReader.read(filepath='./tests/exemple2.txt', use_raw_data=False)
    s: int = Solver.fastMAX2SAT_clustering(lamps=lampGrid)
    print(s)

