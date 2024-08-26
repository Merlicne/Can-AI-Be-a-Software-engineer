package com.example.demo.proxy;

import com.example.demo.entity.Record;
import com.example.demo.repository.RecordRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
public class DatabaseManager implements DatabaseOperations {

    @Autowired
    private RecordRepository recordRepository;

    @Override
    public Record create(Record record) {
        return recordRepository.save(record);
    }

    @Override
    public List<Record> readAll() {
        return recordRepository.findAll();
    }

    @Override
    public Record readById(Long id) {
        Optional<Record> record = recordRepository.findById(id);
        return record.orElse(null);
    }

    @Override
    public Record update(Long id, Record updatedRecord) {
        Optional<Record> existingRecord = recordRepository.findById(id);
        if (existingRecord.isPresent()) {
            updatedRecord.setId(id);
            return recordRepository.save(updatedRecord);
        } else {
            return null;
        }
    }

    @Override
    public void delete(Long id) {
        recordRepository.deleteById(id);
    }
}
