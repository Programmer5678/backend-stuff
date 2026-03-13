package exercises.42;


class CardView {

    CardModel model;
    
    CardView(CardModel model) {
        this.model = model;
        model.addObserver(this);
    }

    void update() {
        if (model.faceUp)
            System.out.println(model.s + " card: " + model.value);
        else
            System.out.println(model.s + " card: [hidden]");
    }
}