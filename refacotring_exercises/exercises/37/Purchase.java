package exercises.37;

public class Purchase {
    private Item item;
    private ShippingOption shipping;

    Purchase(Item item, ShippingOption shipping) {
        this.item = item;
        this.shipping = shipping;
    }

    public int cost() {
        return item.cost() + shipping.cost();
    }

    public int days(){
        return shipping.days();
    }

}
