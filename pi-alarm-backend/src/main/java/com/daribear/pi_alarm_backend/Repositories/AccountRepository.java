package com.daribear.pi_alarm_backend.Repositories;

import com.daribear.pi_alarm_backend.Entities.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;

public interface AccountRepository extends JpaRepository<Account, Long> {
    UserDetails findByEmail(String email);
}
