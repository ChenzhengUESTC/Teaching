import java.util.Arrays;

class Book {
    private String name;
    private Author[] authors;
    private double price;
    private int qty = 0;

    public Book(String name, Author[] authors, double price) {
        this.name = name;
        this.authors = authors;
        this.price = price;
    }

    public Book(String name, Author[] authors, double price, int qty) {
        this(name, authors, price);
        this.qty = qty;
    }

    public String getName() {
        return name;
    }

    public Author[] getAuthors() {
        return authors;
    }

    public double getPrice() {
        return price;
    }

    public int getQty() {
        return qty;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public void setQty(int qty) {
        this.qty = qty;
    }

    @Override
    public String toString() {
        return "Book [name=" + name + ", authors=" + Arrays.toString(authors) + ", price=" + price + ", qty=" + qty
                + "]";
    }

    public String getAuthorNames() {
        String str = "";
        for (Author author : this.authors) {
            str += author.getName();
            str += ",";
        }
        return str.substring(0, str.lastIndexOf(","));
    }

    public static void main(String[] args) {
        Author[] authors = new Author[3];
        authors[0] = new Author("Stephen Hawking", "hawking@gmail.com", 'M');
        authors[1] = new Author("Jeremy Hunt", "hunt@gmail.com", 'M');
        authors[2] = new Author("J. B. Hartle", "hartle@gmail.com", 'M');

        Book book = new Book("A Brief History of Time", authors, 24.8, 100);
        System.out.println(book);
        System.out.println(book.getAuthorNames());
    }
}

class Author {
    private String name;
    private String email;
    private char gender;

    public Author(String name, String email, char gender) {
        this.name = name;
        this.email = email;
        this.gender = gender;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public char getGender() {
        return gender;
    }

    @Override
    public String toString() {
        return "Author [name=" + name + ", email=" + email + ", gender=" + gender + "]";
    }

}