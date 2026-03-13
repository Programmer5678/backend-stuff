package exercises.37;

public class ShippingOption {
    private int cost;
    private int days;

    ShippingOption( int cost, int days ) {
        this.cost = cost;
        this.days = days;
    }

    public int cost() {
        return cost;
    }

    public int days() {
        return days;
    }

}
