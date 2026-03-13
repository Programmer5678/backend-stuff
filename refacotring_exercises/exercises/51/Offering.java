import java.sql.*;
import java.util.ArrayList;

public class Offering {

    private DBIntField id;
    private Course course;
    private String daysTimes;

    private static final DBTable tb = new DBTable("offering");
    private static final DBColumn idCol = new DBColumn(tb, "ID");


    public Offering(DBIntField id, Course course, String daysTimesCsv) {
        this.id = id;
        this.course = course;
        this.daysTimes = daysTimesCsv;
    }

    public DBIntField getId() {
        return id;
    }

    public Course getCourse() {
        return course;
    }

    public String getDaysTimes() {
        return daysTimes;
    }

    public String toString() {
        return "Offering " +   String.valueOf(getId().value())   + ": " + getCourse() + " meeting " + getDaysTimes();
    }


    //Make this an abstract function
    private static Offering offeringOf( ResultSet offerings ) {

        private static Course course(){
            String courseName = offerings.getString("Course");
            return Course.find(courseName); 
        }

        if (queryRes.next() == false)
            return null;

        int id = offerings.getInt("ID");
        String dateTime = offerings.getString("DateTime");


        return new Offering(new DBIntField(id), course(), dateTime);
    }

    //Could make this an inherited func 
    // We get result from DB and return it.
    public static Offering find(int id) {

        // cache.add(id, offering)

        ResultSet queryRes = idCol.queryAll( new DBIntField(id) );

        return offeringOf( queryRes );

    }

    // Get new id, add course.name, daysTimeCsv string. No delete this time.
    public static Offering create(Course course, String daysTimesCsv) throws Exception {

        int nextId = idCol.max() + 1;

        tb.insert(new ArrayList<>( String.valueOf(nextId), course.getName(), daysTimesCsv) );

        return new Offering(new DBIntField(nextId), course, daysTimesCsv);
    }

    public void save() throws Exception {

        idCol.delete(new DBIntField(id));
        tb.insert( new ArrayList<>(id, course.getName(), daysTimes) );
        
    }



}
