package com.example.crudapi.service;

import com.example.crudapi.model.Product;

import java.util.List;

// Define the interface for database operations
public interface DatabaseOperations<T, ID> {

    T create(T entity);
    T read(ID id);
    List<T> readAll();
    T update(T entity);
    void delete(ID id);

}