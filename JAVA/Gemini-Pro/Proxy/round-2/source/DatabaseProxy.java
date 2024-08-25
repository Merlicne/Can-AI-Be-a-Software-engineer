package com.example.crudapi.service;

import com.example.crudapi.model.Product;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

// Proxy Class - Intercepts and controls access to DatabaseManager
@Component
public class DatabaseProxy implements DatabaseOperations<Product, Long> {

    @Autowired
    private DatabaseManager databaseManager;

    private static final Logger logger = LoggerFactory.getLogger(DatabaseProxy.class);

    @Override
    public Product create(Product product) {
        logger.info("Creating product: " + product.getName());
        return databaseManager.create(product);
    }

    @Override
    public Product read(Long id) {
        logger.info("Reading product with id: " + id);
        return databaseManager.read(id);
    }

    @Override
    public List<Product> readAll() {
        logger.info("Reading all products");
        return databaseManager.readAll();
    }

    @Override
    public Product update(Product product) {
        logger.info("Updating product with id: " + product.getId());
        return databaseManager.update(product);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting product with id: " + id);
        databaseManager.delete(id);
    }
}