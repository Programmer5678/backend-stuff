package exercises.decorator;
//Interface for both pizza and decorator
class PizzaInterface {
    String description();
    int cost();
}

class BasicPizza implements PizzaInterface{

    int cost = 0;
    String description = "";

    String description(){
        return "Pizza. Yum yum!";
    }

    int cost() {
        return cost;
    }

}


abstract class PizzaDecorator implements PizzaInterface {

    protected PizzaInterface decoratedPizza;
    
    PizzaDecorator( PizzaInterface decoratedPizza ) {
        this.decoratedPizza = decoratedPizza;
    }

    @Override
    String description() {
        return decoratedPizza.description();
    }

    @Override
    int cost() {
        return decoratedPizza.cost();
    }

}




class NothingDecorator extends PizzaDecorator{

    PizzaDecorator( PizzaInterface decoratedPizza ) {
        super(decoratedPizza);
    }


}

class OliveDecorator extends PizzaDecorator{


    PizzaDecorator( PizzaInterface decoratedPizza ) {
        super(decoratedPizza);
    }

    @Override
    String description() {
        return decoratedPizza.description() + " mmm even better with olives!";
    }

    @Override
    int cost() {
        return decoratedPizza.cost() + 5;
    }

}


class CheeseDecorator extends PizzaDecorator{


    PizzaDecorator( PizzaInterface decoratedPizza ) {
        super(decoratedPizza);
    }

    @Override
    String description() {
        return decoratedPizza.description() + " mmm even better with cheese!";
    }

    @Override
    int cost() {
        return decoratedPizza.cost() + 12;
    }

}
