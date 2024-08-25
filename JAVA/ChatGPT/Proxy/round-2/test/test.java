package com.example.demo;

import com.example.demo.controller.ItemController;
import com.example.demo.model.Item;
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
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class CrudApiTests {

    @Autowired
    private MockMvc mockMvc;

    @Mock
    private DatabaseManager databaseManager;

    @InjectMocks
    private DatabaseProxy databaseProxy;

    @InjectMocks
    private ItemController itemController;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCreateItem() throws Exception {
        Item item = new Item(1L, "Item 1", "Description 1");

        when(databaseManager.create(any(Item.class))).thenReturn(item);

        mockMvc.perform(MockMvcRequestBuilders.post("/items/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Item 1\",\"description\":\"Description 1\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Item 1"))
                .andExpect(jsonPath("$.description").value("Description 1"));

        verify(databaseManager, times(1)).create(any(Item.class));
    }

    @Test
    public void testReadItemsWhenDatabaseIsEmpty() throws Exception {
        when(databaseManager.readAll()).thenReturn(Collections.emptyList());

        mockMvc.perform(MockMvcRequestBuilders.get("/items/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isEmpty());

        verify(databaseManager, times(1)).readAll();
    }

    @Test
    public void testReadItemsWhenDatabaseHasRecords() throws Exception {
        Item item1 = new Item(1L, "Item 1", "Description 1");
        Item item2 = new Item(2L, "Item 2", "Description 2");

        when(databaseManager.readAll()).thenReturn(Arrays.asList(item1, item2));

        mockMvc.perform(MockMvcRequestBuilders.get("/items/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].name").value("Item 1"))
                .andExpect(jsonPath("$[0].description").value("Description 1"))
                .andExpect(jsonPath("$[1].id").value(2L))
                .andExpect(jsonPath("$[1].name").value("Item 2"))
                .andExpect(jsonPath("$[1].description").value("Description 2"));

        verify(databaseManager, times(1)).readAll();
    }

    @Test
    public void testReadItemById() throws Exception {
        Item item = new Item(1L, "Item 1", "Description 1");

        when(databaseManager.readById(1L)).thenReturn(item);

        mockMvc.perform(MockMvcRequestBuilders.get("/items/read/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Item 1"))
                .andExpect(jsonPath("$.description").value("Description 1"));

        verify(databaseManager, times(1)).readById(1L);
    }

    @Test
    public void testUpdateItem() throws Exception {
        Item updatedItem = new Item(1L, "Updated Item", "Updated Description");

        when(databaseManager.update(eq(1L), any(Item.class))).thenReturn(updatedItem);

        mockMvc.perform(MockMvcRequestBuilders.put("/items/update/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Updated Item\",\"description\":\"Updated Description\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Updated Item"))
                .andExpect(jsonPath("$.description").value("Updated Description"));

        verify(databaseManager, times(1)).update(eq(1L), any(Item.class));
    }

    @Test
    public void testDeleteItem() throws Exception {
        doNothing().when(databaseManager).delete(1L);

        mockMvc.perform(MockMvcRequestBuilders.delete("/items/delete/1"))
                .andExpect(status().isOk());

        verify(databaseManager, times(1)).delete(1L);
    }

    @Test
    public void testDatabaseProxyCreateItem() {
        Item item = new Item(1L, "Item 1", "Description 1");

        when(databaseManager.create(any(Item.class))).thenReturn(item);

        Item result = databaseProxy.create(item);

        verify(databaseManager, times(1)).create(item);
    }

    @Test
    public void testDatabaseProxyReadAll() {
        when(databaseManager.readAll()).thenReturn(Collections.emptyList());

        databaseProxy.readAll();

        verify(databaseManager, times(1)).readAll();
    }

    @Test
    public void testDatabaseProxyReadById() {
        Item item = new Item(1L, "Item 1", "Description 1");

        when(databaseManager.readById(1L)).thenReturn(item);

        databaseProxy.readById(1L);

        verify(databaseManager, times(1)).readById(1L);
    }

    @Test
    public void testDatabaseProxyUpdate() {
        Item updatedItem = new Item(1L, "Updated Item", "Updated Description");

        when(databaseManager.update(eq(1L), any(Item.class))).thenReturn(updatedItem);

        databaseProxy.update(1L, updatedItem);

        verify(databaseManager, times(1)).update(eq(1L), any(Item.class));
    }

    @Test
    public void testDatabaseProxyDelete() {
        doNothing().when(databaseManager).delete(1L);

        databaseProxy.delete(1L);

        verify(databaseManager, times(1)).delete(1L);
    }

    @Test
    public void testReadItemByIdWhenNotFound() throws Exception {
        when(databaseManager.readById(1L)).thenReturn(null);

        mockMvc.perform(MockMvcRequestBuilders.get("/items/read/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").doesNotExist());

        verify(databaseManager, times(1)).readById(1L);
    }
}
