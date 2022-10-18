class Circle {
    private double radius = 1.0;

    public Circle() {

    }

    public Circle(double radius) {
        this.radius = radius;
    }

    public double getRadius() {
        return this.radius;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    public double getCircumference() {
        return 2 * Math.PI * this.radius;
    }

    public String toString() {
        return "Circle[radius=" + this.radius + "]";
    }

    public static void main(String[] args) {
        Circle circle = new Circle(2.0);
        System.out.println("circle: " + circle + ", circumference is " + circle.getCircumference());
        circle.setRadius(3.5);
        System.out.println("circle: " + circle + ", circumference is " + circle.getCircumference());
    }

}

class Rectangle {
    private float length = 1.0f;
    private float width = 1.0f;

    public Rectangle() {

    }

    public Rectangle(float length, float width) {
        this.length = length;
        this.width = width;
    }

    public float getLength() {
        return this.length;
    }

    public float getWidth() {
        return width;
    }

    public void setLength(float length) {
        this.length = length;
    }

    public void setWidth(float width) {
        this.width = width;
    }

    public float getArea() {
        return width * length;
    }

    public float getPerimeter() {
        return 2 * (width + length);
    }

    public String toString() {
        return "Rectangle[length=" + this.length + ",width=" + this.width + "]";
    }

    public static void main(String[] args) {
        Rectangle rectangle = new Rectangle(5.0f, 3.0f);
        System.out.println("rectangle: " + rectangle + ", perimeter is " + rectangle.getPerimeter());
        rectangle.setLength(3.5f);
        rectangle.setWidth(2.5f);
        System.out.println("rectangle: " + rectangle + ", perimeter is " + rectangle.getPerimeter());
    }

}