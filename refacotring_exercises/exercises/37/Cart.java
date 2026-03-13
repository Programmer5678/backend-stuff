package exercises.37;

public class Cart {

    public List<Purchase> purchases; 

    Cart( List<Purchase> purchases ) {
        this.purchases = new ArrayList<>(purchases);
    }


    public int cost() {
        return purchases.reduce( (total, purchase) -> total+purchase.cost() );
    }

    public int maxDays() {
        return purchases.reduce( (total, purchase) -> max( total, purchase.days() ) );
    }
    

}
