import junit.framework.TestCase;
import java.util.List;
import java.util.Collection;

public class TestSchedule extends TestCase {

    final Kuka Bob = new Kuka(11);
    final Kuka Alice = new Kuka(12);
    final Kuka ExampleStudentId = new Kuka(13);

    final DBIntField ExampleId = new DBIntField(1);

    public TestSchedule(String name) {
        super(name);
    }

    public void testMinCredits() {
        Schedule schedule = new Schedule( ExampleStudentId );
        Collection analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Too few credits"));
    }

    public void testJustEnoughCredits() {
        Course cs110 = new Course("CS110", 11);
        Offering mwf10 = new Offering(ExampleId, cs110, "M10,W10,F10");

        Schedule schedule = new Schedule( ExampleStudentId );
        schedule.add(mwf10);
        List analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Too few credits"));

        schedule = new Schedule( ExampleStudentId );
        Course cs101 = new Course("CS101", 12);
        Offering th11 = new Offering(ExampleId, cs101, "T11,H11");
        schedule.add(th11);
        analysis = schedule.analysis();
        assertEquals(0, analysis.size());
    }

    public void testMaxCredits() {
        Course cs110 = new Course("CS110", 20);
        Offering mwf10 = new Offering(ExampleId, cs110, "M10,W10,F10");

        Schedule schedule = new Schedule( ExampleStudentId );
        schedule.add(mwf10);
        List analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Too many credits"));

        schedule.authorizeOverload(true);
        analysis = schedule.analysis();
        assertEquals(0, analysis.size());
    }

    public void testJustBelowMax() {
        Course cs110 = new Course("CS110", 19);
        Offering mwf10 = new Offering(ExampleId, cs110, "M10,W10,F10");

        Schedule schedule = new Schedule(ExampleStudentId );
        schedule.add(mwf10);
        List analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Too many credits"));

        schedule = new Schedule( ExampleStudentId );
        Course cs101 = new Course("CS101", 18);
        Offering th11 = new Offering(ExampleId, cs101, "T11,H11");
        schedule.add(th11);
        analysis = schedule.analysis();
        assertEquals(0, analysis.size());
    }

    public void testDupCourses() {
        Course cs110 = new Course("CS110", 6);
        Offering mwf10 = new Offering(ExampleId, cs110, "M10,W10,F10");
        Offering th11 = new Offering(ExampleId, cs110, "T11,H11");

        Schedule schedule = new Schedule( ExampleStudentId );
        schedule.add(mwf10);
        schedule.add(th11);
        List analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Same course twice - CS110"));
    }

    public void testOverlap() {
        Schedule schedule = new Schedule( ExampleStudentId );

        Course cs110 = new Course("CS110", 6);
        Offering mwf10 = new Offering(ExampleId, cs110, "M10,W10,F10");
        schedule.add(mwf10);

        Course cs101 = new Course("CS101", 6);
        Offering mixed = new Offering(ExampleId, cs101, "M10,W11,F11");
        schedule.add(mixed);

        List analysis = schedule.analysis();
        assertEquals(1, analysis.size());
        assertTrue(analysis.contains("Course overlap - M10"));

        Course cs102 = new Course("CS102", 1);
        Offering mixed2 = new Offering(ExampleId, cs102, "M9,W10,F11");
        schedule.add(mixed2);

        analysis = schedule.analysis();
        assertEquals(3, analysis.size());
        assertTrue(analysis.contains("Course overlap - M10"));
        assertTrue(analysis.contains("Course overlap - W10"));
        assertTrue(analysis.contains("Course overlap - F11"));
    }

    public void testCourseCreate() throws Exception {
        Course c = Course.create("CS202", 1);
        Course c2 = Course.find("CS202");
        assertEquals("CS202", c2.getName());
        Course c3 = Course.find("Nonexistent");
        assertNull(c3);
    }

    public void testOfferingCreate() throws Exception {
        Course c = Course.create("CS202", 2);
        Offering offering = Offering.create(c, "M10");
        assertNotNull(offering);
    }

    public void testPersistentSchedule() throws Exception {
        ScheduleRepo.delete(Bob);
        Schedule s = new Schedule(Bob);

        assertNotNull(s);
    }

    public void testScheduleUpdate() throws Exception {
        Course cs101 = Course.create("CS101", 3);
        cs101.save();

        Offering off1 = Offering.create(cs101, "M10");
        off1.save();

        Offering off2 = Offering.create(cs101, "T9");
        off2.save();

        ScheduleRepo.delete( Bob );
        Schedule s = new Schedule(Bob);

        s.add(off1);
        s.add(off2);
        ScheduleRepo.save(s);

        ScheduleRepo.delete(Alice);
        Schedule s2 = new Schedule(Alice);
        s2.add(off1);
        ScheduleRepo.save(s2);

        Schedule s3 = ScheduleRepo.find(Bob);
        assertEquals(2, s3.offerings.size());
        Schedule s4 =  ScheduleRepo.find(Alice);
        assertEquals(1, s4.offerings.size());
    }
}
