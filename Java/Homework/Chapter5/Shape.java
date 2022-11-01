
abstract class Shape {

    protected String color;
    protected boolean filled;

    public Shape() {

    }

    public Shape(String color, boolean filled) {
        this.color = color;
        this.filled = filled;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public boolean isFilled() {
        return filled;
    }

    public void setFilled(boolean filled) {
        this.filled = filled;
    }

    public abstract double getArea();

    public abstract double getPerimeter();

    public String toString() {
        return "Shape{" + "color=" + color + ", filled=" + filled + '}';
    }

    public static void main(String args[]) {
        Circle c = new Circle(2.0, "red", true);
        System.out.println(c);
        System.out.println("c.getArea(): " + c.getArea());
        System.out.println("c.getPerimeter(): " + c.getPerimeter());
        System.out.println();
        System.out.println();

        Rectangle r = new Rectangle(3.0, 4.0, "blue", true);
        System.out.println(r);
        System.out.println("r.getArea(): " + r.getArea());
        System.out.println("r.getPerimeter(): " + r.getPerimeter());
        System.out.println();
        System.out.println();

        Square s = new Square(3.5, "yellow", false);
        System.out.println(s);
        System.out.println("s.getArea(): " + s.getArea());
        System.out.println("s.getPerimeter(): " + s.getPerimeter());
        System.out.println();
        System.out.println();
    }

}

class Circle extends Shape {

    protected double radius;

    public Circle() {
    }

    public Circle(double radius) {
        this.radius = radius;
    }

    public Circle(double radius, String color, boolean filled) {
        super(color, filled);
        this.radius = radius;
    }

    public double getRadius() {
        return radius;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    public double getArea() {
        return Math.PI * this.radius * this.radius;
    }

    public double getPerimeter() {
        return Math.PI * this.radius * 2;
    }

    public String toString() {
        return "Circle{" + "radius=" + radius + ", color=" + color + ", filled=" + filled + '}';
    }

}

class Rectangle extends Shape {

    double width;

    double length;

    public Rectangle() {
    }

    public Rectangle(double width, double length) {
        this.width = width;
        this.length = length;
    }

    public Rectangle(double width, double length, String color, boolean filled) {
        super(color, filled);
        this.width = width;
        this.length = length;
    }

    public double getLength() {
        return length;
    }

    public void setLength(double length) {
        this.length = length;
    }

    public double getWidth() {
        return width;
    }

    public void setWidth(double width) {
        this.width = width;
    }

    public double getArea() {
        return this.width * this.length;
    }

    public double getPerimeter() {
        return this.width * 2 + this.length * 2;
    }

    public String toString() {
        return "Rectangle{" + "width=" + width + ", length=" + length + ", color=" + color + ", filled=" + filled + '}';
    }

}

class Square extends Rectangle {

    public Square() {
    }

    public Square(double side) {
        super(side, side);
    }

    public Square(double side, String color, boolean filled) {
        super(side, side, color, filled);
    }

    public double getside() {
        return width;
    }

    public void setside(double side) {
        this.width = side;
        this.length = side;
    }

    public void setWidth(double side) {
        this.width = side;
    }

    public void setLength(double side) {
        this.width = side;
    }

    public String toString() {
        return "Square{" + "side=" + this.getside() + ", color=" + color + ", filled=" + filled + '}';
    }

}
