package exercises.37;

import java.io.IOException;
import java.io.Writer;
import java.util.Arrays;

public class Csv {

    public String linesToString(String[][] lines) {
        StringBuilder sb = new StringBuilder();
        for (String[] line : lines) {
            sb.append(lineToString(line));
        }
        return sb.toString();
    }

    private String lineToString(String[] fields) {
        StringBuilder sb = new StringBuilder();

        if (fields.length > 0) {
            sb.append(fieldToString(fields[0]));
        }

        for (int i = 1; i < fields.length; i++) {
            sb.append(',');
            sb.append(fieldToString(fields[i]));
        }

        sb.append('\n');
        return sb.toString();
    }

    private String fieldToString(String field) {
        if (field.indexOf(',') != -1 || field.indexOf('"') != -1) {
            return quotedToString(field);
        }
        return field;
    }

    private String quotedToString(String field) {
        StringBuilder sb = new StringBuilder();
        sb.append('"');

        for (int i = 0; i < field.length(); i++) {
            char c = field.charAt(i);
            if (c == '"') {
                sb.append("\"\"");
            } else {
                sb.append(c);
            }
        }

        sb.append('"');
        return sb.toString();
    }
}
