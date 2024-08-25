package com.example.crudapi.controller;

import com.example.crudapi.model.Product;
import com.example.crudapi.service.DatabaseProxy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class ProductController {

    @Autowired
    private DatabaseProxy databaseProxy;

    @PostMapping("/create")
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        Product createdProduct = databaseProxy.create(product);
        return new ResponseEntity<>(createdProduct, HttpStatus.CREATED);
    }

    @GetMapping("/read/{id}")
    public ResponseEntity<Product> readProduct(@PathVariable Long id) {
        Product product = databaseProxy.read(id);
        return product != null ? new ResponseEntity<>(product, HttpStatus.OK)
                : new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    @GetMapping("/read")
    public ResponseEntity<List<Product>> readAllProducts() {
        List<Product> products = databaseProxy.readAll();
        return new ResponseEntity<>(products, HttpStatus.OK);
    }

    @PutMapping("/update/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product updatedProduct) {
        Product existingProduct = databaseProxy.read(id);
        if (existingProduct != null) {
            updatedProduct.setId(id);
            return new ResponseEntity<>(databaseProxy.update(updatedProduct), HttpStatus.OK);
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        databaseProxy.delete(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}