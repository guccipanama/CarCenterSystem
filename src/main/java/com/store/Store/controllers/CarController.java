package com.store.Store.controllers;

import com.store.Store.models.Car;
import com.store.Store.services.CarService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/*package com.store.Store.controllers;

import com.store.Store.model.Address;
import com.store.Store.repository.MySqlRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class StoreController {
    @Autowired
    MySqlRepository mySqlRepository;

    @GetMapping("/get-all-addresses")
    public List<Address> getAddresses() {
        return mySqlRepository.findAll();
    };

    @GetMapping("/get-address/{identity}")
    public Address getSingleAddress(@PathVariable("identity") Integer id) {
        return mySqlRepository.findById(id).get();
    };
}*/


@RestController
public class CarController {
    @Autowired
    private CarService carService;

    @GetMapping("/api/cars")
    public List<Car> getAllCars() {
        return carService.getAllCars();
    }

    @GetMapping("/api/cars/{identity}")
    public Car getSingleCar(@PathVariable("identity") Long id) {
        return carService.findById(id);
    };

    @GetMapping("/api/cars/{identity}/name")
    public String getCarName(@PathVariable("identity") Long id) {
        return carService.getCarNameById(id);
    }
}
