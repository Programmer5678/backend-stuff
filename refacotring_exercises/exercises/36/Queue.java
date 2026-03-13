package exercises.36;

import java.util.ArrayList;

public class Queue {

    private ArrayList delegate = new ArrayList();

    public Queue() {
    }

    private ArrayList delegate() {
        return delegate;
    }

    public addRear(String s) {
        delegate.add(s);
    }

    public size() {
        return delegate.size();
    }

    String removeFront() {
        String result = delegate.get(0).toString();
        delegate.remove(0);
        return result;
    }

}
