import junit.framework.TestCase;
import java.util.List;
import java.util.Collection;

public class TestReport extends TestCase {

    public TestReport(String name) {
        super(name);
    }

    public void testEmptyReport() throws Exception {
        ScheduleRepo.deleteAll();
        Report report = new Report();
        StringBuffer buffer = new StringBuffer();
        report.write(buffer);

        assertEquals("Number of scheduled offerings: 0\n", buffer.toString());
    }

    public void testReport() throws Exception {

        
        final Kuka Bob = new Kuka(11);
        final Kuka Alice = new Kuka(12);

        ScheduleRepo.deleteAll();

        Course cs101 = Course.create("CS101", 3);
        cs101.save();

        Offering off1 = Offering.create(cs101, "M10");
        off1.save();

        Offering off2 = Offering.create(cs101, "T9");
        off2.save();

        ScheduleRepo.delete( Bob );
        // final int BOB = 11;
        Schedule s = new Schedule( Bob );

        s.add(off1);
        s.add(off2);
        ScheduleRepo.save(s);

        ScheduleRepo.delete( Alice );
        // final int ALICE = 9;
        Schedule s2 = new Schedule( Alice );

        s2.add(off1);
        ScheduleRepo.save(s2);

        Report report = new Report();
        StringBuffer buffer = new StringBuffer();
        report.write(buffer);

        String result = buffer.toString();

        String valid1 = "CS101 M10\n\tAlice\n\tBob\n"
                + "CS101 T9\n\tBob\n"
                + "Number of scheduled offerings: 2\n";

        String valid2 = "CS101 T9\n\tBob\n"
                + "CS101 M10\n\tAlice\n\tBob\n"
                + "Number of scheduled offerings: 2\n";

        assertTrue(result.equals(valid1) || result.equals(valid2));
    }
}
