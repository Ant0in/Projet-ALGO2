
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.HashSet;
import java.util.Set;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;
import java.util.Iterator;

import dep.GridReader;
import dep.Lamp;


public class Solver {

    public static List<?> deepCopy(List<?> originalList) {
        List<Object> copiedList = new ArrayList<>();
        for (Object item : originalList) {
            if (item instanceof List<?>) {
                copiedList.add(deepCopy((List<?>) item)); // Appel récursif pour les listes imbriquées
            } else {
                copiedList.add(item);
            }
        }
        return copiedList;
    }

    public static List<List<List<Integer>>> createClauses(List<Lamp> lamps) {

        // On déclare l'array qui contriendra les listes de sub-clauses
        List<List<List<Integer>>> clauses = new ArrayList<>();

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
                    clauses.add(List.of(List.of(rowSid, columnSid)));
                    break;
                case 2:
                    clauses.add(List.of(List.of(rowSid, -columnSid)));
                    break;
                case 4:
                    clauses.add(List.of(List.of(-rowSid, columnSid)));
                    break;
                case 8:
                    clauses.add(List.of(List.of(-rowSid, -columnSid)));
                    break;
                case 3:
                    clauses.add(List.of(List.of(rowSid, columnSid), List.of(rowSid, -columnSid)));
                    break;
                case 5:
                    clauses.add(List.of(List.of(-rowSid, columnSid), List.of(rowSid, columnSid)));
                    break;
                case 6:
                    clauses.add(List.of(List.of(-rowSid, columnSid), List.of(rowSid, -columnSid)));
                    break;
                case 9:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(rowSid, columnSid)));
                    break;
                case 10:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(rowSid, -columnSid)));
                    break;
                case 12:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(-rowSid, columnSid)));
                    break;
                case 7:
                    clauses.add(List.of(List.of(rowSid, columnSid), List.of(-rowSid, columnSid), List.of(rowSid, -columnSid)));
                    break;
                case 11:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(rowSid, -columnSid), List.of(rowSid, columnSid)));
                    break;
                case 13:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(-rowSid, columnSid), List.of(rowSid, columnSid)));
                    break;
                case 14:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(-rowSid, columnSid), List.of(rowSid, -columnSid)));
                    break;
                case 15:
                    clauses.add(List.of(List.of(-rowSid, -columnSid), List.of(-rowSid, columnSid), List.of(rowSid, -columnSid), List.of(rowSid, columnSid)));
                    break;
                default:
                    throw new UnsupportedOperationException("[E] Mode d'allumage inconnu (=" + l.getMode() + ").");

            }
        }

        return clauses;
    }

    public static Object[] simplifyClauses(List<List<List<Integer>>> clauses) {
        
        boolean possibleSimplification = true;
        Set<Integer> prerequisites = new HashSet<>();
        boolean contradiction = false;

        while (possibleSimplification) {

            possibleSimplification = false;
            List<List<List<Integer>>> copyClauses = (List<List<List<Integer>>>) Solver.deepCopy(clauses);

            for (List<List<Integer>> c : copyClauses) {

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
                    List<List<Integer>> copySubclauses = (List<List<Integer>>) Solver.deepCopy(c);

                    for (List<Integer> d : copySubclauses) {

                        for (int u : d) {

                            if (prerequisites.contains(u * -1)) {
                                possibleSimplification = true;
                                clauses.get(clauses.indexOf(c)).remove(d);
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

    public static void main(String[] args) {
        
        // Main reader + solver :

        List<Lamp> lamps = new ArrayList<>();

        try {

            List<Object> objects = GridReader.read("C:\\Users\\antoi\\Desktop\\Projet-INFO-F-203\\resources\\exemple1.txt", false);
            for (Object obj : objects) {if (obj instanceof dep.Lamp) {lamps.add((Lamp) obj);}}

        } catch (IOException e) {

            e.printStackTrace();

        }


        List<List<List<Integer>>> clauses = Solver.createClauses(lamps);
        Object[] simplified_results = simplifyClauses(clauses);

    }
}
