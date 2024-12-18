package com.store.Store.services;


import com.store.Store.models.Car;
import com.store.Store.models.Center;
import com.store.Store.repositories.CenterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
import java.util.Optional;

@Service
public class CenterService {
    @Autowired
    private CenterRepository CenterRepository;

    public Center findById(@PathVariable("identity") Long id) {
        return CenterRepository.findById(id).get();
    }

    public String getCenterAddressById(Long id) {
        Optional<Center> CenterOptional = CenterRepository.findById(id);

        // Если запись найдена, возвращаем CustomerName, иначе сообщение об отсутствии
        return CenterOptional.map(Center::getCenterAddress)
                .orElseThrow(() -> new RuntimeException("Center not found with id: " + id));
    }

    public List<Center> getAllCenters() { return CenterRepository.findAll();
    }

    public Center saveCenter(Center center) {
        return CenterRepository.save(center);
    }
    public ResponseEntity<String> deleteCenter(String id) {
        return CenterRepository.findById(Long.valueOf(id)).map(center -> {
            CenterRepository.delete(center);
            return ResponseEntity.ok("Center с ID " + id + " был успешно удалён.");
        }).orElseGet(() -> ResponseEntity.notFound().build());
    }
}
