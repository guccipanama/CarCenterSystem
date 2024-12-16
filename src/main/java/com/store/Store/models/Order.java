package com.store.Store.models;
import jakarta.persistence.*;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDate;


@Getter
@Setter
@ToString
@EqualsAndHashCode
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String orderId;

    private LocalDate orderDate;

    @ManyToOne
    @JoinColumn(name = "order_car_id", nullable = false)
    private Car car;

    @ManyToOne
    @JoinColumn(name = "order_customer_id", nullable = false)
    private Customer customer;
}