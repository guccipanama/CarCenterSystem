package com.store.Store.controllers;

import com.store.Store.models.Center;
import com.store.Store.services.CenterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class CenterController {
    @Autowired
    private CenterService CenterService;

    @GetMapping("/api/centers")
    public List<Center> getAllCenters() {
        return CenterService.getAllCenters();
    }

    @GetMapping("/api/centers/{identity}")
    public Center getSingleCenter(@PathVariable("identity") Long id) {
        return CenterService.findById(id);
    };

    @GetMapping("/api/centers/{identity}/address")
    public String getCenterAddress(@PathVariable("identity") Long id) {
        return CenterService.getCenterAddressById(id);
    }
}
