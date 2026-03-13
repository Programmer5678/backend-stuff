import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class DBContext implements AutoCloseable {

    private Connection conn;
    private Statement statement;
    private final String url = "jdbc:odbc:Reggie";

    public DBContext() throws Exception {
        conn = DriverManager.getConnection(url, "", "");
        statement = conn.createStatement();
    }

    public int executeUpdate(String sql) throws Exception {
        return statement.executeUpdate(sql);
    }

    public ResultSet executeQuery(String sql) throws Exception {
        return statement.executeQuery(sql);
    }

    @Override
    public void close() {
        try {
            statement.close();
        } catch (Exception ignored) {}

        try {
            conn.close();
        } catch (Exception ignored) {}
    }
}
