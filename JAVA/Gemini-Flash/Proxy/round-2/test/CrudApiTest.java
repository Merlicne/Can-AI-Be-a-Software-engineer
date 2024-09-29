import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
public class CrudApiTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private DatabaseProxy databaseProxy;

    @Autowired
    private DatabaseManager databaseManager;

    @BeforeEach
    void setUp() {
        // Clear the database before each test
        databaseManager.readAll().forEach(user -> databaseManager.delete(user.getId()));
    }

    @Test
    void testCreateUser() throws Exception {
        // Create a new user
        String requestBody = "{\"name\": \"John Doe\"}";
        mockMvc.perform(MockMvcRequestBuilders.post("/users/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestBody))
                .andExpect(status().isOk());

        // Verify the user is created in the database
        User createdUser = databaseManager.readAll().get(0);
        assert createdUser.getName().equals("John Doe");
    }

    @Test
    void testGetUser() throws Exception {
        // Create a user
        User user = databaseManager.create(new User("Jane Doe"));

        // Get the user by ID
        mockMvc.perform(MockMvcRequestBuilders.get("/users/" + user.getId()))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Jane Doe"));
    }

    @Test
    void testGetUserNotFound() throws Exception {
        // Try to get a user that doesn't exist
        mockMvc.perform(MockMvcRequestBuilders.get("/users/100"))
                .andExpect(status().isNotFound());
    }

    @Test
    void testGetAllUsers() throws Exception {
        // Create a few users
        databaseManager.create(new User("Alice"));
        databaseManager.create(new User("Bob"));

        // Get all users
        mockMvc.perform(MockMvcRequestBuilders.get("/users"))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].name").value("Alice"))
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].name").value("Bob"));
    }

    @Test
    void testUpdateUser() throws Exception {
        // Create a user
        User user = databaseManager.create(new User("John Doe"));

        // Update the user's name
        String requestBody = "{\"name\": \"John Smith\"}";
        mockMvc.perform(MockMvcRequestBuilders.put("/users/" + user.getId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestBody))
                .andExpect(status().isOk());

        // Verify the update in the database
        User updatedUser = databaseManager.read(user.getId());
        assert updatedUser.getName().equals("John Smith");
    }

    @Test
    void testDeleteUser() throws Exception {
        // Create a user
        User user = databaseManager.create(new User("Jane Doe"));

        // Delete the user
        mockMvc.perform(MockMvcRequestBuilders.delete("/users/" + user.getId()))
                .andExpect(status().isOk());

        // Verify the user is deleted from the database
        assert databaseManager.read(user.getId()) == null;
    }

    @Test
    void testDatabaseProxyLogging() {
        // Test the proxy logging by creating a user
        User user = databaseProxy.create(new User("Test User"));
        // No specific assertion here, as we are just checking the log output
        // You can use a logging framework and assert the log messages
    }

    @Test
    void testDatabaseProxyDelegation() {
        // Create a user through the proxy
        User user = databaseProxy.create(new User("Proxy Test User"));

        // Verify the user is created in the database through the DatabaseManager
        User createdUser = databaseManager.read(user.getId());
        assert createdUser.getName().equals("Proxy Test User");
    }
}