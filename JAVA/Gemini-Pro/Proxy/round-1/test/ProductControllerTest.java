package com.example.demo;

import com.example.demo.controller.ProductController;
import com.example.demo.model.Product;
import com.example.demo.proxy.DatabaseProxy;
import com.example.demo.repository.ProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ProductController.class)
public class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private DatabaseProxy databaseProxy;

    @MockBean
    private ProductRepository productRepository; // You might not need this if not directly used

    private Product testProduct;

    @BeforeEach
    void setUp() {
        testProduct = new Product();
        testProduct.setId(1L);
        testProduct.setName("Test Product");
        testProduct.setPrice(10.0);
    }

    // Test: Creating a new product (POST /create)
    @Test
    void testCreateProduct() throws Exception {
        when(databaseProxy.create(any(Product.class))).thenReturn(testProduct);

        mockMvc.perform(MockMvcRequestBuilders.post("/api/products/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Test Product\",\"price\":10.0}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Test Product")))
                .andExpect(jsonPath("$.price", is(10.0)));

        verify(databaseProxy, times(1)).create(any(Product.class));
    }

    // Test: Reading a product by ID (GET /read/{id})
    @Test
    void testGetProductById_Found() throws Exception {
        when(databaseProxy.read(1L)).thenReturn(Optional.of(testProduct));

        mockMvc.perform(MockMvcRequestBuilders.get("/api/products/read/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Test Product")))
                .andExpect(jsonPath("$.price", is(10.0)));

        verify(databaseProxy, times(1)).read(1L);
    }

    // Test: Reading a product by ID - Not Found (GET /read/{id})
    @Test
    void testGetProductById_NotFound() throws Exception {
        when(databaseProxy.read(2L)).thenReturn(Optional.empty());

        mockMvc.perform(MockMvcRequestBuilders.get("/api/products/read/2"))
                .andExpect(status().isNotFound());

        verify(databaseProxy, times(1)).read(2L);
    }

    // Test: Reading all products (GET /read)
    @Test
    void testGetAllProducts() throws Exception {
        List<Product> productList = Collections.singletonList(testProduct);
        when(databaseProxy.readAll()).thenReturn(productList);

        mockMvc.perform(MockMvcRequestBuilders.get("/api/products/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].id", is(1)))
                .andExpect(jsonPath("$[0].name", is("Test Product")))
                .andExpect(jsonPath("$[0].price", is(10.0)));

        verify(databaseProxy, times(1)).readAll();
    }

    // Test: Updating a product (PUT /update/{id})
    @Test
    void testUpdateProduct() throws Exception {
        when(databaseProxy.read(1L)).thenReturn(Optional.of(testProduct));
        when(databaseProxy.update(any(Product.class))).thenReturn(testProduct);

        mockMvc.perform(MockMvcRequestBuilders.put("/api/products/update/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Updated Product\",\"price\":12.5}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Updated Product")))
                .andExpect(jsonPath("$.price", is(12.5)));

        verify(databaseProxy, times(1)).read(1L);
        verify(databaseProxy, times(1)).update(any(Product.class));
    }

    // Test: Updating a product - Not Found (PUT /update/{id})
    @Test
    void testUpdateProduct_NotFound() throws Exception {
        when(databaseProxy.read(2L)).thenReturn(Optional.empty());

        mockMvc.perform(MockMvcRequestBuilders.put("/api/products/update/2")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Updated Product\",\"price\":12.5}"))
                .andExpect(status().isNotFound());

        verify(databaseProxy, times(1)).read(2L);
        verify(databaseProxy, never()).update(any(Product.class));
    }

    // Test: Deleting a product (DELETE /delete/{id})
    @Test
    void testDeleteProduct() throws Exception {
        doNothing().when(databaseProxy).delete(1L);

        mockMvc.perform(MockMvcRequestBuilders.delete("/api/products/delete/1"))
                .andExpect(status().isNoContent());

        verify(databaseProxy, times(1)).delete(1L);
    }

    // Additional Tests for DatabaseProxy (You might need to refactor for better testability)
    @Test
    void testDatabaseProxy_Create() {
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);
        Product created = databaseProxy.create(testProduct);
        assert (created.equals(testProduct));
        verify(productRepository, times(1)).save(any(Product.class));
    }

    // ... Similarly add tests for DatabaseProxy's read, readAll, update, delete methods

}