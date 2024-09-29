package com.example.demo;

import com.example.demo.controller.EmployeeController;
import com.example.demo.model.Employee;
import com.example.demo.proxy.DatabaseManager;
import com.example.demo.proxy.DatabaseProxy;
import com.example.demo.repository.EmployeeRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(EmployeeController.class)
public class EmployeeApiTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private DatabaseProxy databaseProxy;

    @MockBean
    private DatabaseManager databaseManager;

    @MockBean
    private EmployeeRepository employeeRepository;

    @BeforeEach
    public void setup() {
        // Configure mock behavior for DatabaseManager
        when(databaseManager.create(any(Employee.class))).thenAnswer(i -> {
            Employee employee = i.getArgument(0);
            employee.setId(1L);
            return employee;
        });

        when(databaseManager.readAll()).thenReturn(Arrays.asList(
                new Employee(1L, "John Doe", "IT"),
                new Employee(2L, "Jane Doe", "HR")
        ));

        when(databaseManager.readById(1L)).thenReturn(new Employee(1L, "John Doe", "IT"));
        when(databaseManager.readById(2L)).thenReturn(new Employee(2L, "Jane Doe", "HR"));

        when(databaseManager.update(eq(1L), any(Employee.class))).thenAnswer(i -> {
            Employee updatedEmployee = i.getArgument(1);
            updatedEmployee.setId(1L);
            return updatedEmployee;
        });

        doNothing().when(databaseManager).delete(1L);
    }

    // --- Tests for EmployeeController ---

    @Test
    public void testCreateEmployee() throws Exception {
        String employeeJson = "{\"name\": \"Test User\", \"department\": \"Testing\"}";
        mockMvc.perform(MockMvcRequestBuilders.post("/api/employees/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(employeeJson))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Test User")))
                .andExpect(jsonPath("$.department", is("Testing")));

        verify(databaseProxy, times(1)).create(any(Employee.class));
    }

    @Test
    public void testReadAllEmployees() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/employees/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].id", is(1)))
                .andExpect(jsonPath("$[0].name", is("John Doe")))
                .andExpect(jsonPath("$[1].id", is(2)))
                .andExpect(jsonPath("$[1].name", is("Jane Doe")));

        verify(databaseProxy, times(1)).readAll();
    }

    @Test
    public void testReadEmployeeById() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/employees/read/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("John Doe")))
                .andExpect(jsonPath("$.department", is("IT")));

        verify(databaseProxy, times(1)).readById(1L);
    }

    @Test
    public void testUpdateEmployee() throws Exception {
        String updatedEmployeeJson = "{\"name\": \"Updated User\", \"department\": \"Updated Dept\"}";
        mockMvc.perform(MockMvcRequestBuilders.put("/api/employees/update/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(updatedEmployeeJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Updated User")))
                .andExpect(jsonPath("$.department", is("Updated Dept")));

        verify(databaseProxy, times(1)).update(eq(1L), any(Employee.class));
    }

    @Test
    public void testDeleteEmployee() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/api/employees/delete/1"))
                .andExpect(status().isNoContent());

        verify(databaseProxy, times(1)).delete(1L);
    }


    // --- Tests for DatabaseProxy ---

    @Test
    public void testDatabaseProxyCreate() {
        Employee employee = new Employee("Test", "Testing");
        databaseProxy.create(employee);
        verify(databaseManager, times(1)).create(employee);
    }

    @Test
    public void testDatabaseProxyReadAll() {
        List<Employee> employees = Arrays.asList(new Employee(), new Employee());
        when(databaseManager.readAll()).thenReturn(employees);
        List<Employee> result = databaseProxy.readAll();
        verify(databaseManager, times(1)).readAll();
    }

    @Test
    public void testDatabaseProxyReadById() {
        Employee employee = new Employee(1L, "Test", "Testing");
        when(databaseManager.readById(1L)).thenReturn(employee);
        Employee result = databaseProxy.readById(1L);
        verify(databaseManager, times(1)).readById(1L);
    }

    @Test
    public void testDatabaseProxyUpdate() {
        Employee employee = new Employee(1L, "Updated", "Updated");
        when(databaseManager.update(1L, employee)).thenReturn(employee);
        Employee result = databaseProxy.update(1L, employee);
        verify(databaseManager, times(1)).update(1L, employee);
    }

    @Test
    public void testDatabaseProxyDelete() {
        databaseProxy.delete(1L);
        verify(databaseManager, times(1)).delete(1L);
    }

    // --- Additional Tests for Edge Cases and Exception Handling ---

    @Test
    public void testReadEmployeeByIdNotFound() throws Exception {
        when(databaseManager.readById(99L)).thenReturn(null);

        mockMvc.perform(MockMvcRequestBuilders.get("/api/employees/read/99"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").doesNotExist());

        verify(databaseProxy, times(1)).readById(99L);
    }

    @Test
    public void testUpdateEmployeeNotFound() throws Exception {
        String updatedEmployeeJson = "{\"name\": \"Updated User\", \"department\": \"Updated Dept\"}";
        when(databaseManager.update(eq(99L), any(Employee.class))).thenReturn(null);

        mockMvc.perform(MockMvcRequestBuilders.put("/api/employees/update/99")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(updatedEmployeeJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").doesNotExist()); // Or any other appropriate response

        verify(databaseProxy, times(1)).update(eq(99L), any(Employee.class));
    }

    @Test
    public void testDeleteEmployeeNotFound() throws Exception {
        doNothing().when(databaseManager).delete(99L); // Assuming delete doesn't throw an exception if not found

        mockMvc.perform(MockMvcRequestBuilders.delete("/api/employees/delete/99"))
                .andExpect(status().isNoContent()); // Or any other appropriate response

        verify(databaseProxy, times(1)).delete(99L);
    }

    @Test
    public void testReadAllEmployeesEmptyDatabase() throws Exception {
        when(databaseManager.readAll()).thenReturn(Collections.emptyList());
        mockMvc.perform(MockMvcRequestBuilders.get("/api/employees/read"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));

        verify(databaseProxy, times(1)).readAll();
    }
}