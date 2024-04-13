


class Edge:

    def __init__(self, destination: 'Switch', depart: 'Switch' = None) -> None:

        self._depart = depart
        self._destination = destination
     
    @property
    def Depart(self) -> 'Switch':
        return self._depart
    
    @property
    def Destination(self) -> 'Switch':
        return self._destination
    
    def set_depart(self, depart: 'Switch') -> None:
        self._depart = depart
    
class Switch:

    def __init__(self, ID: int, powered: bool, edges: Edge = None) -> None:
        
        self._ID = ID
        self._powered = powered
        self._edges = edges if edges else list()

    @property
    def Edges(self) -> list[Edge]:
        return [i for i in self._edges]
    
    @property
    def ID(self) -> int:
        return self._ID
    
    @property
    def power(self) -> bool:
        return self._powered

    def add_edge(self, *new_edges: tuple[Edge]) -> None:
        for new_edge in new_edges:
            new_edge.set_depart(self)
            self._edges.append(new_edge)

    def __str__(self) -> str:
        return f'Switch #{self.ID} ({"powered" if self.power else "not powered"})'

class Graph:

    def __init__(self, *switches) -> None:
        
        self._switches = [i for i in switches]

    @property
    def Vertices(self) -> list[Switch]:
        return self._switches
    
    @property
    def Edges(self) -> list[Edge]:
        ret = []
        for v in self.Vertices:
            for e in v.Edges:
                ret.append(e)
        return ret
    
    def getEdgeList(self, switch: Switch) -> list[Edge]:
        return [i for i in switch.Edges]
    
    def getAccessList(self, switch: Switch) -> list[Switch]:
        return [i.Destination for i in self.getEdgeList(switch)]
    
    def DFS(self, root_switch: Switch) -> list[Switch]:

        ret: list = []
        
        def _DFS(root: Switch):

            for voisin in self.getAccessList(root):

                if voisin not in ret:
                    ret.append(voisin)
                    _DFS(voisin)
                else: pass

        _DFS(root_switch)

        return ret

        
            
if __name__ == '__main__':

    L1_P = Switch(1, True); L1_N = Switch(1, False)
    L2_P = Switch(2, True); L2_N = Switch(2, False)
    L3_P = Switch(3, True); L3_N = Switch(3, False)
    L4_P = Switch(4, True); L4_N = Switch(4, False)

    C1_P = Switch(5, True); C1_N = Switch(5, False)
    C2_P = Switch(6, True); C2_N = Switch(6, False)
    C3_P = Switch(7, True); C3_N = Switch(7, False)
    C4_P = Switch(8, True); C4_N = Switch(8, False)

    C1_P.add_edge(Edge(L4_N))
    C2_P.add_edge(Edge(L3_P))
    C3_P.add_edge(Edge(L1_P))
    C4_P.add_edge(Edge(L4_N), Edge(L2_N))
    C2_N.add_edge(Edge(L3_P))
    C3_N.add_edge(Edge(L3_N))
    C4_N.add_edge(Edge(L2_P), Edge(L4_P))

    L2_N.add_edge(Edge(C4_P), Edge(C1_N))
    L3_N.add_edge(Edge(C3_N))
    L4_N.add_edge(Edge(C4_P), Edge(C1_P))
    L1_P.add_edge(Edge(C3_P))
    L2_P.add_edge(Edge(C1_N), Edge(C4_N))
    L4_P.add_edge(Edge(C4_N))

    g = Graph(L1_P, L1_N, L2_P, L2_N, L3_P, L3_N, L4_P, L4_N, C1_P, C1_N, C2_P, C2_N, C3_P, C3_N, C4_P, C4_N)
    for b in g.DFS(C1_P):
        print(b)


