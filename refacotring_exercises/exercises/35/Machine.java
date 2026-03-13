package exercises.3444;

public class Machine {

    String name;
    String location;
    String bin;

    public Machine(String name, String location) {
        this.name = name;
        this.location = location;
    }

    public String take() {
        String result = bin;
        bin = null;
        return result;
    }

    public String bin() {
        return bin;
    }

    public void put(String bin) {
        this.bin = bin;
    }

    public String name() {
        return name;
    }


    public static void report(Writer out) {

        out.write("Machine " +  name());
            if ( bin() != null) {
                out.write(" bin=" + bin());
            }
        out.write("\n");

    }


}
