import java.util.Optional;
import java.util.Stack;

abstract class Operation {
    char type;

    public Operation(char type) {
        this.type = type;
    }

    protected abstract String stringIt();

    public void printIt() {
        System.out.println("operation=" + this.stringIt());
    }

    public abstract void doIt(Stack s, Optional<Object> item);
}

class Plus extends Operation {

    public Plus() {
        super('+');
    }

    @Override
    protected String stringIt() {
        return "push";
    }

    @Override
    public void doIt(Stack s, Optional<Object> item) {
        s.push(item.orElse(null));
    }
}

class Pop extends Operation {

    public Pop() {
        super('-');
    }

    @Override
    protected String stringIt() {
        return "pop";
    }

    @Override
    public void doIt(Stack s, Optional<Object> item) {
        s.pop();
    }
}

class Top extends Operation {

    public Top() {
        super('@');
    }

    @Override
    protected String stringIt() {
        return "top";
    }

    @Override
    public void doIt(Stack s, Optional<Object> item) {
        System.out.println("top=" + s.peek());
    }
}

public class Main {

    // New realistic operation
    public void swapTopTwo(Stack s) {
        Object first = s.pop();
        Object second = s.pop();
        s.push(first);
        s.push(second);
    }

    public static void main(String[] args) {
        Main m = new Main();
        Stack<Object> stack = new Stack<>();

        // Example usage:
        new Plus().doIt(stack, "hello");
        new Plus().doIt(stack, "world");

        new Plus().printIt();
        System.out.println("stack before swap: " + stack);

        // Use the new operation
        m.swapTopTwo(stack);

        System.out.println("stack after swap: " + stack);

        // Example of Top and Pop
        new Top().printIt();
        new Top().doIt(stack, null);

        new Pop().printIt();
        new Pop().doIt(stack, null);
    }
}
