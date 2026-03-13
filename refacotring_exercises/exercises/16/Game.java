import java.util.ArrayList;
import java.util.List;
import javax.swing.*;

class ScoreBoard {
    public int score = 0;
    public int id = 0;
    private List<ScoreObserver> observers = new ArrayList<>();



    public void addObserver(ScoreObserver observer) {
        observers.add(observer);
    }

    public void addId ( int id ){
        this.id = id;
    }

    public void addPoints(int points) {
        score += points;
        notifyObservers();
    }

    private void notifyObservers() {
        observers.forEach(obs -> obs.update(this));
    }

}

interface ScoreObserver {
    void update(ScoreBoard board);
}

class ScoreBoardWidget implements ScoreObserver {

    private JLabel label = new JLabel("No score");

    @Override
    public void update(ScoreBoard board) {
        label.setText("Score: " + board.score + ", Id: " + board.id );
    }

    public JLabel getLabel() {
        return label;
    }
}

class ScoreBoardString implements ScoreObserver {

    private String s = "No score";

    @Override
    public void update(ScoreBoard board) {
        s = "Score: " + board.score + ", Id: " + board.id ;
    }

    public void print() {
        System.out.println(s);
    }
}

public class Game {
    public static void main(String[] args) {

        JFrame frame = new JFrame("Game");

        ScoreBoard board = new ScoreBoard();
        board.addPoints(5);
        board.addPoints(10);
        board.addId(5);

        ScoreBoardString string = new ScoreBoardString();
        board.addObserver(string);
        string.print(); // "No score"

        ScoreBoardWidget widget = new ScoreBoardWidget();
        board.addObserver(widget);

        frame.add(widget.getLabel());
        frame.setSize(200, 100);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

    }
}
