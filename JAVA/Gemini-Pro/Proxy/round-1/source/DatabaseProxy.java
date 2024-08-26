package com.example.demo.proxy;

import com.example.demo.model.Product;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
public class DatabaseProxy implements DatabaseOperations<Product> {

    @Autowired
    private DatabaseManager databaseManager;

    private static final Logger logger = LoggerFactory.getLogger(DatabaseProxy.class);

    @Override
    public Product create(Product product) {
        logger.info("Creating new product: {}", product.getName());
        return databaseManager.create(product);
    }

    @Override
    public Optional<Product> read(Long id) {
        logger.info("Reading product with ID: {}", id);
        return databaseManager.read(id);
    }

    @Override
    public List<Product> readAll() {
        logger.info("Reading all products.");
        return databaseManager.readAll();
    }

    @Override
    public Product update(Product product) {
        logger.info("Updating product with ID: {}", product.getId());
        return databaseManager.update(product);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting product with ID: {}", id);
        databaseManager.delete(id);
    }
}