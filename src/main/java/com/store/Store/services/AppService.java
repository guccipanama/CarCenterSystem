package com.store.Store.services;

import com.store.Store.models.MyUser;
import com.store.Store.repositories.UserRepository;
import lombok.AllArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AppService {
    private UserRepository repository;
    private PasswordEncoder passwordEncoder;

    public void addUser(MyUser user){
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        repository.save(user);
    }
}
