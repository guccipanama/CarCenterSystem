package com.store.Store.controllers;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/")
    public String getHome() {
        return "Hello home";
    }

    @GetMapping("/test")
    public String getTest() {
        return "Hello test";
    }

    @GetMapping("/person")
    public Person getPerson() {
        Person p = new Person();
        p.setAge(20);
        p.setName("Bob");

        return p;
    }
}


class Person{
    private String name;
    private int age;

    public Person() {}

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}
