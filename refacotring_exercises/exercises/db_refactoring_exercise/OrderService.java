import java.sql.*;

public class OrderService {

    public void createOrder(int orderId, int personId, String personName, int amount)
            throws SQLException {

        DBCalls.insertOrders(orderId, personId, personName, amount);
        
    }
}
