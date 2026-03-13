package exercises.3444;

import java.util.*;
import java.io.*;

public class Report {


    public static void report(Writer out, List machines, Robot robot) throws IOException {
        out.write("FACTORY REPORT\n");


        //Iterate through machines list
        Iterator line = machines.iterator();
        while (line.hasNext()) {
            Machine machine = (Machine) line.next();
            machine.report(out);
        }

        out.write("\n");

        robot.report(out);
        
        out.write("========\n");
    }
}
