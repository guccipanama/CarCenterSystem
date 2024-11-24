package com.store.Store.repositories;

import com.store.Store.models.Center;
import org.springframework.data.jpa.repository.JpaRepository;

// Репозиторий для центров
public interface CenterRepository extends JpaRepository<Center, Long> { }
