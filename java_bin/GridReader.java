import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class GridReader {
    public static List<Object> read(String filepath, boolean useRawData) throws IOException {
        List<Object> ret = new ArrayList<>();

        BufferedReader br = new BufferedReader(new FileReader(filepath));
        String line;
        while ((line = br.readLine()) != null) {
            String[] parts = line.split(" ");
            int x = Integer.parseInt(parts[0]);
            int y = Integer.parseInt(parts[1]);
            int mode = Integer.parseInt(parts[2], 2);

            if (useRawData) {
                ret.add(new int[]{x, y, mode});
            } else {
                ret.add(new Lamp(x, y, mode));
            }
        }
        br.close();

        return ret;
    }
}
