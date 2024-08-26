package com.example.demo.controller;

import com.example.demo.entity.Record;
import com.example.demo.proxy.DatabaseOperations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/records")
public class RecordController {

    @Autowired
    private DatabaseOperations databaseProxy;

    @PostMapping("/create")
    public Record createRecord(@RequestBody Record record) {
        return databaseProxy.create(record);
    }

    @GetMapping("/read")
    public List<Record> readAllRecords() {
        return databaseProxy.readAll();
    }

    @GetMapping("/read/{id}")
    public Record readRecordById(@PathVariable Long id) {
        return databaseProxy.readById(id);
    }

    @PutMapping("/update/{id}")
    public Record updateRecord(@PathVariable Long id, @RequestBody Record record) {
        return databaseProxy.update(id, record);
    }

    @DeleteMapping("/delete/{id}")
    public void deleteRecord(@PathVariable Long id) {
        databaseProxy.delete(id);
    }
}
