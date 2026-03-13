import java.util.Arrays;

import junit.framework.*;

final int BOARD_SIZE = 3;

public class GameTest extends TestCase {

    private int tmp(Position p) {
        if (p == null) {
            return -1;
        }
        return p.row() * BOARD_SIZE + p.column();
    }

    public GameTest(String s) {
        super(s);
    }

    public void testDefaultMove() {
        Board board = new Board(new Row[] { new Row(Square.EMPTY, Square.EMPTY, Square.EMPTY),
                new Row(Square.EMPTY, Square.EMPTY, Square.EMPTY),
                new Row(Square.EMPTY, Square.EMPTY, Square.EMPTY) });
        Game game = new Game(board);

        assertEquals(5, tmp(game.nextMove(Square.X)));

        game = new Game(
            new Board(new Row[] { new Row(Square.X, Square.O, Square.X),
                new Row(Square.O, Square.X, Square.EMPTY),
                new Row(Square.EMPTY, Square.O, Square.EMPTY) }));

        assertEquals(8, game.nextMove(Square.O));

        game = new Game(new Board(new Row[] { new Row(Square.X, Square.O, Square.X),
                new Row(Square.O, Square.X, Square.EMPTY),
                new Row(Square.EMPTY, Square.O, Square.EMPTY) }));
    

        assertEquals(0, tmp(game.nextMove(Square.X)));
        game = new Game(new Board(new Row[] { new Row(Square.X, Square.O, Square.X),
                new Row(Square.O, Square.X, Square.O),
                new Row(Square.O, Square.X, Square.X) }));

        assertEquals(-1, tmp(game.nextMove(Square.X)));
    
    };

    public void testFindWinningMove() {
        Board board = new Board(new Row[] { new Row(Square.X, Square.X, Square.EMPTY),
                new Row(Square.O, Square.O, Square.EMPTY),
                new Row(Square.EMPTY, Square.EMPTY, Square.EMPTY) });
        Game game = new Game(board);
        assertEquals(5, tmp(game.nextMove(Square.X)));
    }

    public void testWinConditions() {

        Board board = new Board(new Row[] { new Row(Square.X, Square.X, Square.X),
                new Row(Square.O, Square.O, Square.EMPTY),
                new Row(Square.EMPTY, Square.EMPTY, Square.EMPTY) });
        Game game = new Game(board);

        assertEquals(Square.X, game.winner());

    }
}

public enum Square {
    X, O, EMPTY
}

public class Row {
    private Square[] squares = new Square[BOARD_SIZE];

    public Row(Square a, Square b, Square c) {
        squares[0] = a;
        squares[1] = b;
        squares[2] = c;
    }

    public Square[] squares() {
        return squares.clone();
    }

    public void set(int index, Square value) {
        squares[index] = value;
    }

    public Square get(int index) {
        return squares[index];
    }

    public Row copy() {
        return new Row(squares[0], squares[1], squares[2]);
    }

    private boolean rowX() {
        return squares[0] == Square.X && squares[1] == Square.X && squares[2] == Square.X;
    }

    private boolean rowO() {
        return squares[0] == Square.O && squares[1] == Square.O && squares[2] == Square.O;
    }

    // Returns who is the winner in row. XXX --> X , OOO --> O , otherwise null
    public Square winner() {

        if (rowX()) {
            return Square.X;
        }

        if (rowO()) {
            return Square.O;
        }

        return null;

    }

}

public record Position(int row, int column) {

    private final int START = 0;

    public Position {
        if (row < START || row >= BOARD_SIZE || column < START || column >= BOARD_SIZE) {
            throw new IllegalArgumentException("Row and column must be between 0 and " + (BOARD_SIZE - 1));
        }
    }

    public static Position[] allPositions() {
        Position[] positions = new Position[BOARD_SIZE * BOARD_SIZE];
        int index = START;
        for (int row = START; row < BOARD_SIZE; row++) {
            for (int col = START; col < BOARD_SIZE; col++) {
                positions[index++] = new Position(row, col);
            }
        }
        return positions;
    }

}


//We can add a function to extract diagonals and columns , i still think rows are useful conceptually, 
// as representing a 2d board as array of rows is natural , unlike 1D
//Easily extendable to bigger boards, just change BOARD_SIZE constant, add number in a row that makes win and change row winner func .
public class Board {

    protected Row[] rows = new Row[BOARD_SIZE];

    public Board(Row[] rows) {
        this.rows = rows.clone();
    }

    public Square get(Position pos) {
        return rows[pos.row()].get(pos.column());
    }

    public void set(Position pos, Square value) {
        rows[pos.row()].set(pos.column(), value);
    }

    public Row[] rows_copy() {

        private final int START = 0;

        Row[] result = new Row[BOARD_SIZE];
        for (int i = START; i < BOARD_SIZE; i++) {
            result[i] = rows[i].copy();
        }
        return result;
    }

    public Board copy() {
        return new Board(rows_copy());
    }
    
}

public class Game {

    protected Board board;

    // StringBuffer s is starting board
    public Game(Board board) {
        this.board = board;
    }

    // Winner check - XXX or OOO in one of the rows
    // XXX --> winner = 'X'
    // OOO --> winner = 'O'
    // No winner --> return '-'
    public Square winner() {

        Square result = Square.EMPTY;

        for (Row r : board.rows_copy()) {
            if (r.winner() != null) {
                result = r.winner();
            }
        }

        return result;
    }

    // Return new Game object with updated board (player played at position i)
    public Game play(Position position, Square player) {

        Game result = new Game(board.copy());
        result.board.set(position, player);

        return result;

    }

    private Position winningMove(Square player) {

        for (Position pos : Position.allPositions()) {

            if (board.get(pos) == Square.EMPTY) {

                Game game = play(pos, player);
                if (game.winner() == player)
                    return pos;

            }
        }

        return null;
    }

    private Position firstEmptyCell() {

        for (Position pos : Position.allPositions()) {
            if (board.get(pos) == Square.EMPTY) {
                return pos;
            }
        }

        return null;

    }

    // Doesnt modify current board!
    // I think this the next move? It is shit - if we can win we win it otherwise we
    // pick first empty and then -1 on fail
    public Position nextMove(Square player) {

        Position result;

        if (winningMove(player) != null) {
            result = winningMove(player);
        }

        else if (firstEmptyCell() != null) {
            result = firstEmptyCell();
        }

        else {
            result = null;
        }
        return result;
    }

}