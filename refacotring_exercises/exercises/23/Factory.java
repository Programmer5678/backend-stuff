public interface Driver {
    void find();
    void save();
}

class MemoryDriver implements Driver {

    public MemoryDriver() {}

    @Override
    public void find() {
        System.out.println("memory driver find");
    }

    @Override
    public void save() {
        System.out.println("memory driver save");
    }
}

class DebugDriver implements Driver {

    public DebugDriver() {}

    @Override
    public void find() {
        System.out.println("debug driver find");
    }

    @Override
    public void save() {
        System.out.println("debug driver save");
    }
}

class ProductionDriver implements Driver {

    public ProductionDriver() {}

    @Override
    public void find() {
        System.out.println("production driver find");
    }

    @Override
    public void save() {
        System.out.println("production driver save");
    }
}

class Factory {

    private Class<? extends Driver> driverClass;

    public Factory(String driverClassName) {
        try {
            this.driverClass =
                (Class<? extends Driver>) Class.forName(driverClassName);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public Driver getDriver() {
        try {
            return driverClass.getDeclaredConstructor().newInstance();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

public class Main {
    public static void main(String[] args) {

        Factory factory = new Factory("MemoryDriver");
        Driver driver = factory.getDriver();

        driver.find();
        driver.save();
    }
}
