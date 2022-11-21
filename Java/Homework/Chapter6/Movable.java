interface Movable {
    void moveUp();

    void moveDown();

    void moveLeft();

    void moveRight();

    public static void main(String args[]) {

        MoveableCircle mc = new MoveableCircle(0, 0, 1, 1, 5);
        System.out.println("MoveableCircle Initialized: \t" + mc);

        mc.moveDown();
        System.out.println("MoveableCircle moved down: \t" + mc);

        mc.moveLeft();
        System.out.println("MoveableCircle moved left: \t" + mc);

        mc.moveUp();
        System.out.println("MoveableCircle moved up: \t" + mc);

        mc.moveRight();
        System.out.println("MoveableCircle moved right: \t" + mc);

    }

}

class MovablePoint implements Movable {
    int x;
    int y;
    int xSpeed;
    int ySpeed;

    public MovablePoint(int x, int y, int xSpeed, int ySpeed) {
        this.x = x;
        this.y = y;
        this.xSpeed = xSpeed;
        this.ySpeed = ySpeed;
    }

    public void moveDown() {
        y -= ySpeed;
    }

    public void moveLeft() {
        x -= xSpeed;
    }

    public void moveRight() {
        x += xSpeed;
    }

    public void moveUp() {
        y += ySpeed;
    }

    public String toString() {
        return "MovablePoint [x=" + x + ", y=" + y + ", xSpeed=" + xSpeed + ", ySpeed=" + ySpeed + "]";
    }

}

class MoveableCircle implements Movable {
    private int radius;
    private MovablePoint center;

    public MoveableCircle(int x, int y, int xSpeed, int ySpeed, int radius) {
        this.center = new MovablePoint(x, y, xSpeed, ySpeed);
        this.radius = radius;
    }

    public String toString() {
        return "MoveableCircle [radius=" + radius + ", center=" + center + "]";
    }

    public void moveDown() {
        this.center.moveDown();
    }

    public void moveLeft() {
        this.center.moveLeft();
    }

    public void moveRight() {
        this.center.moveRight();
    }

    public void moveUp() {
        this.center.moveUp();
    }

}