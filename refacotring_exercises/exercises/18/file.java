import java.awt.Point;

public class Bird {
    private PointWithConstraints position;

    public Bird(PointWithConstraints position) {
        this.position = position;
    }

    public void move(Point p) {
        position.move(p);
    }
}


public class Button {
    
    private PointWithConstraints position;

    public Button(PointWithConstraints position) {
        this.position = position;
    }

    public void move(Point p) {
        position.setPosition(p);
    }
}



public class PointWithConstraints {

    private int x;
    private int y;

    private int maxX;
    private int maxY;

    public PointWithConstraints(int startX, int startY, int maxX, int maxY) {
        this.x = startX;
        this.y = startY;
        this.maxX = maxX;
        this.maxY = maxY;
    }

    public Point getPosition() {
        return new Point(x, y);
    }

    // the shared logic lives here
    public void move(Point vector) {
        x = wrap(x + vector.x, maxX);
        y = wrap(y + vector.y, maxY);
    }

    public void setPosition(Point p) {
        x = wrap(p.x, maxX);
        y = wrap(p.y, maxY);
    }

    private int wrap(int value, int max) {
        while (value >= max) value -= max;
        while (value < 0) value += max;
        return value;
    }
}
