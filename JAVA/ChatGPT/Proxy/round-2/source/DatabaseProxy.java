package com.example.demo.proxy;

import com.example.demo.model.Item;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DatabaseProxy implements DatabaseOperations<Item> {

    private static final Logger logger = LoggerFactory.getLogger(DatabaseProxy.class);

    @Autowired
    private DatabaseManager databaseManager;

    @Override
    public Item create(Item entity) {
        logger.info("Creating an item: {}", entity);
        return databaseManager.create(entity);
    }

    @Override
    public List<Item> readAll() {
        logger.info("Reading all items");
        return databaseManager.readAll();
    }

    @Override
    public Item readById(Long id) {
        logger.info("Reading item with id: {}", id);
        return databaseManager.readById(id);
    }

    @Override
    public Item update(Long id, Item entity) {
        logger.info("Updating item with id: {}", id);
        return databaseManager.update(id, entity);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting item with id: {}", id);
        databaseManager.delete(id);
    }
}
