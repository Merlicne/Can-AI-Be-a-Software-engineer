package com.example.demo.proxy;

import com.example.demo.model.Item;
import com.example.demo.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DatabaseManager implements DatabaseOperations<Item> {

    @Autowired
    private ItemRepository itemRepository;

    @Override
    public Item create(Item entity) {
        return itemRepository.save(entity);
    }

    @Override
    public List<Item> readAll() {
        return itemRepository.findAll();
    }

    @Override
    public Item readById(Long id) {
        return itemRepository.findById(id).orElse(null);
    }

    @Override
    public Item update(Long id, Item entity) {
        if (itemRepository.existsById(id)) {
            entity.setId(id);
            return itemRepository.save(entity);
        }
        return null;
    }

    @Override
    public void delete(Long id) {
        itemRepository.deleteById(id);
    }
}
