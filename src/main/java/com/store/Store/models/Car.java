package com.store.Store.models;


import jakarta.persistence.*;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@EqualsAndHashCode
@Entity
@Table(name = "car")
public class Car {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String carId;
    //private Long carCenterId;

    private String carName;
    private String carCost;

    @OneToOne
    @JoinColumn(name = "car_center_id", nullable = false)
    private Center center;

    public String getCarCenter() { return center.getCenterAddress();
    }
}
