
from reader import gridReader
from graph import Switch, Graph, Edge





def graphInit(filename: str, size: int) -> Graph:

    closed_switch: list[Switch] = []
    opened_swtich: list[Switch] = []

    for id in range(1, size * 2 + 1):
        closed_switch.append(Switch(id, True))
        opened_swtich.append(Switch(id, False))

    for data in gridReader(filename):
        
        switchLineID = data[0]
        switchColumnID = data[1] + 4
        connexionType: int = int(''.join([str(d) for d in data[2:]]), 2)

        match connexionType:
            
            # 0001 | Fermé-Fermé
            case 1:
                # Ligne fermée implique Colomne fermée et inversément.
                closed_switch[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))
                closed_switch[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))
            
            # 0010 | Fermé-Ouvert
            case 2:
                # Ligne Fermée implique Colomne ouverte et inversément.
                closed_switch[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                opened_swtich[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))

            # 0011 | Fermé-Fermé OU Fermé-Ouvert
            case 3:
                # Colomne fermée implique Ligne fermée et Colomne ouverte implique Ligne fermée.
                closed_switch[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))
                opened_swtich[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))

            # 0100 | Ouvert-Fermé
            case 4:
                opened_swtich[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))
                closed_switch[switchColumnID - 1].add_edge(Edge(opened_swtich[switchLineID - 1]))

            # 0101 | Fermé-Fermé OU Ouvert-Fermé
            case 5:
                closed_switch[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))
                opened_swtich[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))

            # 0110 | Fermé-Ouvert OU Ouvert-Fermé
            case 6:
                opened_swtich[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))
                closed_switch[switchColumnID - 1].add_edge(Edge(opened_swtich[switchLineID - 1]))
                closed_switch[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                opened_swtich[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))

            # 0111 | Fermé-Ouvert OU Ouvert-Fermé ou Fermé-Fermé
            case 7:
                pass

            # 1000 | Ouvert-Ouvert
            case 8:
                opened_swtich[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                opened_swtich[switchColumnID - 1].add_edge(Edge(opened_swtich[switchLineID - 1]))

            # 1001 | Fermé-Fermé OU Ouvert-Ouvert
            case 9:
                opened_swtich[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                opened_swtich[switchColumnID - 1].add_edge(Edge(opened_swtich[switchLineID - 1]))
                closed_switch[switchLineID - 1].add_edge(Edge(closed_switch[switchColumnID - 1]))
                closed_switch[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))

            # 1010 | Ouvert-Ouvert OU Fermé-Ouvert
            case 10:
                opened_swtich[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                closed_switch[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))

            # 1011 | Ouvert-Ouvert OU Fermé-Fermé OU Fermé-Ouvert
            case 11:
                opened_swtich[switchLineID - 1].add_edge(Edge(opened_swtich[switchColumnID - 1]))
                closed_switch[switchColumnID - 1].add_edge(Edge(closed_switch[switchLineID - 1]))

            case _:
                ...


        switches: list = closed_switch + opened_swtich
        return Graph(*switches)

        




g = graphInit(r'../resources/exemple1.txt', size=4)

print(g.Vertices[4].Edges)