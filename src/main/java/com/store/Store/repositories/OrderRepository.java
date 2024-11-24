package com.store.Store.repositories;

import com.store.Store.models.Order;
import org.springframework.data.jpa.repository.JpaRepository;

// Репозиторий для заказов
public interface OrderRepository extends JpaRepository<Order, Long> { }
