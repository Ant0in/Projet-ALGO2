
from src.python.core.lamp import Lamp
import os
  


class GridReader:

    @staticmethod
    def read(filepath: str, use_raw_data: bool = False) -> list[list[int]]:

        assert(os.path.exists(filepath) and os.path.isfile(filepath)), f'[E] path is not valid. ({filepath})'
        
        with open(filepath, encoding='utf-8') as f:
            lines: list[str] = f.readlines()

        ret: list = []
        for line in lines:

            _x, _y, *mode = line.split(' ')
            _x, _y = int(_x), int(_y)
            mode: int = int(''.join(mode), 2)

            if use_raw_data: ret.append([_x, _y, mode])
            else: ret.append(Lamp(_x, _y, mode))

        return ret


if __name__ == '__main__':

    b = GridReader.read('./../resources/exemple1.txt')