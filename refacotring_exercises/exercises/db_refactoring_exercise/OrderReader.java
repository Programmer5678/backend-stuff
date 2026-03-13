import java.sql.*;
import java.util.ArrayList;
import java.util.List;



public class OrderReader {

    public void printOrders() throws SQLException {

        List<Order> orders = DBCalls.readOrders();
        
        orders.forEach( order -> System.out.println(
                order.orderId() + " | " +
                order.personId() + " | " +
                order.amount()
            ) );

    }
}
