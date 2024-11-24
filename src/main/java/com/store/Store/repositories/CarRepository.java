package com.store.Store.repositories;

import com.store.Store.models.Car;
import org.springframework.data.jpa.repository.JpaRepository;

// Репозиторий для машин
public interface CarRepository extends JpaRepository<Car, Long> { }