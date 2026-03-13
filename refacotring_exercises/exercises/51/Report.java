import java.util.*;

public class Report {

    public Report() {
    }

    //map[offering] = [ list of student names ]
    Hashtable offeringToName = new Hashtable(); // offeringId students all cached here but name and are still pulled from db. 

    // Get all schedules --> loop through all offerings of all schedules
    //populates offeringToName by querying schedules table.  
    public void populateMap() throws Exception {
        Collection schedules = ScheduleRepo.all();
        for (Iterator eachSchedule = schedules.iterator(); eachSchedule.hasNext();) {
            Schedule schedule = (Schedule) eachSchedule.next();

            for (Iterator each = schedule.offerings.iterator(); each.hasNext();) {
                Offering offering = (Offering) each.next();
                populateMapFor(schedule, offering);
            }
        }
    }

    // Add schedule to offering, append to map[offering] schedule name. 
    private void populateMapFor(Schedule schedule, Offering offering) {
        ArrayList list = (ArrayList) offeringToName.get(new Integer(offering.getId().value()));
        if (list == null) {
            list = new ArrayList();
            offeringToName.put(new Integer(offering.getId().value()), list);
        }
        list.add(schedule.studentId());
    }

    public void writeOffering(StringBuffer buffer, ArrayList list, Offering offering) {
        //Print course name, times
        buffer.append(offering.getCourse().getName() + " " + offering.getDaysTimes() + "\n");
        //Prints student names( loop through table )
        for (Iterator iterator = list.iterator(); iterator.hasNext();) {
            String s = (String) iterator.next();
            buffer.append("\t" + s + "\n"); 
        }
    }


    // iterate through ( select * from offerings ) --> print ofering header, iterate with ( select * from schedule  where offeringId = offeringId) --> print 
    public void write(StringBuffer buffer) throws Exception {
        populateMap();

        Enumeration enumeration = offeringToName.keys(); //Get offerings from map keys, write them to buffer.    
        while (enumeration.hasMoreElements()) {
            Integer offeringId = (Integer) enumeration.nextElement(); // Get next offeringId
            ArrayList list = (ArrayList) offeringToName.get(offeringId); // Get offerings
            writeOffering(buffer, list, Offering.find(offeringId.intValue())); // select * from offerings where id = id;

        }

        buffer.append("Number of scheduled offerings: ");
        buffer.append(offeringToName.size());
        buffer.append("\n");
    }
}
