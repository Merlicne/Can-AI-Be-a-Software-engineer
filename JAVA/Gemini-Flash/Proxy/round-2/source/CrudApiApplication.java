import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;

@SpringBootApplication
public class CrudApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(CrudApiApplication.class, args);
    }
}

// Database Operations Interface
interface DatabaseOperations<T> {
    T create(T entity);
    T read(Long id);
    List<T> readAll();
    T update(T entity);
    void delete(Long id);
}

// Real Subject Class: DatabaseManager
@Repository
class DatabaseManager implements DatabaseOperations<User> {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public User create(User user) {
        entityManager.persist(user);
        return user;
    }

    @Override
    public User read(Long id) {
        return entityManager.find(User.class, id);
    }

    @Override
    public List<User> readAll() {
        return entityManager.createQuery("SELECT u FROM User u", User.class).getResultList();
    }

    @Override
    public User update(User user) {
        return entityManager.merge(user);
    }

    @Override
    public void delete(Long id) {
        User user = entityManager.find(User.class, id);
        if (user != null) {
            entityManager.remove(user);
        }
    }
}

// Proxy Class: DatabaseProxy
class DatabaseProxy implements DatabaseOperations<User> {

    @Autowired
    private DatabaseManager databaseManager;

    @Override
    public User create(User user) {
        // Add proxy logic here (e.g., logging, validation)
        System.out.println("Creating user: " + user.getName());
        return databaseManager.create(user);
    }

    @Override
    public User read(Long id) {
        // Add proxy logic here (e.g., caching)
        System.out.println("Reading user with ID: " + id);
        return databaseManager.read(id);
    }

    @Override
    public List<User> readAll() {
        // Add proxy logic here
        System.out.println("Reading all users");
        return databaseManager.readAll();
    }

    @Override
    public User update(User user) {
        // Add proxy logic here
        System.out.println("Updating user: " + user.getName());
        return databaseManager.update(user);
    }

    @Override
    public void delete(Long id) {
        // Add proxy logic here
        System.out.println("Deleting user with ID: " + id);
        databaseManager.delete(id);
    }
}

// User Entity
@Entity
class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    // Getters and setters

    public User(String name) {
        this.name = name;
    }
}

// API Controller
@RestController
@RequestMapping("/users")
class UserController {

    @Autowired
    private DatabaseProxy databaseProxy;

    @PostMapping("/create")
    public User createUser(@RequestBody User user) {
        return databaseProxy.create(user);
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return databaseProxy.read(id);
    }

    @GetMapping
    public List<User> getAllUsers() {
        return databaseProxy.readAll();
    }

    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        user.setId(id);
        return databaseProxy.update(user);
    }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        databaseProxy.delete(id);
    }
}