package com.daribear.pi_alarm_backend.Services;

import com.daribear.pi_alarm_backend.AccountRole;
import com.daribear.pi_alarm_backend.Entities.Account;
import com.daribear.pi_alarm_backend.Errors.ErrorStorage;
import com.daribear.pi_alarm_backend.IncomeClasses.RegisterDto;
import com.daribear.pi_alarm_backend.Repositories.AccountRepository;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.HashSet;

@Service
public class AuthService implements UserDetailsService {

    @Autowired
    AccountRepository repository;


    public UserDetails signUp(RegisterDto registerDto) {
        /**
        boolean isEmailValid = emailValidator.test(request.getEmail());
        if (!isEmailValid){
            throw ErrorStorage.getCustomErrorFromType(ErrorStorage.ErrorType.REGISTEREMAILNOTVALID);
        }
         */
        if (repository.findByEmail(registerDto.getLogin()) != null){
            throw ErrorStorage.getCustomErrorFromType(ErrorStorage.ErrorType.REGEMAILTAKE);
        }
        Account newAccount = new Account(registerDto.getLogin(), registerDto.getPassword(), (HashSet<SimpleGrantedAuthority>) AccountRole.USER.getGrantedAuthorities());

        return repository.save(newAccount);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDetails user = repository.findByEmail(username);
        return user;
    }
}
