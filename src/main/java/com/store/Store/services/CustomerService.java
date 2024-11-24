package com.store.Store.services;


import com.store.Store.models.Customer;
import com.store.Store.repositories.CustomerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
import java.util.Optional;

@Service
public class CustomerService {
    @Autowired
    private CustomerRepository CustomerRepository;

    public Customer findById(@PathVariable("identity") Long id) {
        return CustomerRepository.findById(id).get();
    }

    public String getCustomerNameById(Long id) {
        Optional<Customer> CustomerOptional = CustomerRepository.findById(id);

        // Если запись найдена, возвращаем CenterAddress, иначе сообщение об отсутствии
        return CustomerOptional.map(Customer::getCustomerName)
                .orElseThrow(() -> new RuntimeException("Center not found with id: " + id));
    }

    public List<Customer> getAllCustomers() { return CustomerRepository.findAll();
    }

}


