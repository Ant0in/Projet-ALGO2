

class Switch:

    def __init__(self, ID: int) -> None:
        
        self.ID = ID
        self.accessible: list = []

    def implique(self, neighborSwitch: 'Switch', doubleImplication: bool = False) -> None:

        # On schématise les arêtes dans le problème par des "implications".
        self.accessible.append(neighborSwitch)
        if doubleImplication: neighborSwitch.accessible.append(self)

    def DFS(self) -> list['Switch']:
        
        # On récupère les implications qui découlent de notre Switch. On utilise
        # le DFS pour parcourir les Switchs accessibles.

        visited: list['Switch'] = []

        def _dfs(current: 'Switch') -> None:
            for node in current.accessible:
                if node not in visited and node is not self:
                    visited.append(node)
                    _dfs(node)

        _dfs(self)
        return visited

    def __repr__(self) -> str:
        return f'Switch #{self.ID} -> {[i.ID for i in self.accessible]}'

class Graph:

    def __init__(self, switches: list[Switch]) -> None:

        # La classe Graphe ne sert qu'à regrouper les sommets.
        
        self.switches = switches