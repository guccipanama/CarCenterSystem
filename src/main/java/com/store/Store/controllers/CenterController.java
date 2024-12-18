package com.store.Store.controllers;

import com.store.Store.models.Car;
import com.store.Store.models.Center;
import com.store.Store.services.CenterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class CenterController {
    @Autowired
    private CenterService CenterService;


    @GetMapping("/api/centers")
    @PreAuthorize("hasAuthority('ROLE_USER')")
    public List<Center> getAllCenters() {
        return CenterService.getAllCenters();
    }

    @GetMapping("/api/centers/{identity}")
    @PreAuthorize("hasAuthority('ROLE_USER')")
    public Center getSingleCenter(@PathVariable("identity") Long id) {
        return CenterService.findById(id);
    };

    @GetMapping("/api/centers/{identity}/address")
    @PreAuthorize("hasAuthority('ROLE_USER')")
    public String getCenterAddress(@PathVariable("identity") Long id) {
        return CenterService.getCenterAddressById(id);
    }

    @PostMapping(value="/add/center", consumes={"application/json"})
    public ResponseEntity<Center> addCenter(@RequestBody Center center) {
        Center savedCenter = CenterService.saveCenter(center);
        return ResponseEntity.ok(savedCenter);
    }
}
