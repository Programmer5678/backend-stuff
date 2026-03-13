import java.sql.*;

public class OrderUpdater {

    public void renamePerson(int personId, String newName)
            throws SQLException {

        DBCalls.updateOrders(personId, newName);
    }
}
