interface GeometricObject {
    double getPerimeter();

    double getArea();

    public static void main(String args[]) {

        ResizableCircle rc = new ResizableCircle(10);
        System.out.println("ResizableCircle with radius " + rc.radius + " has perimeter " + rc.getPerimeter()
                + " and area " + rc.getArea());

        rc.resize(200);
        System.out.println("ResizableCircle with radius " + rc.radius + " has perimeter " + rc.getPerimeter()
                + " and area " + rc.getArea());

        rc.resize(30);
        System.out.println("ResizableCircle with radius " + rc.radius + " has perimeter " + rc.getPerimeter()
                + " and area " + rc.getArea());

    }
}

interface Resizable {
    void resize(int percent);
}

class Circle implements GeometricObject {
    protected double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    public double getPerimeter() {
        return radius * 2 * Math.PI;
    }

    public double getArea() {
        return radius * Math.PI * Math.PI;
    }
}

class ResizableCircle extends Circle implements Resizable {

    public ResizableCircle(double radius) {
        super(radius);
    }

    public void resize(int percent) {
        this.radius = radius * percent / 100;
    }

}