class Person {

    private String name;
    private String address;

    public Person(String name, String address) {
        this.name = name;
        this.address = address;
    }

    public String getName() {
        return this.name;
    }

    public String getAddress() {
        return this.address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String toString() {
        return "Person[name=" + this.name + ",address=" + this.address + "]";
    }

    public static void main(String args[]) {

        Person person = new Person("Chen", "Section 2, No.4, North Jianshe Road");
        System.out.println(person);
		System.out.println();

        Person student = new Student("Wang", "Section 2, No.4, North Jianshe Road", "Software Engineering", 2021, 8000);
        System.out.println(student);
		System.out.println();

        Person staff = new Staff("Zhang", "Section 2, No.4, North Jianshe Road", "School of Software Engineering", 6000);
        System.out.println(staff);

    }
}

class Student extends Person {

    private String program;
    private int year;
    private double fee;

    public Student(String name, String address, String program, int year, double fee) {
        super(name, address);
        this.program = program;
        this.year = year;
        this.fee = fee;
    }

    public String getProgram() {
        return program;
    }

    public void setProgram(String program) {
        this.program = program;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public double getFee() {
        return fee;
    }

    public void setFee(double fee) {
        this.fee = fee;
    }

    public String toString() {
        return "Student[Person[name=" + this.getName() + ",address=" + this.getAddress() + "],"
                + "program=" + program + ",year=" + year + ",fee=" + fee + ']';
    }

}

class Staff extends Person {

    private String school;
    private double pay;

    public Staff(String name, String address, String school, double pay) {
        super(name, address);
        this.school = school;
        this.pay = pay;
    }

    public String getSchool() {
        return school;
    }

    public void setSchool(String school) {
        this.school = school;
    }

    public double getPay() {
        return pay;
    }

    public void setPay(double pay) {
        this.pay = pay;
    }

    public String toString() {
        return "Staff[Person[name=" + this.getName() + ",address=" + this.getAddress() + "],"
                + "school=" + school + ",pay=" + pay + ']';
    }

}
