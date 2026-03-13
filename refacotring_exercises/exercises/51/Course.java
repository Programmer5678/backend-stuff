import java.sql.*;
import java.util.ArrayList;

public class Course {

    private String name;
    private int credits;

    private static final DBTable tb = new DBTable("course");
    private static final DBColumn nameCol = new DBColumn(tb, "Name");



    Course(String name, int credits) {
        this.name = name;
        this.credits = credits;
    }

    public int getCredits() {
        return credits;
    }

    public String getName() {
        return name;
    }



    private static Offering courseOf( ResultSet course ) {

        if (!course.next())
            return null;


        String name = course.getString(nameCol.name());
        int credits = course.getInt("Credits");
        return new Course(name, credits);

    }

    public static Course find(String name) {

        ResultSet queryRes = nameCol.queryAll( new DBStringField(name) );

        return courseOf(queryRes);
    }



    // Create a course --> using drivermanager statement.
    // DB - delete if course exists then add name, credits
    public static Course create(String name, int credits) throws Exception {


        nameCol.delete(new DBStringField(name));

        tb.insert(   new ArrayList<>(List.of(new DBStringField(name), new DBIntField(credits)))   );

        return new Course(name, credits);
    }

    public void save() throws Exception {

        nameCol.delete(new DBStringField(name));
        tb.insert(   new ArrayList<>(List.of(new DBStringField(name), new DBIntField(credits)))  ) 

    }


}
