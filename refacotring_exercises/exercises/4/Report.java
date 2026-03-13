package factory;

import java.util.List;
import java.io.Writer;
import java.io.IOException;
import java.util.Iterator;

public class Report {
    public static void report(Writer out, List<Machine> machines, Robot robot) throws IOException {

        reportHeader(out);
        reportMachines(out, machines);
        reportRobot(out, robot);
        reportFooter(out);
    }

    private static void reportFooter( Writer out ) {
        out.write("\n");
        out.write("========\n");
    }

    private static void reportHeader ( Writer out ) {
        out.write("FACTORY REPORT\n");
    }

    private static void reportRobot(Writer out, Robot robot) throws IOException {
        out.write("Robot");
        if (robot.location() != null)
            out.write(" location=" + robot.location().name());
        if (robot.bin() != null)
            out.write(" bin=" + robot.bin());
    }

    private static void reportMachines(Writer out, List<Machine> machines) throws IOException {
        Iterator<Machine> line = machines.iterator();

        while (line.hasNext()) {
            Machine machine = line.next();

            reportMachine(out, machine);
            out.write("\n");
        }
    }

    private static void reportMachine(Writer out, Machine aMachine) throws IOException {
        out.write("Machine " + aMachine.name());
        if (aMachine.bin() != null)
            out.write(" bin=" + aMachine.bin());

        out.write("\n");
    }
}
