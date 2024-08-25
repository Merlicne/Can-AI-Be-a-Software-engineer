package com.example.demo.proxy;

import com.example.demo.model.Employee;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import java.util.List;

@Component
public class DatabaseProxy implements DatabaseOperations {

    private static final Logger logger = LoggerFactory.getLogger(DatabaseProxy.class);
    private final DatabaseManager databaseManager;

    public DatabaseProxy(DatabaseManager databaseManager) {
        this.databaseManager = databaseManager;
    }

    @Override
    public Employee create(Employee employee) {
        logger.info("Creating new employee: {}", employee);
        return databaseManager.create(employee);
    }

    @Override
    public List<Employee> readAll() {
        logger.info("Fetching all employees.");
        return databaseManager.readAll();
    }

    @Override
    public Employee readById(Long id) {
        logger.info("Fetching employee with id: {}", id);
        return databaseManager.readById(id);
    }

    @Override
    public Employee update(Long id, Employee employee) {
        logger.info("Updating employee with id: {}", id);
        return databaseManager.update(id, employee);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting employee with id: {}", id);
        databaseManager.delete(id);
    }
}