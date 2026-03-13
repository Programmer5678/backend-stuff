import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

public class DBContext implements AutoCloseable {

    private Connection conn;
    private boolean commited;
    private final String url = "jdbc:h2:mem:testdb";

    public DBContext() {
        
        try{
    
            conn = DriverManager.getConnection(url, "sa", "");
            conn.setAutoCommit(false);

        }

        catch(Exception e){}
    }

    public void commit() throws SQLException {
        conn.commit();
        commited = true;
    }

    public PreparedStatement prepareStatement(String sql){
        return conn.prepareStatement(sql);
    }


    // public Connection getConnection() {
    //     return conn;
    // }

    @Override
    public void close() {

        try {

            if (!commited) {
                conn.rollback();
            }

        }

        finally {

            try {
                conn.close();
            } catch (Exception ignored) {
            }
        }

    }



}
