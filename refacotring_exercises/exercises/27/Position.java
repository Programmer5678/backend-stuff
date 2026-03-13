import java.util.List;

public class Insert {
    public int insertAt;
    public String text;
}

public class Position {
    private int index;

    public Position(int index) {
        this.index = index;
    }

    public int index() {
        return index;
    }

    void onInsert(Insert ins) {
        if (index >= ins.insertAt) {
            index += ins.text.length();
        }
    }
}

public class Editor {

    private StringBuilder buffer = new StringBuilder();
    private int cursor = 0;
    private List<Position> positions = [];

    public void addPosition( Position p ) {
        positions.add(p);
    }

    public void insert(String text){

        Insert ins = new Insert(cursor, text);

        buffer.insert(ins.insertAt, ins.text);
        cursor += ins.text.length();

        positions.forEach( position -> position.onInsert( ins ) ) ;
    }

    public String fetch(int numberOfCharactersToFetch) {
        return buffer.substring(cursor, cursor + numberOfCharactersToFetch);
    }

    public void moveTo(Position position) {
        this.cursor = position.index();
    }

    public int position() {
        return cursor;
    }

    @Override
    public String toString() {
        return buffer.toString();
    }
}




public class Main {
    public static void main(String[] args) {

        Editor editor = new Editor();

        editor.insert("ba(nana)");

        final Position firstParenPosition = new Position(2);
        editor.addPosition(firstParenPosition);

        editor.moveTo(firstParenPosition);
        assert "(".equals(editor.fetch(1));

        editor.moveTo( new Position(1) );
        editor.insert("x");   // buffer is now: bxa(nana)

        editor.moveTo( firstParenPosition );
        assert "a".equals(editor.fetch(1));

        System.out.println(editor);
    }
}

