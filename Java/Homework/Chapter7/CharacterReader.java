import java.security.Principal;

class CharacterReader {
    int total;
    StringBuffer passedChars = new StringBuffer();

    public int pass(char c) throws NonalphabetException {
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
            // c is an alphabet.
            passedChars.append(c);
            return ++total;
        } else
            // c is not an alphabet.
            throw new NonalphabetException(c + " is not an alphabet.");
    }

    @Override
    public String toString() {
        return "CharacterReader [total=" + total + ", passedChars=" + passedChars + "]";
    }

    public static void main(String args[]) {
        CharacterReader cr = new CharacterReader();
        try {
            while (true) {
                cr.pass((char) System.in.read());
            }
        } catch (Exception e) {
            System.out.println(e);
        } finally {
            System.out.println(cr);
        }
    }

}

class NonalphabetException extends Exception {

    String msg;

    public NonalphabetException(String msg) {
        this.msg = msg;
    }

    public String toString() {
        return "NonalphabetException [" + msg + "]";
    }

}