
import os


class Lamp:

    def __init__(self, _x: int, _y: int, mode: int) -> None:
        
        self._x: int = _x
        self._y: int = _y
        self._mode: int = mode

    @property
    def coordinates(self) -> tuple[int]:
        return self._x, self._y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def mode(self) -> int:
        return self._mode
    
    def __repr__(self) -> str:
        return f'Lamp @ {self.coordinates} w mode {self.mode}'
    

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
