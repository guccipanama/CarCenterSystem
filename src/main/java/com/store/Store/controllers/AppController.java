package com.store.Store.controllers;

import com.store.Store.models.MyUser;
import com.store.Store.services.AppService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
public class AppController {
    private AppService service;

    @GetMapping("/welcome")
    public String getWelcome() {
        return "Welcome page";
    }

    @PostMapping("/new-user")
    public String addUser(@RequestBody MyUser user){
        service.addUser(user);
        return "User is saved";
    }















}
