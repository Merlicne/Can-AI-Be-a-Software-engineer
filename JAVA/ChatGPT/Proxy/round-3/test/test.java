package com.example.demo;

import com.example.demo.controller.RecordController;
import com.example.demo.entity.Record;
import com.example.demo.proxy.DatabaseManager;
import com.example.demo.proxy.DatabaseProxy;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class RecordControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private DatabaseProxy databaseProxy;

    private Record record1;
    private Record record2;

    @BeforeEach
    void setUp() {
        record1 = new Record(1L, "Test Record 1", "123");
        record2 = new Record(2L, "Test Record 2", "456");
    }

    @Test
    void testCreateRecord() throws Exception {
        when(databaseProxy.create(any(Record.class))).thenReturn(record1);

        mockMvc.perform(post("/api/records/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\": \"Test Record 1\", \"value\": \"123\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Test Record 1"))
                .andExpect(jsonPath("$.value").value("123"));

        verify(databaseProxy, times(1)).create(any(Record.class));
    }

    @Test
    void testReadAllRecords_emptyDatabase() throws Exception {
        when(databaseProxy.readAll()).thenReturn(Arrays.asList());

        mockMvc.perform(get("/api/records/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isEmpty());

        verify(databaseProxy, times(1)).readAll();
    }

    @Test
    void testReadAllRecords_withRecords() throws Exception {
        when(databaseProxy.readAll()).thenReturn(Arrays.asList(record1, record2));

        mockMvc.perform(get("/api/records/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].name").value("Test Record 1"))
                .andExpect(jsonPath("$[0].value").value("123"))
                .andExpect(jsonPath("$[1].id").value(2L))
                .andExpect(jsonPath("$[1].name").value("Test Record 2"))
                .andExpect(jsonPath("$[1].value").value("456"));

        verify(databaseProxy, times(1)).readAll();
    }

    @Test
    void testReadRecordById_existingRecord() throws Exception {
        when(databaseProxy.readById(1L)).thenReturn(record1);

        mockMvc.perform(get("/api/records/read/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Test Record 1"))
                .andExpect(jsonPath("$.value").value("123"));

        verify(databaseProxy, times(1)).readById(1L);
    }

    @Test
    void testReadRecordById_nonExistingRecord() throws Exception {
        when(databaseProxy.readById(99L)).thenReturn(null);

        mockMvc.perform(get("/api/records/read/99"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").doesNotExist());

        verify(databaseProxy, times(1)).readById(99L);
    }

    @Test
    void testUpdateRecord_existingRecord() throws Exception {
        Record updatedRecord = new Record(1L, "Updated Record 1", "789");
        when(databaseProxy.update(eq(1L), any(Record.class))).thenReturn(updatedRecord);

        mockMvc.perform(put("/api/records/update/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\": \"Updated Record 1\", \"value\": \"789\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Updated Record 1"))
                .andExpect(jsonPath("$.value").value("789"));

        verify(databaseProxy, times(1)).update(eq(1L), any(Record.class));
    }

    @Test
    void testUpdateRecord_nonExistingRecord() throws Exception {
        when(databaseProxy.update(eq(99L), any(Record.class))).thenReturn(null);

        mockMvc.perform(put("/api/records/update/99")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\": \"Non Existing Record\", \"value\": \"000\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").doesNotExist());

        verify(databaseProxy, times(1)).update(eq(99L), any(Record.class));
    }

    @Test
    void testDeleteRecord_existingRecord() throws Exception {
        doNothing().when(databaseProxy).delete(1L);

        mockMvc.perform(delete("/api/records/delete/1"))
                .andExpect(status().isOk());

        verify(databaseProxy, times(1)).delete(1L);
    }

    @Test
    void testDeleteRecord_nonExistingRecord() throws Exception {
        doNothing().when(databaseProxy).delete(99L);

        mockMvc.perform(delete("/api/records/delete/99"))
                .andExpect(status().isOk());

        verify(databaseProxy, times(1)).delete(99L);
    }

    @Test
    void testDatabaseProxy_create() {
        DatabaseManager databaseManager = mock(DatabaseManager.class);
        DatabaseProxy databaseProxy = new DatabaseProxy();
        databaseProxy.databaseManager = databaseManager;

        when(databaseManager.create(any(Record.class))).thenReturn(record1);
        Record result = databaseProxy.create(record1);

        verify(databaseManager, times(1)).create(any(Record.class));
        assert result != null;
        assert result.getId().equals(1L);
        assert result.getName().equals("Test Record 1");
    }

    @Test
    void testDatabaseProxy_readAll() {
        DatabaseManager databaseManager = mock(DatabaseManager.class);
        DatabaseProxy databaseProxy = new DatabaseProxy();
        databaseProxy.databaseManager = databaseManager;

        when(databaseManager.readAll()).thenReturn(Arrays.asList(record1, record2));
        List<Record> results = databaseProxy.readAll();

        verify(databaseManager, times(1)).readAll();
        assert results.size() == 2;
    }

    @Test
    void testDatabaseProxy_update() {
        DatabaseManager databaseManager = mock(DatabaseManager.class);
        DatabaseProxy databaseProxy = new DatabaseProxy();
        databaseProxy.databaseManager = databaseManager;

        when(databaseManager.update(eq(1L), any(Record.class))).thenReturn(record1);
        Record result = databaseProxy.update(1L, record1);

        verify(databaseManager, times(1)).update(eq(1L), any(Record.class));
        assert result != null;
        assert result.getId().equals(1L);
    }

    @Test
    void testDatabaseProxy_delete() {
        DatabaseManager databaseManager = mock(DatabaseManager.class);
        DatabaseProxy databaseProxy = new DatabaseProxy();
        databaseProxy.databaseManager = databaseManager;

        doNothing().when(databaseManager).delete(1L);
        databaseProxy.delete(1L);

        verify(databaseManager, times(1)).delete(1L);
    }
}
