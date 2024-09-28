import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ExtendWith(MockitoExtension.class)
public class EntityControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Mock
    private DatabaseManager<Entity> databaseManager;

    @InjectMocks
    private DatabaseProxy<Entity> databaseProxy;

    private Entity testEntity;

    @BeforeEach
    public void setUp() {
        testEntity = new Entity();
        testEntity.setId(1L);
        testEntity.setName("Test Entity");
    }

    @Test
    public void testCreateEntity() throws Exception {
        when(databaseManager.create(any(Entity.class))).thenReturn(testEntity);

        mockMvc.perform(MockMvcRequestBuilders
                .post("/api/v1/entities/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Test Entity\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Entity"));

        verify(databaseManager, times(1)).create(any(Entity.class));
    }

    @Test
    public void testReadEntity() throws Exception {
        when(databaseManager.read(1L)).thenReturn(testEntity);

        mockMvc.perform(MockMvcRequestBuilders
                .get("/api/v1/entities/read/1")
                .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Entity"));

        verify(databaseManager, times(1)).read(1L);
    }

    @Test
    public void testUpdateEntity() throws Exception {
        when(databaseManager.update(anyLong(), any(Entity.class))).thenReturn(testEntity);

        mockMvc.perform(MockMvcRequestBuilders
                .put("/api/v1/entities/update/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Updated Entity\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Updated Entity"));

        verify(databaseManager, times(1)).update(anyLong(), any(Entity.class));
    }

    @Test
    public void testDeleteEntity() throws Exception {
        doNothing().when(databaseManager).delete(1L);

        mockMvc.perform(MockMvcRequestBuilders
                .delete("/api/v1/entities/delete/1"))
                .andExpect(status().isOk());

        verify(databaseManager, times(1)).delete(1L);
    }

    @Test
    public void testProxyCreate() {
        when(databaseManager.create(testEntity)).thenReturn(testEntity);

        Entity createdEntity = databaseProxy.create(testEntity);

        assertNotNull(createdEntity);
        verify(databaseManager, times(1)).create(testEntity);
    }

    @Test
    public void testProxyRead() {
        when(databaseManager.read(1L)).thenReturn(testEntity);

        Entity retrievedEntity = databaseProxy.read(1L);

        assertNotNull(retrievedEntity);
        verify(databaseManager, times(1)).read(1L);
    }

    @Test
    public void testProxyUpdate() {
        when(databaseManager.update(1L, testEntity)).thenReturn(testEntity);

        Entity updatedEntity = databaseProxy.update(1L, testEntity);

        assertNotNull(updatedEntity);
        verify(databaseManager, times(1)).update(1L, testEntity);
    }

    @Test
    public void testProxyDelete() {
        doNothing().when(databaseManager).delete(1L);

        databaseProxy.delete(1L);

        verify(databaseManager, times(1)).delete(1L);
    }

    @Test
    public void testReadEntityNotFound() throws Exception {
        when(databaseManager.read(1L)).thenThrow(new RuntimeException("Entity not found"));

        mockMvc.perform(MockMvcRequestBuilders
                .get("/api/v1/entities/read/1")
                .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.message").value("Entity not found"));

        verify(databaseManager, times(1)).read(1L);
    }

    @Test
    public void testUpdateEntityNotFound() throws Exception {
        when(databaseManager.update(anyLong(), any(Entity.class)))
                .thenThrow(new RuntimeException("Entity not found"));

        mockMvc.perform(MockMvcRequestBuilders
                .put("/api/v1/entities/update/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Updated Entity\"}"))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.message").value("Entity not found"));

        verify(databaseManager, times(1)).update(anyLong(), any(Entity.class));
    }

    @Test
    public void testDeleteEntityNotFound() throws Exception {
        doThrow(new RuntimeException("Entity not found")).when(databaseManager).delete(1L);

        mockMvc.perform(MockMvcRequestBuilders
                .delete("/api/v1/entities/delete/1"))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.message").value("Entity not found"));

        verify(databaseManager, times(1)).delete(1L);
    }
}
