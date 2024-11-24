package com.store.Store.repositories;

import com.store.Store.models.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

// Репозиторий для клиентов
public interface CustomerRepository extends JpaRepository<Customer, Long> { }
