package com.example.demo.proxy;

import com.example.demo.model.Product;

import java.util.List;
import java.util.Optional;

public interface DatabaseOperations<T> {
    T create(T entity);
    Optional<T> read(Long id);
    List<T> readAll();
    T update(T entity);
    void delete(Long id);
}