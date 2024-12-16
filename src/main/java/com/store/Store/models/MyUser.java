package com.store.Store.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name="users")
public class MyUser {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;

    @Column(unique = true)
    private String name;

    private String password;
    private String roles;
}
