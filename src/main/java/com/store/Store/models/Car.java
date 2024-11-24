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
    private Long carId;
    //private Long carCenterId;

    private String carName;
    private Double carCost;

    @OneToOne
    @JoinColumn(name = "car_center_id", nullable = false)
    private Center center;

    public String getCarCenter() { return center.getCenterAddress();
    }
}

/*
@Entity
@Table(name = "Addresses")
public class Address {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private int number;
    private String street;
    private String postcode;

    public Address(int number, String street, String postcode) {
        this.number = number;
        this.street = street;
        this.postcode = postcode;
    }

    public Address() {

    }

    public int getId() {
        return id;
    }
    public int getNumber() {
        return number;
    }
    public void setNumber(int number) {
        this.number = number;
    }
    public String getStreet() {
        return street;
    }
    public void setStreet(String street) {
        this.street = street;
    }
    public String getPostcode() {
        return postcode;
    }
    public void setPostcode(String postcode) {
        this.postcode = postcode;
    }
}
*/
