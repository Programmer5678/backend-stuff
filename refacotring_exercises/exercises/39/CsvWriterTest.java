package exercises.39;

import junit.framework.TestCase;

public class CsvWriterTest extends TestCase {

    public CsvWriterTest(String name) {
        super(name);
    }

    public void testWriter() {
        Csv csv = new Csv();

        String[][] lines = new String[][] {
            new String[] {},
            new String[] {"only one field"},
            new String[] {"two", "fields"},
            new String[] {"", "contents", "several words included"},
            new String[] {",", ",", "embedded , commas, included", "trailing comma,"},
            new String[] {"\"", "embedded \" quotes", "multiple \"\"\" quotes\"\""},
            new String[] {"mixed commas, and \"quotes\"", "simple field"}
        };
        

        Writer writer = new StringWriter();
        writer.write( csv.linesToString(lines) );
    }
}
