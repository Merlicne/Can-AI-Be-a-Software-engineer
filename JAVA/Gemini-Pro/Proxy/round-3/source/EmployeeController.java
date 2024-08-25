package com.example.demo.controller;

import com.example.demo.model.Employee;
import com.example.demo.proxy.DatabaseOperations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    private final DatabaseOperations databaseOperations;

    public EmployeeController(DatabaseOperations databaseOperations) {
        this.databaseOperations = databaseOperations;
    }

    @PostMapping("/create")
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {
        Employee createdEmployee = databaseOperations.create(employee);
        return new ResponseEntity<>(createdEmployee, HttpStatus.CREATED);
    }

    @GetMapping("/read")
    public ResponseEntity<List<Employee>> readAllEmployees() {
        List<Employee> employees = databaseOperations.readAll();
        return new ResponseEntity<>(employees, HttpStatus.OK);
    }

    @GetMapping("/read/{id}")
    public ResponseEntity<Employee> readEmployeeById(@PathVariable Long id) {
        Employee employee = databaseOperations.readById(id);
        return new ResponseEntity<>(employee, HttpStatus.OK);
    }

    @PutMapping("/update/{id}")
    public ResponseEntity<Employee> updateEmployee(@PathVariable Long id, @RequestBody Employee employee) {
        Employee updatedEmployee = databaseOperations.update(id, employee);
        return new ResponseEntity<>(updatedEmployee, HttpStatus.OK);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        databaseOperations.delete(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}