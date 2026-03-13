
// Replaces original by replacement in template
public String replace(String template, String original, String replacement) {
    // Substitute for %ALTCODE%
    int templateSplitBegin = template.indexOf(original);
    int templateSplitEnd = templateSplitBegin + original.length();

    String templatePartOne = new String(template.substring(0, templateSplitBegin));
    String templatePartTwo = new String(template.substring(templateSplitEnd, template.length()));

    String res = new String(templatePartOne + replacement + templatePartTwo);

    return res;

}

public String altCode( String code ) {
    return code.substring(0, 5) + "-" + code.substring(5, 8);
}

public void substitute(
        String sourceTemplate,
        String reqId,
        PrintWriter out
) {
    try {
        String code = new String(reqId);

        out.print(
                replace(
                        replace(new String(sourceTemplate), "%CODE%", code),
                        "%ALTCODE%",
                        altCode(code)
                )
        );

    } catch (Exception e) {
        System.out.println("Error in substitute()");
    }
}
