package exercises.42;

abstract class CardModel {
    String value;
    boolean faceUp;
    protected String s;

    CardModel(String value) {
        this.value = value;
        this.faceUp = false;
    }

    void flip() {
        faceUp = !faceUp;
        notifyObservers();
    }

    abstract String getDescription();

    // Observer logic
    private CardView observer;
    void addObserver(CardView view) {
        this.observer = view;
    }
    void notifyObservers() {
        if (observer != null) observer.update();
    }
}

class NumberCardModel extends CardModel {


    NumberCardModel(String value) {
        super(value);
        s = "Number";
    }

    @Override
    String getDescription() {
        return "Number card: " + value;
    }
}

class FaceCardModel extends CardModel {

    
    FaceCardModel(String value) {
        super(value);
        s = "Face";
    }

    @Override
    String getDescription() {
        return "Face card: " + value;
    }
}
