package com.store.Store.controllers;

import com.store.Store.models.Car;
import com.store.Store.models.Order;
import com.store.Store.services.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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


    @PostMapping(value="/add/order", consumes={"application/json"})
    public ResponseEntity<Order> addOrder(@RequestBody Order order) {
        Order savedOrder = OrderService.saveOrder(order);
        return ResponseEntity.ok(savedOrder);
    }


}


