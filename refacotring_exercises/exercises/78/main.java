package exercises

import java.util.List;


public class main {

    Catalog catalog;

    public void setUp() {
        catalog = new Catalog();
        catalog.add("Hammer 10 lb");
        catalog.add("shirt XL blue");
        catalog.add("shirt L green");
        catalog.add("Halloween candle orange");
        catalog.add("Halloween candy gum");
    }

    public void testSimpleQuery() {
        List result = Interegator.itemsMatching (new StringQuery("shirt"), catalog );
        AssertEquals(2, result.size());
    }

    public void testOrQuery() {
        Query query = new OrQuery ( new StringQuery("shirt"), new StringQuery("Halloween"));
        List list = Interegator.itemsMatching (query, catalog );
        assertEquals(4, list.size());
    }

}


//Now it clearer to me why we have the matching in the Query class.
//The matching is the essenece of the Query, and we use inheritance to define different types of queries.
public abstract class Query {
    
    public boolean matches( String item );

}

public class StringQuery extends Query {

    private String text;

    public StringQuery(String text) {
        this.text = text;
    }

    public boolean matches( String item ){
        return item.contains(this.text);
    }


}


//If i want to make this faster i must couple it with StringQuery. 
//Instead of Or chain, and running itemsMatching twice i can have a list of string store inside Query and 
// the itemsMatching just checks if any of the strings in the list is contained in the item.
public class OrQuery extends Query {
    
    private Query left;
    private Query right;

    public OrQuery(Query left, Query right) {
        this.left = left;
        this.right = right;
    }


    public boolean matches( String item ) {
        return left.matches(item) || right.matches(item);
    }
}



public class Interregator  {

    public static List<String> itemsMatching ( Query query , Catalog catalog ) {
        return catalog.items().filter(item -> matches(item) ).toList();
    }


}



// public class Gulag {

//     public static Li

// }   

public class OriginalMatcher {

    public List<String> itemsMatching(StringQuery q, Catalog catalog){
        return catalog.items().filter(item -> matches(item) ).toList();
    }

}

public class OrOriginalMatcherDecorator {

    public 

}


public class Catalog {

    private List<String> items = new ArrayList<>();

    public void add(String item){
        items.add(item);
        // for word in items --> words[ word ] . append item.
    }

    public Stream<String> items() {
        return items.stream();
    }


}
