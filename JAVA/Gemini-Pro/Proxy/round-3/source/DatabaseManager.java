package com.example.demo.proxy;

import com.example.demo.model.Employee;
import com.example.demo.repository.EmployeeRepository;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
public class DatabaseManager implements DatabaseOperations {

    private final EmployeeRepository repository;

    public DatabaseManager(EmployeeRepository repository) {
        this.repository = repository;
    }

    @Override
    public Employee create(Employee employee) {
        return repository.save(employee);
    }

    @Override
    public List<Employee> readAll() {
        return repository.findAll();
    }

    @Override
    public Employee readById(Long id) {
        Optional<Employee> employee = repository.findById(id);
        return employee.orElse(null);
    }

    @Override
    public Employee update(Long id, Employee employee) {
        Optional<Employee> existingEmployee = repository.findById(id);
        if (existingEmployee.isPresent()) {
            employee.setId(id);
            return repository.save(employee);
        }
        return null;
    }

    @Override
    public void delete(Long id) {
        repository.deleteById(id);
    }
}