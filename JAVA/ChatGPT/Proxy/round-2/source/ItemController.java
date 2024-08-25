package com.example.demo.controller;

import com.example.demo.model.Item;
import com.example.demo.proxy.DatabaseOperations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/items")
public class ItemController {

    @Autowired
    private DatabaseOperations<Item> databaseProxy;

    @PostMapping("/create")
    public Item createItem(@RequestBody Item item) {
        return databaseProxy.create(item);
    }

    @GetMapping("/read")
    public List<Item> readItems() {
        return databaseProxy.readAll();
    }

    @GetMapping("/read/{id}")
    public Item readItemById(@PathVariable Long id) {
        return databaseProxy.readById(id);
    }

    @PutMapping("/update/{id}")
    public Item updateItem(@PathVariable Long id, @RequestBody Item item) {
        return databaseProxy.update(id, item);
    }

    @DeleteMapping("/delete/{id}")
    public void deleteItem(@PathVariable Long id) {
        databaseProxy.delete(id);
    }
}
