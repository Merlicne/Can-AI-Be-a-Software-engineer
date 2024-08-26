package com.example.demo.proxy;

import com.example.demo.model.Employee;
import java.util.List;

public interface DatabaseOperations {

    Employee create(Employee employee);
    List<Employee> readAll();
    Employee readById(Long id);
    Employee update(Long id, Employee employee);
    void delete(Long id);
}