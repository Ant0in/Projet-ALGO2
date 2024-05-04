

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;

import java.io.IOException; // Importer la classe IOException

import dep.GridReader;
import dep.Lamp;


public class Solver {

    public static void main(String[] args) {
        
        // Main reader + solver :

        List<Lamp> lamps = new ArrayList<>();

        try {
            List<Object> objects = GridReader.read("C:\\Users\\antoi\\Desktop\\Projet-INFO-F-203\\resources\\exemple1.txt", false);
            for (Object obj : objects) {if (obj instanceof dep.Lamp) {lamps.add((Lamp) obj);}}
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println(lamps);

    }
}
