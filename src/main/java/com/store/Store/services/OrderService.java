package com.store.Store.services;


import com.store.Store.models.Order;
import com.store.Store.repositories.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class OrderService {
    @Autowired
    private OrderRepository OrderRepository;

    public Order findById(@PathVariable("identity") Long id) {
        return OrderRepository.findById(id).get();
    }

    public LocalDate getOrderDateById(Long id) {
        Optional<Order> CustomerOptional = OrderRepository.findById(id);

        // Если запись найдена, возвращаем OrderDate, иначе сообщение об отсутствии
        return CustomerOptional.map(Order::getOrderDate)
                .orElseThrow(() -> new RuntimeException("Center not found with id: " + id));
    }

    public List<Order> getAllOrders() { return OrderRepository.findAll();
    }

}

