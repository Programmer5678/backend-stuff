import java.util.*;
import java.sql.*;

// Goal - seperate DB stuff from non-DB stuff.
// add, authorizeOverload, analysis, checkDuplicate, checkOverlap, toString
// These deal only with the actual data stored inside schedule. name, credits, overloadAuthorized, schedule

// Next we have methods that touch DB. 
// Almost all are static, 
// like find - we query all by name then return new Schedule( ... )
// But one isnt - remove schedules with name, then insert new ones with offerings from class. 

//add changes credits
// maybe make it constant and return a new Schedule instead ?

//Why  add a pure function ? --> because i want to move the name, credits to an "immutable dataclass".
// Then what?
// We still have update function no?
// Yeah so what?
// We crete a new class with just name, credits and inner manipulation functions 
// and say call it Schedule and we can have ScheduleDB class with the DB stuff.

public class Student {
    int id;
    String name;

    Student(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public String toString() {
        return "Student " + name;
    }
}

public class Schedule {

    static final int minCredits = 12;
    static final int maxCredits = 18;

    private Kuka studentId;

    // Student student;
    int credits = 0;

    boolean overloadAuthorized = false;
    ArrayList offerings = new ArrayList();

    public Schedule(Kuka studentId) {
        this.studentId = studentId;
    }

    // public String name(){
    // return student.name;
    // }

    public Kuka studentId() {
        return studentId;
    }

    public void add(Offering offering) {

        credits += offering.getCourse().getCredits();
        offerings.add(offering);
    }

    public void authorizeOverload(boolean authorized) {
        overloadAuthorized = authorized;
    }

    public List analysis() {
        ArrayList result = new ArrayList();
        if (credits < minCredits)
            result.add("Too few credits");
        if (credits > maxCredits && !overloadAuthorized)
            result.add("Too many credits");

        checkDuplicateCourses(result);
        checkOverlap(result);
        return result;
    }

    public void checkDuplicateCourses(ArrayList analysis) {
        HashSet courses = new HashSet();
        for (int i = 0; i < offerings.size(); i++) {
            Course course = ((Offering) offerings.get(i)).getCourse();
            if (courses.contains(course))
                analysis.add("Same course twice - " + course.getName());
            courses.add(course);
        }
    }

    public void checkOverlap(ArrayList analysis) {
        HashSet times = new HashSet();
        for (Iterator iterator = .iterator(); iterator.hasNext();) {
            Offering offering = (Offering) iterator.next();
            String daysTimes = offering.getDaysTimes();
            StringTokenizer tokens = new StringTokenizer(daysTimes, ",");
            while (tokens.hasMoreTokens()) {
                String dayTime = tokens.nextToken();
                if (times.contains(dayTime))
                    analysis.add("Course overlap - " + dayTime);
                times.add(dayTime);
            }
        }
    }

    public String toString() {
        // return "Schedule " + student.toString() + ": " + offerings;
        return "Schedule " + String.valueOf(studentId().value()) + ": " + offerings;
    }

}

public static class ScheduleRepo {

    private static final DBTable tb = new DBTable("schedule");
    private static final DBColumn studentIdCol = new DBColumn(tb, "studentId");

    // ScheduleRepo(context) --> DBTable, DBColumn contexts. + Cache for find etc.
    // Cache is implemented somewhere else ,
    // maybe even take it as arg as wellas context because we want to share them

    public static void save(Schedule schedule) throws Exception {

        studentIdCol.delete( schedule.studentId());

        for (int i = 0; i < schedule.offerings.size(); i++) {
            Offering offering = (Offering) schedule.offerings.get(i);
            tb.insert(new ArrayList<>(
                    List.of(
                            schedule.studentId(),
                            new DBIntField(offering.getId().value())))); 
        }

    }

    private static Schedule scheduleOf(ResultSet schedules) {

        Schedule schedule = schedules.getString(studentIdCol.name());
        while (schedules.next()) {
            int offeringId = schedules.getInt("OfferingId");
            Offering offering = Offering.find(offeringId);
            schedule.add(offering);
        }
        return schedule;

    }

    public static Schedule find(Kuka name) {

        ResultSet queryRes = studentIdCol.queryAll( name );

        return scheduleOf(queryRes);
    }

    public static void delete(Kuka id) throws Exception {

        studentIdCol.delete( id);

    }

    public static void deleteAll() throws Exception {

        tb.deleteAll();

    }

    public static Collection all() throws Exception {

        ArrayList result = new ArrayList();
        ResultSet schedules = studentIdCol.getAllDistinct();
        while (schedules.next()) {

            // Get the Schedule repo
            Kuka scheduleName = new Kuka( String.valueOf(schedules.getInt(studentIdCol.name())) );
            Schedule schedule = ScheduleRepo.find(scheduleName);
            result.add(schedule);

        }

        return result;
    }

}
