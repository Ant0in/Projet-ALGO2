
from reader import gridReader
from graph import Switch, Graph


class Solver:

    def __init__(self, filename: str, size: int) -> None:
        
        # On initialise le Graphe représentant notre situation.
        self.size: int = size
        self.dataGrid: list[list[int]] = gridReader(filename)
        self.graph: Graph = self.graphInit(dataGrid=self.dataGrid, size=size)

    @staticmethod
    def graphInit(dataGrid: list[list[int]], size: int) -> Graph:

        opened_switchs: list[Switch] = []
        closed_switchs: list[Switch] = []

        # On initialise les switchs L, C dans leurs deux états possibles.
        # Leur ID est positif si closed, négatif si opened.
        for id in range(1, size * 2 + 1):
            closed_switchs.append(Switch(id))
            opened_switchs.append(Switch(-id))

        for dataLine in dataGrid:
            
            # Les ID des switchs sur la ligne ne changent pas, mais ceux sur les colomnes viennent après,
            # d'où le +size. On identifie également le type d'allumage de chacune des lampes, et on en déduit
            # les implications logiques à l'aide d'un grand match case.

            lineID, columnID = dataLine[0] - 1, dataLine[1] + size - 1
            power_mode = int(''.join(str(i) for i in dataLine[2:]), 2)

            CL: Switch = closed_switchs[lineID]
            OL: Switch = opened_switchs[lineID]
            CC: Switch = closed_switchs[columnID]
            OC: Switch = opened_switchs[columnID]
            
            match power_mode:
                
                # 0001 - FF
                case 1: CL.implique(CC, doubleImplication=True)
                # 0010 - FO
                case 2: CL.implique(OC, doubleImplication=True)
                # 0011 - FF || FO
                case 3: CC.implique(CL); OC.implique(CL)
                # 0100 - OF
                case 4: OL.implique(CC, doubleImplication=True)
                # 0101 - OF || FF
                case 5: OL.implique(CC); CL.implique(CC)
                # 0110 - OF || FO
                case 6: OL.implique(CC, doubleImplication=True); CL.implique(OC, doubleImplication=True)
                # 0111 - FF || OF || FO
                case 7: OL.implique(CC); OC.implique(CL)
                # 1000 - OO
                case 8: OL.implique(OC, doubleImplication=True)
                # 1001 - FF || OO
                case 9: CL.implique(CC, doubleImplication=True); OL.implique(OC, doubleImplication=True)
                # 1010 - OO || FO
                case 10: OL.implique(OC); CL.implique(OC)
                # 1011 - OO || FO || FF
                case 11: OL.implique(OC); CC.implique(CL)
                # 1010 - OO || FO
                case 12: OL.implique(OC); CL.implique(OC)
                # 1101 - OO || OF || FF
                case 13: OC.implique(OL); CL.implique(CC)
                # 1110 - OO || OF || FO
                case 14: CL.implique(OC); CC.implique(OL)

                # 0000 - Nothing Works - Not interesting.
                case 0: pass
                # 1111 - Everything Works - Not interesting.
                case 15: pass
                # Default Case
                case _: raise ValueError(f'[E] Type d\'allumage inconnu. [={power_mode}]')

        return Graph(closed_switchs + opened_switchs)

    @staticmethod
    def canBeTurnedOn(graph: Graph) -> bool:

        canBeTurnedOnBool: bool = True

        # On vérifie si il est possible d'arriver à une contradiction du type :
        # Un switch S allumé finit par impliquer que S est éteint. Si une telle contradiction
        # est trouvée, alors il n'est pas possible d'allumer toutes les lampes à la fois.

        switchStates: set = set()

        for s in graph.switches:

            implications = [i.ID for i in s.DFS()]
            switchStates.update(implications)
         

        for switchState in switchStates:

            # Si on trouve un switch à la fois allumé et éteint ; contradiction
            if (switchState * -1) in switchStates:
                canBeTurnedOnBool = False
                break

        return canBeTurnedOnBool

    def maxThatCanBeTurnedOn(self) -> int:
        
        if self.canBeTurnedOn(self.graph):
            # Si il est déjà possible d'allumer toutes les lampes, on
            # ne va pas s'embêter à faire des calculs pour rien uwu
            return len(self.dataGrid)
        
        # On récupère la meilleure permutation de lampes avec un joli petit backtracking c:

        def backtracking(currentConfig: list, maxLamps) -> None:

            if self.canBeTurnedOn(self.graphInit(currentConfig, self.size)):
                maxLamps = max(maxLamps, len(currentConfig))
                
                #if len(currentConfig) == maxLamps: print(currentConfig)

            for possibleLamp in self.dataGrid:
                if possibleLamp not in currentConfig:
                    currentConfig.append(possibleLamp)
                    maxLamps = backtracking(currentConfig, maxLamps)
                    currentConfig.remove(possibleLamp)

            return maxLamps
        
        return backtracking([], 0)
        

        
            
if __name__ == '__main__':

    path: str = r'../resources/exemple1.txt'
    s = Solver(filename=path, size=4)
    print(s.canBeTurnedOn(s.graph))
    