package com.example.demo.proxy;

import com.example.demo.entity.Record;
import java.util.List;

public interface DatabaseOperations {
    Record create(Record record);
    List<Record> readAll();
    Record readById(Long id);
    Record update(Long id, Record updatedRecord);
    void delete(Long id);
}
