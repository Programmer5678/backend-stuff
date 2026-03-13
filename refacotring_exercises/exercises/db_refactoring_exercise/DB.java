import java.sql.*;

public class DB {
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(
            "jdbc:h2:mem:testdb", "sa", ""
        );
    }
}
