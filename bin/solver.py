
from reader import gridReader
from graph import Switch, Graph


class Solver:

    def __init__(self, filename: str, size: int = 0) -> None:
        
        # On initialise le Graphe représentant notre situation.
        self.dataGrid: list[list[int]] = gridReader(filename)
        self.size = Solver.calculateSize(self.dataGrid) if size == 0 else size

    @staticmethod
    def calculateSize(dataGrid: list[list[Switch]]) -> int:
        return max(max(dataGrid, key=lambda d: d[0])[0], max(dataGrid, key=lambda d: d[1])[1])

    @staticmethod
    def makeImplicationGraph(dataGrid: list[list[int]], size: int) -> Graph:

        opened_switchs: list[Switch] = []
        closed_switchs: list[Switch] = []
        lampSwitchs: list[Switch] = []
        preRequisites: list[Switch] = []

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

            lampSwitchs += [CL, CC, OL, OC]
            
            match power_mode:
                
                # 0001 - FF
                case 1:
                    preRequisites += [CL, CC]

                # 0010 - FO
                case 2:
                    preRequisites += [CL, OC]

                # 0011 - FF || FO
                case 3:
                    CC.implique(CL); OC.implique(CL)

                # 0100 - OF
                case 4:
                    preRequisites += [OL, CC]

                # 0101 - OF || FF
                case 5:
                    OL.implique(CC); CL.implique(CC)

                # 0110 - OF || FO
                case 6:
                    OL.implique(CC, doubleImplication=True); CL.implique(OC, doubleImplication=True)

                # 0111 - FF || OF || FO
                case 7:
                    OL.implique(CC); OC.implique(CL)

                # 1000 - OO
                case 8:
                    preRequisites += [OL, OC]

                # 1001 - FF || OO
                case 9:
                    CL.implique(CC, doubleImplication=True); OL.implique(OC, doubleImplication=True)

                # 1010 - OO || FO
                case 10:
                    OL.implique(OC); CL.implique(OC)

                # 1011 - OO || FO || FF
                case 11:
                    OL.implique(OC); CC.implique(CL)

                # 1010 - OO || FO
                case 12:
                    OL.implique(OC); CL.implique(OC)

                # 1101 - OO || OF || FF
                case 13:
                    OC.implique(OL); CL.implique(CC)

                # 1110 - OO || OF || FO
                case 14:
                    CL.implique(OC); CC.implique(OL)

                # 0000 - Nothing Works - on ajoute un truc que Graph peut facilement lire comme un problème
                case 0: preRequisites.append(False)

                # 1111 - Everything Works - Not interesting.
                case 15: pass

                # Default Case
                case _: raise ValueError(f'[E] Type d\'allumage inconnu. [={power_mode}]')

        return Graph(lampSwitchs, preRequisites)

    @staticmethod
    def canBeTurnedOn(dataGrid: list[list[int]], size: int) -> bool:

        ImplicationGraph: Graph = Solver.makeImplicationGraph(dataGrid, size)

        # On vérifie qu'il n'existe pas de contradiction dans les prérequis, sinon quoi on fera
        # un early return.

        preRequisites = [i.ID for i in ImplicationGraph.preRequisite]
        
        for pr in preRequisites:

            # On vérifie qu'il n'y a pas un cas 0000
            if not pr:
                return False
            
            # Si le switch existe à l'état fermé ET ouvert ;
            if (pr * -1) in preRequisites:
                return False
            
        # Ensuite, on vérifie qu'aucune implication ne crée de contradiction évidente (on utilise le DFS).

        for s in ImplicationGraph.switches:
            
            # Les implications + les prérequis sont à vérifier
            implications = s.DFS() + preRequisites

            # Si le switch s existe à l'état fermé ET ouvert, via les implications ;
            if (s.ID * -1) in implications:
                return False
        
        # Si on a passé tous les tests, alors le système s'allume. 
        return True
    
    def maxThatCanBeTurnedOn(self) -> int:
        
        if Solver.canBeTurnedOn(self.dataGrid, self.size):
            # Si il est déjà possible d'allumer toutes les lampes, on
            # ne va pas s'embêter à faire des calculs pour rien uwu
            return len(self.dataGrid)
        
        # On récupère la meilleure permutation de lampes avec un joli petit backtracking c:

        def backtracking(currentConfig: list, maxLamps) -> None:

            if Solver.canBeTurnedOn(currentConfig, self.size):
                maxLamps = max(maxLamps, len(currentConfig))
                
                # if len(currentConfig) == maxLamps: print(currentConfig)

            for possibleLamp in self.dataGrid:
                if possibleLamp not in currentConfig:
                    currentConfig.append(possibleLamp)
                    maxLamps = backtracking(currentConfig, maxLamps)
                    currentConfig.remove(possibleLamp)

            return maxLamps
        
        return backtracking([], 0)
            



if __name__ == '__main__':

    s = Solver(filename=r'../resources/exemple1.txt')
    print(s.maxThatCanBeTurnedOn())
    