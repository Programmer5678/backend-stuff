import java.sql.ResultSet;
import java.util.List;

public class DBTable {

    private String name;
    private DBContext db;

    public DBTable(DBContext db, String name) {
        this.name = name;
    }

    public String name() {
        return this.name;
    }

    public void insert(List<DBField> params) {

        List<String> params_sql;
        for ( DBField param : params) {
            params_sql.add(param.sql());
        }


        db.executeUpdate("INSERT INTO " + name + " VALUES( " + String.join(",", params_sql) + " );");
    }

    public void deleteAll() {
        db.executeUpdate("DELETE * FROM " + name);
    }
}



//This is general DBColumn - so i cant pass in userId.
//But if this is general how can it accept plain String?
// what if i want to pass in Int instead?
// So i need to change class to accomodate this need for generality. 
// Only then will i be able to send a general object.
//Tommorow task is to refactor this into proper db 
// Then add the general object with name and its implementation will dictate the type. Something like that lol.
public class DBColumn {
    private DBTable tb;
    private String name;

    public DBColumn(DBTable tb, String name) {
        this.tb = tb;
        this.name = name;
    }

    public String name(){
        return name;
    }

    public ResultSet queryAll(DBField field) {


        try (DBContext db = new DBContext()) {

            try {

                return db.executeQuery("SELECT * FROM " + tb.name() + " WHERE " + name + " = " + field.sql() + ";");

            }

            catch (Exception ex) {
                return null;
            }

        }

    }

    public void delete(DBField toDelete) {

        try (DBContext db = new DBContext()) {
            db.executeUpdate(
                    "DELETE FROM " + tb.name() + " WHERE " + name + " = " + toDelete.sql()  + ";");
        }

    }

    public int max(){
        try (DBContext db = new DBContext()) {
            return db.executeQuery("SELECT MAX(" + name + ") FROM " + tb.name() + ";").next();
        }
    }

    public ResultSet getAllDistinct() {
        try (DBContext db = new DBContext()) {
            return db.executeQuery("SELECT DISTINCT " + name + " FROM schedule;");
        }
    }

}


public abstract class DBField<T> {

    private T value;

    public DBField(T value){
        this.value = value;
    }
    public T value(){
        return value;
    }

    public abstract String sql();
}

public class DBStringField extends DBField<String>{

    public DBStringField(String value){
        super(value);
    }
    
    @Override
    public String sql(){
        return "'" + value() + "'";
    }
}

public class Kuka extends DBIntField {


    public Kuka(Integer value){
        super(value);
    }

    
}

public class DBIntField extends DBField<Integer>{

    public DBIntField(Integer value){
        super(value);
    }
    
    @Override
    public String sql(){
        return String.valueOf(value());
    }
}