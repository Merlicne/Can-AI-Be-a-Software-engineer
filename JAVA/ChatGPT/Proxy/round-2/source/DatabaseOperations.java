package com.example.demo.proxy;

import java.util.List;

public interface DatabaseOperations<T> {
    T create(T entity);
    List<T> readAll();
    T readById(Long id);
    T update(Long id, T entity);
    void delete(Long id);
}
