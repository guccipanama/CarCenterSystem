package com.store.Store.services;


import com.store.Store.models.Car;
import com.store.Store.repositories.CarRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
import java.util.Optional;

@Service
public class CarService {
    @Autowired
    private CarRepository carRepository;

    public List<Car> getAllCars() {
        return carRepository.findAll();
    }

    public Car findById(@PathVariable("identity") Long id) {
        return carRepository.findById(id).get();
    }

    public String getCarNameById(Long id) {
        Optional<Car> carOptional = carRepository.findById(id);

        // Если запись найдена, возвращаем car_name, иначе сообщение об отсутствии
        return carOptional.map(Car::getCarName)
                .orElseThrow(() -> new RuntimeException("Car not found with id: " + id));
    }
}
