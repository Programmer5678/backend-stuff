package exercises.db_refactoring_exercise;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class DBCalls {

    private DBContext db;

    public DBCalls(DBContext dbContext) throws SQLException {
        this.db = dbContext;
    }

    private String name(ResultSet rs) throws SQLException {
        if (rs.next()) {
            return rs.getString("full_name");
        } else {
            return null;
        }
    }


    // this can be split to 2.  order_id, person_id, amount insert. then update of person_name(which will be deprecated later)
    private void insertOrdersCore(int orderId, int personId, int amount) throws SQLException {

        PreparedStatement insertQuery = db.prepareStatement(
                "INSERT INTO Orders (order_id, person_id, amount) VALUES (?, ?, ?)");

        insertQuery.setInt(1, orderId);
        insertQuery.setInt(2, personId);
        // insertQuery.setString(3, personName);
        insertQuery.setInt(3, amount);

        insertQuery.executeUpdate();

    }


    public void insertOrders(int orderId, int personId, String personName, int amount) throws SQLException {

        updatePersonPeople(personId, personName);
        insertOrdersCore(orderId, personId, amount);

    }

    public List<Order> readOrders() throws SQLException {

        PreparedStatement stmt = db.prepareStatement("SELECT order_id, person_id, amount FROM Orders");
        ResultSet order = stmt.executeQuery();

        List<Order> result = new ArrayList<>();
        while (order.next()) {
            result.add(
                    new Order(order.getInt("order_id"), order.getInt("person_id"), order.getInt("amount")));
        }

        return result;

    }













    private void f3(int personId, String personName) throws SQLException {

        PreparedStatement insertQuery = db.prepareStatement(
                    "INSERT INTO People ( person_id, full_name ) VALUES ( ?, ? )");
        insertQuery.setInt(1, personId);
        insertQuery.setString(2, personName);

        insertQuery.executeUpdate();
    
    }

    private void updatePersonPeople(int personId, String personName) throws SQLException {

        PreparedStatement matchingPersonQuery = db.prepareStatement(
                "SELECT person_id, full_name FROM People WHERE person_id = ?");
        matchingPersonQuery.setInt(1, personId);
        ResultSet matchingPerson = matchingPersonQuery.executeQuery();
        String matchingPersonName = name(matchingPerson);

        if (matchingPersonName == null) {
            f3(personId, personName);
        }

        else if (!matchingPersonName.equals(personName)) {
            throw new SQLException("Inconsistent person name");
            // Otherwise Person already exists with the same name, do nothing
        }

    }



    private void g2(int personId, String newName) throws SQLException {
        PreparedStatement updateQuery = db.prepareStatement(
                "UPDATE People SET full_name = ? WHERE person_id = ?");

        updateQuery.setString(1, newName);
        updateQuery.setInt(2, personId);
        updateQuery.executeUpdate();
    }


    public void updateOrders(int personId, String newName) throws SQLException {
        g2(personId, newName);
    }

    private void h2() throws SQLException {

        PreparedStatement stmt = db.prepareStatement("UPDATE People SET full_name = UPPER(full_name)");
        stmt.executeUpdate();

    }

    public void normalizeNames() throws SQLException {

        h2();

    }

}


public class DBTest {
    private static void assertConsistent(DBContext db) throws SQLException {
        PreparedStatement stmt = db.prepareStatement("SELECT person_name, full_name FROM People");
        ResultSet res = stmt.executeQuery();
        
        while( res.next() ){
            assert( res.getString("person_name").equals( res.getString("full_name") ) );
        }
        
    }

    public static void testInsertOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            assertConsistent(db);

        }

    }

    public static void testNormalizeNamesOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            dbCalls.normalizeNames();

            assertConsistent(db);
        }

    }

    public static void testUpdateOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            OrderService orderService = new OrderService();
            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            dbCalls.updateOrders(1, "Johnny Doe");

            assertConsistent(db);

        }

    }
}

















































public class OldDBCallsTest {

    private static void assertConsistent(DBContext db) throws SQLException {

        PreparedStatement stmt = db.prepareStatement( "SELECT DISTINCT person_id, person_name
        FROM Orders ORDER BY person_id" );
        ResultSet res = stmt.executeQuery();

        PreparedStatement stmt2 = db.prepareStatement( "SELECT person_id, person_name
        FROM People ORDER BY person_id" );
        ResultSet res2 = stmt2.executeQuery();

        while(true){

            res = res.next();
            res2 = res2.next();

            if ( res == null ){
                assert( res2 == null );
                break;
            }

            assert( res.getInt("person_id") == res2.getInt("person_id") );
            assert( res.getString("person_name").equals(res2.getString("person_name")) );

        }


    }

    public static void testInsertOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            assertConsistent(db);

        }

    }

    public static void testNormalizeNamesOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            dbCalls.normalizeNames();

            assertConsistent(db);
        }

    }

    public static void testUpdateOrders() throws SQLException {

        try (DBContext db = new DBContext()) {
            DBCalls dbCalls = new DBCalls(db);

            OrderService orderService = new OrderService();
            dbCalls.insertOrders(1, 1, "John Doe", 100);
            dbCalls.insertOrders(2, 2, "Jane Smith", 200);

            dbCalls.updateOrders(1, "Johnny Doe");

            assertConsistent(db);

        }

    }

}