package com.store.Store.services;


import com.store.Store.models.Center;
import com.store.Store.models.Order;
import com.store.Store.repositories.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
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

    public Optional<Order> getOrderDateById(Long id) {
        return OrderRepository.findById(id);
        // Если запись найдена, возвращаем OrderDate, иначе сообщение об отсутствии
        //return CustomerOptional.map(Order::getOrderDate)
        //        .orElseThrow(() -> new RuntimeException("Center not found with id: " + id));
    }

    public List<Order> getAllOrders() { return OrderRepository.findAll();
    }

    public Order saveOrder(Order order) {
        return OrderRepository.save(order);
    }
    public ResponseEntity<String> deleteOrder(String id) {
        return OrderRepository.findById(Long.valueOf(id)).map(order -> {
            OrderRepository.delete(order);
            return ResponseEntity.ok("Order с ID " + id + " был успешно удалён.");
        }).orElseGet(() -> ResponseEntity.notFound().build());
    }

}

