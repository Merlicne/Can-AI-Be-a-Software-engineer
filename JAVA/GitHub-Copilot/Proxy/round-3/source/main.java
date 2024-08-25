// Database.java
public interface Database {
    void create(String data);
    String read(int id);
    void update(int id, String data);
    void delete(int id);
}

// RealDatabase.java
public class RealDatabase implements Database {
    @Override
    public void create(String data) {
        System.out.println("Creating data: " + data);
    }

    @Override
    public String read(int id) {
        System.out.println("Reading data with id: " + id);
        return "Data" + id;
    }

    @Override
    public void update(int id, String data) {
        System.out.println("Updating data with id: " + id + " to " + data);
    }

    @Override
    public void delete(int id) {
        System.out.println("Deleting data with id: " + id);
    }
}

// DatabaseProxy.java
public class DatabaseProxy implements Database {
    private RealDatabase realDatabase;

    public DatabaseProxy() {
        this.realDatabase = new RealDatabase();
    }

    @Override
    public void create(String data) {
        System.out.println("Proxy: Creating data");
        realDatabase.create(data);
    }

    @Override
    public String read(int id) {
        System.out.println("Proxy: Reading data");
        return realDatabase.read(id);
    }

    @Override
    public void update(int id, String data) {
        System.out.println("Proxy: Updating data");
        realDatabase.update(id, data);
    }

    @Override
    public void delete(int id) {
        System.out.println("Proxy: Deleting data");
        realDatabase.delete(id);
    }
}

// API.java
public class API {
    private Database database;

    public API() {
        this.database = new DatabaseProxy();
    }

    public void createData(String data) {
        database.create(data);
    }

    public String readData(int id) {
        return database.read(id);
    }

    public void updateData(int id, String data) {
        database.update(id, data);
    }

    public void deleteData(int id) {
        database.delete(id);
    }

    public static void main(String[] args) {
        API api = new API();
        api.createData("Sample Data");
        System.out.println(api.readData(1));
        api.updateData(1, "Updated Data");
        api.deleteData(1);
    }
}