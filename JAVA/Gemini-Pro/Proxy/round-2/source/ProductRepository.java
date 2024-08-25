package com.example.crudapi.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.example.crudapi.model.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {

}