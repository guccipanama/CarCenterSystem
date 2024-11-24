package com.store.Store.controllers;

import com.store.Store.models.Customer;
import com.store.Store.services.CustomerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class CustomerController {
    @Autowired
    private CustomerService CustomerService;

    @GetMapping("/api/customers")
    public List<Customer> getAllCustomers() {
        return CustomerService.getAllCustomers();
    }

    @GetMapping("/api/customers/{identity}")
    public Customer getSingleCustomer(@PathVariable("identity") Long id) {
        return CustomerService.findById(id);
    };

    @GetMapping("/api/customers/{identity}/name")
    public String getCustomerName(@PathVariable("identity") Long id) {
        return CustomerService.getCustomerNameById(id);
    }
}

