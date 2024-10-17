
from src.python.solver import Solver
from src.python.core.reader import GridReader
import argparse


def main():

    parser = argparse.ArgumentParser(description="Mas2SAT Solver Parser")
    parser.add_argument('file', type=str, help='Path to the text file to read')
    args = parser.parse_args()

    lampGrid: list = GridReader.read(filepath=args.file, use_raw_data=False)
    s: int = Solver.fastMAX2SAT_clustering(lamps=lampGrid)
    print(s)


    
if __name__ == "__main__":

    # Usage : use GridReader to read text files with lamp grids and then use one of the following ;
    # - Solver.maxThatCanBeTurnedOn_backtracking
    # - Solver.maxThatCanBeTurnedOn_dynamic
    # - Solver.fastMAX2SAT_clustering
    main()