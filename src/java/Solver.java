
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.HashSet;
import java.util.Set;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import core.Clustering;
import core.GridReader;
import core.Lamp;


public class Solver {

    public static ArrayList<?> deepCopy(ArrayList<?> originalList) {
        ArrayList<Object> copiedList = new ArrayList<>();
        for (Object item : originalList) {
            if (item instanceof ArrayList<?>) {
                copiedList.add(deepCopy((ArrayList<?>) item)); // Appel récursif pour les listes imbriquées
            } else {
                copiedList.add(item);
            }
        }
        return copiedList;
    }
    
    public static int findMax(ArrayList<ArrayList<ArrayList<Integer>>> clauses) {
        
        int max = 0;

        for (ArrayList<ArrayList<Integer>> clause : clauses) {
            for (ArrayList<Integer> pair : clause) {
                for (int num : pair) {
                    max = Math.max(max, Math.abs(num));
                }
            }
        }
        return max;
    }
    
    public static ArrayList<ArrayList<Integer>> tarjan(Map<Integer, ArrayList<Integer>> graph) {
        ArrayList<ArrayList<Integer>> result = new ArrayList<>();
        Stack<Integer> stack = new Stack<>();
        Map<Integer, Integer> index = new HashMap<>();
        Map<Integer, Integer> lowlink = new HashMap<>();
        Set<Integer> onStack = new HashSet<>();
        int currentIndex = 0;
    
        for (int v : graph.keySet()) {
            if (!index.containsKey(v)) {
                strongConnect(v, graph, stack, index, lowlink, onStack, result, currentIndex);
            }
        }
    
        return result;
    }
    
    private static void strongConnect(int v, Map<Integer, ArrayList<Integer>> graph, Stack<Integer> stack,
                                       Map<Integer, Integer> index, Map<Integer, Integer> lowlink, Set<Integer> onStack,
                                       ArrayList<ArrayList<Integer>> result, int currentIndex) {
        index.put(v, currentIndex);
        lowlink.put(v, currentIndex);
        currentIndex++;
        stack.push(v);
        onStack.add(v);
    
        for (int w : graph.getOrDefault(v, new ArrayList<>())) {
            if (!index.containsKey(w)) {
                strongConnect(w, graph, stack, index, lowlink, onStack, result, currentIndex);
                lowlink.put(v, Math.min(lowlink.get(v), lowlink.get(w)));
            } else if (onStack.contains(w)) {
                lowlink.put(v, Math.min(lowlink.get(v), index.get(w)));
            }
        }
    
        if (lowlink.get(v).equals(index.get(v))) {
            ArrayList<Integer> scc = new ArrayList<>();
            int w;
            do {
                w = stack.pop();
                onStack.remove(w);
                scc.add(w);
            } while (w != v);
            result.add(scc);
        }
    }
    
    public static ArrayList<ArrayList<ArrayList<Integer>>> createClauses(ArrayList<Lamp> lamps) {

        // On déclare l'array qui contriendra les listes de sub-clauses
        ArrayList<ArrayList<ArrayList<Integer>>> clauses = new ArrayList<>();

        // On calcule le nombre de lignes pour padder l'ID sur la plus grande ligne
        int numberOfLines = lamps.stream().mapToInt(Lamp::getX).max().orElse(0) + 1;

        for (Lamp l : lamps) {

            int rowSid = l.getX();
            int columnSid = numberOfLines + l.getY();

            switch (l.getMode()) {

                case 0:
                    clauses.add(new ArrayList<>(new ArrayList<>()));
                    break;
                case 1:
                    ArrayList<ArrayList<Integer>> mode1 = new ArrayList<>();
                    ArrayList<Integer> subMode1 = new ArrayList<>();
                    subMode1.add(rowSid);
                    subMode1.add(columnSid);
                    mode1.add(subMode1);
                    clauses.add(mode1);
                    break;
                case 2:
                    ArrayList<ArrayList<Integer>> mode2 = new ArrayList<>();
                    ArrayList<Integer> subMode2 = new ArrayList<>();
                    subMode2.add(rowSid);
                    subMode2.add(-columnSid);
                    mode2.add(subMode2);
                    clauses.add(mode2);
                    break;
                case 4:
                    ArrayList<ArrayList<Integer>> mode4 = new ArrayList<>();
                    ArrayList<Integer> subMode4 = new ArrayList<>();
                    subMode4.add(-rowSid);
                    subMode4.add(columnSid);
                    mode4.add(subMode4);
                    clauses.add(mode4);
                    break;
                case 8:
                    ArrayList<ArrayList<Integer>> mode8 = new ArrayList<>();
                    ArrayList<Integer> subMode8 = new ArrayList<>();
                    subMode8.add(-rowSid);
                    subMode8.add(-columnSid);
                    mode8.add(subMode8);
                    clauses.add(mode8);
                    break;
                case 3:
                    ArrayList<ArrayList<Integer>> mode3 = new ArrayList<>();
                    ArrayList<Integer> subMode3_1 = new ArrayList<>();
                    subMode3_1.add(rowSid);
                    subMode3_1.add(columnSid);
                    ArrayList<Integer> subMode3_2 = new ArrayList<>();
                    subMode3_2.add(rowSid);
                    subMode3_2.add(-columnSid);
                    mode3.add(subMode3_1);
                    mode3.add(subMode3_2);
                    clauses.add(mode3);
                    break;
                case 5:
                    ArrayList<ArrayList<Integer>> mode5 = new ArrayList<>();
                    ArrayList<Integer> subMode5_1 = new ArrayList<>();
                    subMode5_1.add(-rowSid);
                    subMode5_1.add(columnSid);
                    ArrayList<Integer> subMode5_2 = new ArrayList<>();
                    subMode5_2.add(rowSid);
                    subMode5_2.add(columnSid);
                    mode5.add(subMode5_1);
                    mode5.add(subMode5_2);
                    clauses.add(mode5);
                    break;
                case 6:
                    ArrayList<ArrayList<Integer>> mode6 = new ArrayList<>();
                    ArrayList<Integer> subMode6_1 = new ArrayList<>();
                    subMode6_1.add(-rowSid);
                    subMode6_1.add(columnSid);
                    ArrayList<Integer> subMode6_2 = new ArrayList<>();
                    subMode6_2.add(rowSid);
                    subMode6_2.add(-columnSid);
                    mode6.add(subMode6_1);
                    mode6.add(subMode6_2);
                    clauses.add(mode6);
                    break;
                case 9:
                    ArrayList<ArrayList<Integer>> mode9 = new ArrayList<>();
                    ArrayList<Integer> subMode9_1 = new ArrayList<>();
                    subMode9_1.add(-rowSid);
                    subMode9_1.add(-columnSid);
                    ArrayList<Integer> subMode9_2 = new ArrayList<>();
                    subMode9_2.add(rowSid);
                    subMode9_2.add(columnSid);
                    mode9.add(subMode9_1);
                    mode9.add(subMode9_2);
                    clauses.add(mode9);
                    break;
                case 10:
                    ArrayList<ArrayList<Integer>> mode10 = new ArrayList<>();
                    ArrayList<Integer> subMode10_1 = new ArrayList<>();
                    subMode10_1.add(-rowSid);
                    subMode10_1.add(-columnSid);
                    ArrayList<Integer> subMode10_2 = new ArrayList<>();
                    subMode10_2.add(rowSid);
                    subMode10_2.add(-columnSid);
                    mode10.add(subMode10_1);
                    mode10.add(subMode10_2);
                    clauses.add(mode10);
                    break;
                case 12:
                    ArrayList<ArrayList<Integer>> mode12 = new ArrayList<>();
                    ArrayList<Integer> subMode12_1 = new ArrayList<>();
                    subMode12_1.add(-rowSid);
                    subMode12_1.add(-columnSid);
                    ArrayList<Integer> subMode12_2 = new ArrayList<>();
                    subMode12_2.add(-rowSid);
                    subMode12_2.add(columnSid);
                    mode12.add(subMode12_1);
                    mode12.add(subMode12_2);
                    clauses.add(mode12);
                    break;
                case 7:
                    ArrayList<ArrayList<Integer>> mode7 = new ArrayList<>();
                    ArrayList<Integer> subMode7_1 = new ArrayList<>();
                    subMode7_1.add(rowSid);
                    subMode7_1.add(columnSid);
                    ArrayList<Integer> subMode7_2 = new ArrayList<>();
                    subMode7_2.add(-rowSid);
                    subMode7_2.add(columnSid);
                    ArrayList<Integer> subMode7_3 = new ArrayList<>();
                    subMode7_3.add(rowSid);
                    subMode7_3.add(-columnSid);
                    mode7.add(subMode7_1);
                    mode7.add(subMode7_2);
                    mode7.add(subMode7_3);
                    clauses.add(mode7);
                    break;
                case 11:
                    ArrayList<ArrayList<Integer>> mode11 = new ArrayList<>();
                    ArrayList<Integer> subMode11_1 = new ArrayList<>();
                    subMode11_1.add(-rowSid);
                    subMode11_1.add(-columnSid);
                    ArrayList<Integer> subMode11_2 = new ArrayList<>();
                    subMode11_2.add(rowSid);
                    subMode11_2.add(-columnSid);
                    ArrayList<Integer> subMode11_3 = new ArrayList<>();
                    subMode11_3.add(rowSid);
                    subMode11_3.add(columnSid);
                    mode11.add(subMode11_1);
                    mode11.add(subMode11_2);
                    mode11.add(subMode11_3);
                    clauses.add(mode11);
                    break;
                case 13:
                    ArrayList<ArrayList<Integer>> mode13 = new ArrayList<>();
                    ArrayList<Integer> subMode13_1 = new ArrayList<>();
                    subMode13_1.add(-rowSid);
                    subMode13_1.add(-columnSid);
                    ArrayList<Integer> subMode13_2 = new ArrayList<>();
                    subMode13_2.add(-rowSid);
                    subMode13_2.add(columnSid);
                    ArrayList<Integer> subMode13_3 = new ArrayList<>();
                    subMode13_3.add(rowSid);
                    subMode13_3.add(columnSid);
                    mode13.add(subMode13_1);
                    mode13.add(subMode13_2);
                    mode13.add(subMode13_3);
                    clauses.add(mode13);
                    break;
                case 14:
                    ArrayList<ArrayList<Integer>> mode14 = new ArrayList<>();
                    ArrayList<Integer> subMode14_1 = new ArrayList<>();
                    subMode14_1.add(-rowSid);
                    subMode14_1.add(-columnSid);
                    ArrayList<Integer> subMode14_2 = new ArrayList<>();
                    subMode14_2.add(-rowSid);
                    subMode14_2.add(columnSid);
                    ArrayList<Integer> subMode14_3 = new ArrayList<>();
                    subMode14_3.add(rowSid);
                    subMode14_3.add(-columnSid);
                    mode14.add(subMode14_1);
                    mode14.add(subMode14_2);
                    mode14.add(subMode14_3);
                    clauses.add(mode14);
                    break;
                case 15:
                    ArrayList<ArrayList<Integer>> mode15 = new ArrayList<>();
                    ArrayList<Integer> subMode15_1 = new ArrayList<>();
                    subMode15_1.add(-rowSid);
                    subMode15_1.add(-columnSid);
                    ArrayList<Integer> subMode15_2 = new ArrayList<>();
                    subMode15_2.add(-rowSid);
                    subMode15_2.add(columnSid);
                    ArrayList<Integer> subMode15_3 = new ArrayList<>();
                    subMode15_3.add(rowSid);
                    subMode15_3.add(-columnSid);
                    ArrayList<Integer> subMode15_4 = new ArrayList<>();
                    subMode15_4.add(rowSid);
                    subMode15_4.add(columnSid);
                    mode15.add(subMode15_1);
                    mode15.add(subMode15_2);
                    mode15.add(subMode15_3);
                    mode15.add(subMode15_4);
                    clauses.add(mode15);
                    break;
                default:
                    throw new UnsupportedOperationException("[E] Mode d'allumage inconnu (=" + l.getMode() + ").");
            }
        }

        return clauses;
    }

    public static Object[] simplifyClauses(ArrayList<ArrayList<ArrayList<Integer>>> clauses) {
        
        boolean possibleSimplification = true;
        Set<Integer> prerequisites = new HashSet<>();
        boolean contradiction = false;

        while (possibleSimplification) {

            possibleSimplification = false;
            ArrayList<ArrayList<ArrayList<Integer>>> copyClauses = (ArrayList<ArrayList<ArrayList<Integer>>>) Solver.deepCopy(clauses);

            for (ArrayList<ArrayList<Integer>> c : copyClauses) {

                if (c.isEmpty()) {
                    
                    // Si la clause est de taille 0, alors rien ne peut la satisfaire.
                    contradiction = true;
                    break;

                } else if (c.size() == 1) {

                    // Si notre clause est de taille 1 : alors ce n'est plus une clause mais une obligation.
                    prerequisites.addAll(c.get(0));
                    clauses.remove(c);
                    possibleSimplification = true;

                } else {

                    // Sinon la clause n'est pas unaire, alors on la simplifie si on peut puis on passe juste à autre chose.
                    ArrayList<ArrayList<Integer>> copySubclauses = (ArrayList<ArrayList<Integer>>) Solver.deepCopy(c);

                    for (List<Integer> d : copySubclauses) {

                        for (int u : d) {

                            if (prerequisites.contains(u * -1)) {
                                possibleSimplification = true;

                                for (ArrayList<ArrayList<Integer>> clause : clauses) {
                                    if (clause.equals(c)) {
                                        clause.remove(d);
                                        break;
                                    }
                                }
                            
                                break;
                            }

                        }

                    }

                }

            }
            
            if (contradiction) {
                break;
            }
   
        }

        for (int n : prerequisites) {
            if (prerequisites.contains(n * -1)) {
                contradiction = true;
                break;
            }
        }

        return new Object[]{clauses, contradiction};
    }

    public static boolean canBeTurnedOn(ArrayList<Lamp> lamps) {
        
        // On crée les clauses puis on les simplifies.
        ArrayList<ArrayList<ArrayList<Integer>>> clauses = Solver.createClauses(lamps);
        Object[] simplifiedResults = simplifyClauses(clauses);
        ArrayList<ArrayList<ArrayList<Integer>>> simplifiedClauses = (ArrayList<ArrayList<ArrayList<Integer>>>) simplifiedResults[0];
        boolean contradiction = (boolean) simplifiedResults[1];

        // Si on a une contradiction dans les clauses unaires, alors on return False : le système ne peut pas s'allumer.
        if (contradiction) return false;
        // Si pas de contradiction mais aucune clauses, alors on peut retourner True.
        if (simplifiedClauses.isEmpty() && !(contradiction)) return true;

        // Réprésentation sous forme de liste d'accès.
        Map<Integer, ArrayList<Integer>> graph = new HashMap<>();
        int nbVar = Solver.findMax(clauses);

        for (int i = 1; i <= nbVar; i++) {
            graph.put(i, new ArrayList<>());
            graph.put(-i, new ArrayList<>());
        }

        for (ArrayList<ArrayList<Integer>> c : simplifiedClauses) {
            for (ArrayList<Integer> pair : c) {
                int a = pair.get(0);
                int b = pair.get(1);
                graph.get(a).add(b);
                graph.get(b).add(a);
            }
        }

        // Recherche des composantes fortement connexes
        ArrayList<ArrayList<Integer>> scc = Solver.tarjan(graph);

        // Vérification des contraintes de non-contestation
        for (ArrayList<Integer> cc : scc) {
            //System.out.println(cc);
            for (int n : cc) {
                if (cc.contains(-n)) {
                    return false;
                }
            }
        }

        return true;
    }

    public static int maxThatCanBeTurnedOn_backtracking(ArrayList<Lamp> lamps) {
        if (canBeTurnedOn(lamps)) {
            // Si toutes les lampes peuvent déjà être allumées, on retourne simplement le nombre total de lampes.
            return lamps.size();
        }
        // Sinon, on effectue la recherche par backtracking pour trouver la meilleure configuration.
        return backtracking(new ArrayList<>(), lamps, 0);
    }

    private static int backtracking(ArrayList<Lamp> currentConfig, ArrayList<Lamp> lamps, int maxLamps) {
        if (!currentConfig.isEmpty()) {
            if (canBeTurnedOn(currentConfig)) {
                maxLamps = Math.max(maxLamps, currentConfig.size());
            }
        }

        for (Lamp possibleLamp : lamps) {
            if (!currentConfig.contains(possibleLamp)) {
                currentConfig.add(possibleLamp);
                maxLamps = backtracking(currentConfig, lamps, maxLamps);
                currentConfig.remove(possibleLamp);
            }
        }

        return maxLamps;
    }

    public static int fastMAX2SAT_clustering(List<Lamp> lamps) {
        List<List<Lamp>> clusters = Clustering.clustering(lamps);
        int maxLampsSum = 0;
        
        for (List<Lamp> cluster : clusters) {
            maxLampsSum += Solver.maxThatCanBeTurnedOn_backtracking((ArrayList<Lamp>) cluster);
        }
        
        return maxLampsSum;
    }


    public static void main(String[] args) {
        
        // Main reader + solver :

        ArrayList<Lamp> lamps = new ArrayList<>();

        try {

            List<Object> objects = GridReader.read("C:\\Users\\antoi\\Desktop\\Projet-INFO-F-203\\resources\\exemple4.txt", false);
            for (Object obj : objects) {if (obj instanceof dep.Lamp) {lamps.add((Lamp) obj);}}

        } catch (IOException e) {

            e.printStackTrace();

        }

        System.out.println(Solver.maxThatCanBeTurnedOn_backtracking(lamps));

    }
}
