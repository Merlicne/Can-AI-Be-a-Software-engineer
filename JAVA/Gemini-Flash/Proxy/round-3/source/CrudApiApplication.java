import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CrudApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(CrudApiApplication.class, args);
    }

    @Bean
    public DatabaseOperations databaseOperations(DatabaseManager databaseManager) {
        return new DatabaseProxy(databaseManager);
    }
}

// Proxy Interface
interface DatabaseOperations {
    void create(String data);
    String read(int id);
    void update(int id, String data);
    void delete(int id);
}

// Real Subject Class
@org.springframework.stereotype.Repository
class DatabaseManager implements DatabaseOperations {

    // Inject the repository here for database interactions
    // You can use Spring Data JPA or JDBC
    // Example using Spring Data JPA with an entity named "DataEntity"
    @org.springframework.beans.factory.annotation.Autowired
    private DataEntityRepository dataEntityRepository;

    @Override
    public void create(String data) {
        // Save the data to the database
        // Example using Spring Data JPA
        dataEntityRepository.save(new DataEntity(data));
    }

    @Override
    public String read(int id) {
        // Fetch data from the database
        // Example using Spring Data JPA
        DataEntity dataEntity = dataEntityRepository.findById(id).orElse(null);
        return dataEntity != null ? dataEntity.getData() : null;
    }

    @Override
    public void update(int id, String data) {
        // Update the data in the database
        // Example using Spring Data JPA
        DataEntity dataEntity = dataEntityRepository.findById(id).orElse(null);
        if (dataEntity != null) {
            dataEntity.setData(data);
            dataEntityRepository.save(dataEntity);
        }
    }

    @Override
    public void delete(int id) {
        // Delete data from the database
        // Example using Spring Data JPA
        dataEntityRepository.deleteById(id);
    }
}

// Proxy Class
class DatabaseProxy implements DatabaseOperations {

    private final DatabaseManager databaseManager;

    public DatabaseProxy(DatabaseManager databaseManager) {
        this.databaseManager = databaseManager;
    }

    @Override
    public void create(String data) {
        // Add additional logic here before delegating to the real subject
        log("Creating data: " + data);
        // Validate data if required
        databaseManager.create(data);
    }

    @Override
    public String read(int id) {
        // Add additional logic here before delegating to the real subject
        log("Reading data for id: " + id);
        return databaseManager.read(id);
    }

    @Override
    public void update(int id, String data) {
        // Add additional logic here before delegating to the real subject
        log("Updating data for id: " + id + " with data: " + data);
        databaseManager.update(id, data);
    }

    @Override
    public void delete(int id) {
        // Add additional logic here before delegating to the real subject
        log("Deleting data for id: " + id);
        databaseManager.delete(id);
    }

    private void log(String message) {
        // Log the operation for monitoring or debugging purposes
        System.out.println(message);
    }
}

// Controller Class
@org.springframework.web.bind.annotation.RestController
class DataController {

    // Inject the DatabaseOperations interface here
    // This will automatically inject the DatabaseProxy instance
    @org.springframework.beans.factory.annotation.Autowired
    private DatabaseOperations databaseOperations;

    @org.springframework.web.bind.annotation.PostMapping("/create")
    public void create(@org.springframework.web.bind.annotation.RequestBody String data) {
        databaseOperations.create(data);
    }

    @org.springframework.web.bind.annotation.GetMapping("/read/{id}")
    public String read(@org.springframework.web.bind.annotation.PathVariable int id) {
        return databaseOperations.read(id);
    }

    @org.springframework.web.bind.annotation.PutMapping("/update/{id}")
    public void update(@org.springframework.web.bind.annotation.PathVariable int id, @org.springframework.web.bind.annotation.RequestBody String data) {
        databaseOperations.update(id, data);
    }

    @org.springframework.web.bind.annotation.DeleteMapping("/delete/{id}")
    public void delete(@org.springframework.web.bind.annotation.PathVariable int id) {
        databaseOperations.delete(id);
    }
}

// Data Entity Class (Example for Spring Data JPA)
@org.springframework.data.jpa.repository.Entity
class DataEntity {
    @org.springframework.data.annotation.Id
    @org.springframework.data.annotation.GeneratedValue(strategy = org.springframework.data.annotation.GenerationType.IDENTITY)
    private int id;
    private String data;

    // Constructors, getters, and setters
    public DataEntity() {}
    public DataEntity(String data) {
        this.data = data;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }
}

// Data Entity Repository (Example for Spring Data JPA)
@org.springframework.data.jpa.repository.JpaRepository<DataEntity, Integer>
interface DataEntityRepository {}