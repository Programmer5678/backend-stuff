package exercises.decorator2;

interface ReportType {
    void beforeRender();
    void beforeExport();
}

class HtmlReportType implements ReportType {
    @Override
    public void beforeRender() {
        System.out.println("Render HTML report");
    }

    @Override
    public void beforeExport() {
        System.out.println("Export HTML report");
    }
}

class PDFReportType implements ReportType {
    @Override
    public void beforeRender() {
        System.out.println("Render PDF report");
    }

    @Override
    public void beforeExport() {
        System.out.println("Export PDF report");
    }
}

interface ReportInterface {
    void export();
    void render();
}

class Report implements ReportInterface {

    private ReportType reportType;

    Report(ReportType reportType) {
        this.reportType = reportType;
    }

    @Override
    public void export() {
        reportType.beforeExport();
        System.out.println("This is the export itself");
    }

    @Override
    public void render() {
        reportType.beforeRender();
        System.out.println("This is the render itself");
    }
}

/* ===== DECORATOR ===== */
abstract class ReportDecorator implements ReportInterface {

    protected ReportInterface report;

    ReportDecorator(ReportInterface report) {
        this.report = report;
    }

    @Override
    public void render() {
        report.render();
    }

    @Override
    public void export() {
        report.export();
    }
}

class CacheReportDecorator extends ReportDecorator {
    CacheReportDecorator(ReportInterface report) {
        super(report);
    }

    @Override
    public void render() {
        System.out.println("Check cache");
        super.render();
    }
}

class SecureReportDecorator extends ReportDecorator {
    SecureReportDecorator(ReportInterface report) {
        super(report);
    }

    @Override
    public void export() {
        System.out.println("Encrypt data");
        super.export();
    }
}

/* ===== MAIN ===== */
public class File {
    public static void main(String[] args) {

        ReportInterface r1 = new Report(new HtmlReportType());
        ReportInterface r2 = new SecureReportDecorator(new Report(new HtmlReportType()));
        ReportInterface r3 = new CacheReportDecorator(
                new SecureReportDecorator(
                        new Report(new PDFReportType())));

        System.out.println("--- HTML ---");
        r1.render();
        r1.export();

        System.out.println("\n--- SECURE HTML ---");
        r2.render();
        r2.export();

        System.out.println("\n--- CACHED SECURE PDF ---");
        r3.render();
        r3.export();
    }
}
