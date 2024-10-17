package dep;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Clustering {

    public static boolean isAdjacent(Lamp lamp1, Lamp lamp2) {
        return lamp1.getX() == lamp2.getX() || lamp1.getY() == lamp2.getY();
    }

    public static void exploreNeighbors(Lamp lamp, List<Lamp> lampList, Set<Lamp> visited, List<List<Lamp>> clusters) {
        visited.add(lamp);

        for (Lamp neighbor : lampList) {
            if (!visited.contains(neighbor) && isAdjacent(lamp, neighbor)) {
                clusters.get(clusters.size() - 1).add(neighbor);
                exploreNeighbors(neighbor, lampList, visited, clusters);
            }
        }
    }

    public static List<List<Lamp>> clustering(List<Lamp> lampList) {
        List<List<Lamp>> clusters = new ArrayList<>();
        Set<Lamp> visited = new HashSet<>();

        for (Lamp lamp : lampList) {
            if (!visited.contains(lamp)) {
                List<Lamp> cluster = new ArrayList<>();
                cluster.add(lamp);
                clusters.add(cluster);
                exploreNeighbors(lamp, lampList, visited, clusters);
            }
        }

        return clusters;
    }
}