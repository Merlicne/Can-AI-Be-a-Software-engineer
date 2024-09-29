import org.junit.jupiter.api.AfterEach;
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
    private ItemRepository itemRepository;

    @Autowired
    private DatabaseProxy databaseProxy;

    @BeforeEach
    public void setUp() {
        itemRepository.deleteAll();
    }

    @AfterEach
    public void tearDown() {
        itemRepository.deleteAll();
    }

    @Test
    public void testCreate() throws Exception {
        Item newItem = new Item("Item 1", "Description 1");
        mockMvc.perform(MockMvcRequestBuilders.post("/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(JsonUtil.toJson(newItem)))
                .andExpect(status().isCreated());

        // Verify that the record is added to the database
        Item createdItem = itemRepository.findAll().get(0);
        assert createdItem.getName().equals("Item 1");
        assert createdItem.getDescription().equals("Description 1");
    }

    @Test
    public void testReadEmptyDatabase() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/read/1"))
                .andExpect(status().isNotFound());
    }

    @Test
    public void testReadExistingRecord() throws Exception {
        Item newItem = new Item("Item 2", "Description 2");
        itemRepository.save(newItem);

        mockMvc.perform(MockMvcRequestBuilders.get("/read/" + newItem.getId()))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().json(JsonUtil.toJson(newItem)));
    }

    @Test
    public void testUpdateExistingRecord() throws Exception {
        Item newItem = new Item("Item 3", "Description 3");
        itemRepository.save(newItem);

        Item updatedItem = new Item(newItem.getId(), "Updated Item 3", "Updated Description 3");
        mockMvc.perform(MockMvcRequestBuilders.put("/update/" + newItem.getId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(JsonUtil.toJson(updatedItem)))
                .andExpect(status().isOk());

        // Verify the update in the database
        Item updatedRecord = itemRepository.findById(newItem.getId()).get();
        assert updatedRecord.getName().equals("Updated Item 3");
        assert updatedRecord.getDescription().equals("Updated Description 3");
    }

    @Test
    public void testUpdateNonExistingRecord() throws Exception {
        Item newItem = new Item(100L, "Item 4", "Description 4"); // Non-existing ID
        mockMvc.perform(MockMvcRequestBuilders.put("/update/100")
                .contentType(MediaType.APPLICATION_JSON)
                .content(JsonUtil.toJson(newItem)))
                .andExpect(status().isBadRequest());
    }

    @Test
    public void testDeleteExistingRecord() throws Exception {
        Item newItem = new Item("Item 5", "Description 5");
        itemRepository.save(newItem);

        mockMvc.perform(MockMvcRequestBuilders.delete("/delete/" + newItem.getId()))
                .andExpect(status().isNoContent());

        // Verify the deletion from the database
        assert itemRepository.findById(newItem.getId()).isEmpty();
    }

    @Test
    public void testDeleteNonExistingRecord() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/delete/100"))
                .andExpect(status().isNoContent()); // No error for deleting non-existing records
    }

    @Test
    public void testDatabaseProxyCreate() {
        Item item = new Item("Test Proxy Create", "Test Description");
        Item createdItem = databaseProxy.create(item);
        assert createdItem.getId() != null;
    }

    @Test
    public void testDatabaseProxyRead() {
        Item item = new Item("Test Proxy Read", "Test Description");
        itemRepository.save(item);
        Item readItem = databaseProxy.read(item.getId());
        assert readItem.getId().equals(item.getId());
    }

    @Test
    public void testDatabaseProxyUpdate() {
        Item item = new Item("Test Proxy Update", "Test Description");
        itemRepository.save(item);
        item.setName("Updated Test");
        Item updatedItem = databaseProxy.update(item);
        assert updatedItem.getName().equals("Updated Test");
    }

    @Test
    public void testDatabaseProxyDelete() {
        Item item = new Item("Test Proxy Delete", "Test Description");
        itemRepository.save(item);
        databaseProxy.delete(item.getId());
        assert itemRepository.findById(item.getId()).isEmpty();
    }
}