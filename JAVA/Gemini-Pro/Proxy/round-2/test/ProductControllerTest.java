package com.example.crudapi.controller;

import com.example.crudapi.model.Product;
import com.example.crudapi.repository.ProductRepository;
import com.example.crudapi.service.DatabaseProxy;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private DatabaseProxy databaseProxy;

    @BeforeEach
    public void setUp() {
        productRepository.deleteAll(); // Start with a clean database before each test
    }

    @AfterEach
    public void tearDown() {
        productRepository.deleteAll(); // Clean up after each test
    }

    // Test creating a new product
    @Test
    public void testCreateProduct() throws Exception {
        String productJson = "{\"name\": \"Test Product\", \"price\": 10.0}";
        mockMvc.perform(post("/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(productJson))
                .andExpect(status().isCreated())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").exists())
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Test Product"))
                .andExpect(MockMvcResultMatchers.jsonPath("$.price").value(10.0));
    }

    // Test reading a product by ID
    @Test
    public void testReadProduct() throws Exception {
        Product product = new Product();
        product.setName("Test Product");
        product.setPrice(10.0);
        product = productRepository.save(product);

        mockMvc.perform(get("/read/" + product.getId()))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value(product.getId()))
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Test Product"))
                .andExpect(MockMvcResultMatchers.jsonPath("$.price").value(10.0));
    }


    // Test reading all products when the database is empty
    @Test
    public void testReadAllProductsEmpty() throws Exception {
        mockMvc.perform(get("/read"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$").isEmpty());
    }

    // Test updating a product
    @Test
    public void testUpdateProduct() throws Exception {
        Product product = new Product();
        product.setName("Test Product");
        product.setPrice(10.0);
        product = productRepository.save(product);

        String updatedProductJson = "{\"name\": \"Updated Product\", \"price\": 15.0}";

        mockMvc.perform(put("/update/" + product.getId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(updatedProductJson))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value(product.getId()))
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Updated Product"))
                .andExpect(MockMvcResultMatchers.jsonPath("$.price").value(15.0));
    }

    // Test deleting a product
    @Test
    public void testDeleteProduct() throws Exception {
        Product product = new Product();
        product.setName("Test Product");
        product.setPrice(10.0);
        product = productRepository.save(product);

        mockMvc.perform(delete("/delete/" + product.getId()))
                .andExpect(status().isNoContent());
        assertEquals(0, productRepository.findAll().size());

    }

    // Test reading a product that does not exist
    @Test
    public void testReadProductNotFound() throws Exception {
        mockMvc.perform(get("/read/999"))
                .andExpect(status().isNotFound());
    }

    // Test updating a product that does not exist
    @Test
    public void testUpdateProductNotFound() throws Exception {
        String updatedProductJson = "{\"name\": \"Updated Product\", \"price\": 15.0}";

        mockMvc.perform(put("/update/999")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(updatedProductJson))
                .andExpect(status().isNotFound());
    }

    // Test deleting a product that does not exist
    @Test
    public void testDeleteProductNotFound() throws Exception {
        mockMvc.perform(delete("/delete/999"))
                .andExpect(status().isNoContent()); // Still returns 204 even if the product doesn't exist
    }

    // Test DatabaseProxy methods
    @Test
    public void testDatabaseProxy() {
        Product product = new Product();
        product.setName("Proxy Test Product");
        product.setPrice(20.0);

        // Test create
        Product createdProduct = databaseProxy.create(product);
        assertEquals("Proxy Test Product", createdProduct.getName());

        // Test read
        Product readProduct = databaseProxy.read(createdProduct.getId());
        assertEquals(createdProduct.getId(), readProduct.getId());

        // Test update
        readProduct.setPrice(25.0);
        databaseProxy.update(readProduct);
        Product updatedProduct = databaseProxy.read(readProduct.getId());
        assertEquals(25.0, updatedProduct.getPrice());

        // Test delete
        databaseProxy.delete(updatedProduct.getId());
        Product deletedProduct = databaseProxy.read(updatedProduct.getId());
        assertEquals(null, deletedProduct);
    }

    // Test reading all products
    @Test
    public void testReadAllProducts() throws Exception {
        Product product1 = new Product();
        product1.setName("Product 1");
        product1.setPrice(10.0);
        productRepository.save(product1);

        Product product2 = new Product();
        product2.setName("Product 2");
        product2.setPrice(20.0);
        productRepository.save(product2);

        mockMvc.perform(get("/read"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].name", is("Product 1")))
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].name", is("Product 2")));
    }
}