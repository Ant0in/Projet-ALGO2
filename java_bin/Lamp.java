

public class Lamp {
    private int x;
    private int y;
    private int mode;

    public Lamp(int x, int y, int mode) {
        this.x = x;
        this.y = y;
        this.mode = mode;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getMode() {
        return mode;
    }

    public String toString() {
        return String.format("Lamp @ (%d, %d) w mode %d", x, y, mode);
    }
}
