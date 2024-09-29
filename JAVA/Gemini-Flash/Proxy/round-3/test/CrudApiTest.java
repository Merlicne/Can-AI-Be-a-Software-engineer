import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(DataController.class)
class CrudApiTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private DatabaseManager databaseManager;

    @MockBean
    private DatabaseProxy databaseProxy;

    @BeforeEach
    void setUp() {
        // Mock the DatabaseProxy to delegate to DatabaseManager
        Mockito.when(databaseProxy.create(any())).thenCallRealMethod();
        Mockito.when(databaseProxy.read(anyInt())).thenCallRealMethod();
        Mockito.when(databaseProxy.update(anyInt(), any())).thenCallRealMethod();
        Mockito.when(databaseProxy.delete(anyInt())).thenCallRealMethod();
    }

    @Test
    void testCreate() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.post("/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"data\":\"Test Data\"}"))
                .andExpect(status().isOk());
        verify(databaseManager).create("Test Data");
    }

    @Test
    void testReadExistingRecord() throws Exception {
        Mockito.when(databaseManager.read(1)).thenReturn("Test Data 1");
        mockMvc.perform(MockMvcRequestBuilders.get("/read/1"))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().string("Test Data 1"));
        verify(databaseManager).read(1);
    }

    @Test
    void testReadNonExistingRecord() throws Exception {
        Mockito.when(databaseManager.read(2)).thenReturn(null);
        mockMvc.perform(MockMvcRequestBuilders.get("/read/2"))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(""));
        verify(databaseManager).read(2);
    }

    @Test
    void testUpdate() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.put("/update/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"data\":\"Updated Data\"}"))
                .andExpect(status().isOk());
        verify(databaseManager).update(1, "Updated Data");
    }

    @Test
    void testDelete() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/delete/1"))
                .andExpect(status().isOk());
        verify(databaseManager).delete(1);
    }

    @Test
    void testDatabaseProxyLogging() {
        databaseProxy.create("Test Data");
        verify(databaseManager).create("Test Data");
        // Verify logging is called in the proxy
        // You may need to implement a mock logging mechanism for verification
    }

    @Test
    void testDatabaseProxyExceptionHandling() {
        // Simulate an exception in the databaseManager
        Mockito.doThrow(new RuntimeException("Database Error")).when(databaseManager).create(any());

        // Verify that the proxy handles the exception appropriately
        // You may need to add exception handling logic in the proxy and test accordingly
        // Example: Implement a try-catch block in the proxy and test if an appropriate response is returned
    }
}