package com.store.Store.controllers;

import com.store.Store.models.Order;
import com.store.Store.services.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

@RestController
public class OrderController {
    @Autowired
    private OrderService OrderService;

    @GetMapping("/api/orders")
    public List<Order> getAllOrders() {
        return OrderService.getAllOrders();
    }

    @GetMapping("/api/orders/{identity}")
    public Order getSingleOrder(@PathVariable("identity") Long id) {
        return OrderService.findById(id);
    };

    @GetMapping("/api/orders/{identity}/name")
    public LocalDate getOrderDate(@PathVariable("identity") Long id) {
        return OrderService.getOrderDateById(id);
    }
}


