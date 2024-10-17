


class Lamp:

    def __init__(self, _x: int, _y: int, mode: int) -> None:
        # Lamp container class, having canTurnOn function.        
        self._x: int = _x
        self._y: int = _y
        self._mode: int = mode

    @property
    def coordinates(self) -> tuple[int]:
        return (self._x, self._y)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def mode(self) -> int:
        return self._mode
    
    def canTurnOn(self, switch1state: bool, switch2state: bool) -> bool:

        match self.mode:
            case 0 : return False
            case 1 : return switch1state and switch2state # FF
            case 2 : return switch1state and not switch2state # FO
            case 3 : return (switch1state and switch2state) or (switch1state and not switch2state)
            case 4 : return not switch1state and switch2state # OF
            case 5 : return (switch1state and switch2state) or (not switch1state and switch2state)
            case 6 : return (not switch1state and switch2state) or (switch1state and not switch2state)
            case 7 : return (switch1state and switch2state) or (switch1state and not switch2state) or (not switch1state and switch2state)
            case 8 : return not switch1state and not switch2state # OO
            case 9 : return (not switch1state and not switch2state) or (switch1state and switch2state)
            case 10: return (not switch1state and not switch2state) or (switch1state and not switch2state)
            case 11: return (not switch1state and not switch2state) or (switch1state and switch2state) or (switch1state and not switch2state)
            case 12: return (not switch1state and not switch2state) or (not switch1state and switch2state)
            case 13: return (not switch1state and not switch2state) or (not switch1state and switch2state) or (switch1state and switch2state)
            case 14: return (not switch1state and not switch2state) or (not switch1state and switch2state) or (switch1state and not switch2state)
            case 15: return True
            case _ : raise ValueError(f'[E] Mode d\'allumage inconnu (={self.mode}).')
    
    def __repr__(self) -> str:
        return f'Lamp @ {self.coordinates} w mode {self.mode}'

