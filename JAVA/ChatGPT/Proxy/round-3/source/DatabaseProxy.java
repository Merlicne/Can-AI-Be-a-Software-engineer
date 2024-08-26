package com.example.demo.proxy;

import com.example.demo.entity.Record;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.logging.Logger;

@Component
public class DatabaseProxy implements DatabaseOperations {

    private static final Logger logger = Logger.getLogger(DatabaseProxy.class.getName());

    @Autowired
    private DatabaseManager databaseManager;

    @Override
    public Record create(Record record) {
        logger.info("Creating record: " + record.toString());
        return databaseManager.create(record);
    }

    @Override
    public List<Record> readAll() {
        logger.info("Reading all records.");
        return databaseManager.readAll();
    }

    @Override
    public Record readById(Long id) {
        logger.info("Reading record with ID: " + id);
        return databaseManager.readById(id);
    }

    @Override
    public Record update(Long id, Record updatedRecord) {
        logger.info("Updating record with ID: " + id);
        return databaseManager.update(id, updatedRecord);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting record with ID: " + id);
        databaseManager.delete(id);
    }
}
