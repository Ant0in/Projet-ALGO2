
# done using 2-SAT method. More can be found here : https://www.youtube.com/watch?v=Ku-jJ0G4tIc
from reader import GridReader, Lamp


class Solver:

    @staticmethod
    def find_max(alist: list) -> int:
        return max(Solver.find_max(item) for item in alist) if isinstance(alist, list) else abs(alist)
    
    @staticmethod
    def tarjan(graph: dict) -> list[list[int]]:
        
        def dfs(v):
            nonlocal index, stack, indices, lowlinks, result
            indices[v] = index
            lowlinks[v] = index
            index += 1
            stack.append(v)

            for neighbor in graph.get(v, []):
                if neighbor not in indices:
                    dfs(neighbor)
                    lowlinks[v] = min(lowlinks[v], lowlinks[neighbor])
                elif neighbor in stack:
                    lowlinks[v] = min(lowlinks[v], indices[neighbor])

            if lowlinks[v] == indices[v]:
                scc = []
                while True:
                    node = stack.pop()
                    scc.append(node)
                    if node == v:
                        break
                result.append(scc)

        index = 0
        stack = []
        indices = {}
        lowlinks = {}
        result = []

        for node in graph:
            if node not in indices:
                dfs(node)

        return result

    @staticmethod
    def create_clauses(lamps: list[Lamp]) -> list[list[int]]:

        clauses: list = []
        # On calcule le nombre de lines pour padder l'ID sur la plus grande ligne
        number_of_lines: int = max(lamps, key=lambda w: w.x).x + 1
        
        for l in lamps:

            row_sid: int = l.x
            column_sid: int = number_of_lines + l.y

            match l.mode:
                
                # 0000 - Nothing
                # 0001 - FF
                # 0010 - FO
                # 0100 - OF
                # 1000 - OO

                case 0: clauses.append([[]])
                case 1: clauses.append([[row_sid, column_sid]])
                case 2: clauses.append([[row_sid, -column_sid]])
                case 4: clauses.append([[-row_sid, column_sid]])
                case 8: clauses.append([[-row_sid, -column_sid]])

                # 0011 - FF || FO
                # 0101 - OF || FF
                # 0110 - OF || FO
                # 1001 - FF || OO
                # 1010 - OO || FO
                # 1100 - OO || OF

                case 3: clauses.append([[row_sid, column_sid], [row_sid, -column_sid]])
                case 5: clauses.append([[-row_sid, column_sid], [row_sid, column_sid]])
                case 6: clauses.append([[-row_sid, column_sid], [row_sid, -column_sid]])
                case 9: clauses.append([[-row_sid, -column_sid], [row_sid, column_sid]])
                case 10: clauses.append([[-row_sid, -column_sid], [row_sid, -column_sid]])
                case 12: clauses.append([[-row_sid, -column_sid], [-row_sid, column_sid]])

                # 0111 - FF || OF || FO
                # 1011 - OO || FO || FF
                # 1101 - OO || OF || FF
                # 1110 - OO || OF || FO
                # 1111 - Everything Works

                case 7: clauses.append([[row_sid, column_sid], [-row_sid, column_sid], [row_sid, -column_sid]])
                case 11: clauses.append([[-row_sid, -column_sid], [row_sid, -column_sid], [row_sid, column_sid]])
                case 13: clauses.append([[-row_sid, -column_sid], [-row_sid, column_sid], [row_sid, column_sid]])
                case 14: clauses.append([[-row_sid, -column_sid], [-row_sid, column_sid], [row_sid, -column_sid]])
                case 15: clauses.append([[-row_sid, -column_sid], [-row_sid, column_sid], [row_sid, -column_sid], [row_sid, column_sid]])

                # Default Case
                case _: raise NotImplementedError(f'[E] Mode d\'allumage inconnu (={l.mode}).')

        return clauses

    @staticmethod
    def simplify_clauses(clauses: list[list[int]]) -> tuple[list[list[int]], bool]:

        possible_simplification: bool = True
        prerequisites: set = set()
        contradiction: bool = False

        while possible_simplification:

            possible_simplification = False

            for c in clauses[:]:

                # Si la clause est de taille 0, alors rien ne peut la satisfaire.
                if len(c) == 0:
                    contradiction: bool = True
            
                # Si notre clause est de taille 1 : alors ce n'est plus une clause mais une obligation.
                elif len(c) == 1:

                    for t in c[0]: prerequisites.add(t)
                    clauses.remove(c)
                    possible_simplification = True

                # Sinon la clause n'est pas unaire, alors on la simplifie si on peut puis on passe juste à autre chose.
                else:     
                    
                    # On veut regarder si l'une des conditions contient une position interdite.
                    for d in c[:]:

                        for u in d:
                            if u * -1 in prerequisites:
                                possible_simplification = True
                                c.remove(d)
                                break

            for n in prerequisites:
                if n * -1 in prerequisites:
                    contradiction = True
                    break
        
        return clauses, contradiction
                
    @staticmethod
    def canBeTurnedOn(lamps: list[Lamp]) -> bool:
        
        clauses, contradiction = Solver.simplify_clauses(Solver.create_clauses(lamps))

        # Si on a une contradiction dans les clauses unaires, alors on return False : le système ne peut pas s'allumer.
        if contradiction: return False
        # Si pas de contradiction mais aucune clauses, alors on peut retourner True.
        if not clauses: return True

        # Réprésentation sous forme de liste d'accès.
        graph: dict = {}
        nb_var: int = Solver.find_max(clauses)

        for i in range(1, nb_var + 1):
            graph[i] = []
            graph[-i] = []

        for c in clauses:
            for a, b in c:
                graph[a].append(b)
                graph[b].append(a)

        scc = Solver.tarjan(graph)

        for cc in scc:
            for n in cc:
                if n * -1 in cc:
                    return False
        return True

    @staticmethod
    def maxThatCanBeTurnedOn_backtracking(lamps) -> int:
        
        if Solver.canBeTurnedOn(lamps):
            # Si il est déjà possible d'allumer toutes les lampes, on
            # ne va pas s'embêter à faire des calculs pour rien uwu
            return len(lamps)
        
        # On récupère la meilleure permutation de lampes avec un joli petit backtracking c:

        def backtracking(currentConfig: list, maxLamps) -> None:

            if currentConfig:
                if Solver.canBeTurnedOn(currentConfig):
                    maxLamps = max(maxLamps, len(currentConfig))
                
                # if len(currentConfig) == maxLamps: print(currentConfig)

            for possibleLamp in lamps:
                if possibleLamp not in currentConfig:
                    currentConfig.append(possibleLamp)
                    maxLamps = backtracking(currentConfig, maxLamps)
                    currentConfig.remove(possibleLamp)

            return maxLamps
        
        return backtracking([], 0)



if __name__ == '__main__':

    w = GridReader.read(r'./../resources/exemple2.txt')
    print(Solver.canBeTurnedOn(w))
