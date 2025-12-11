package com.daribear.pi_alarm_backend;

import org.springframework.security.core.authority.SimpleGrantedAuthority;

import java.util.HashSet;
import java.util.Set;

public enum AccountRole {
    ADMIN("admin"),
    USER("user");

    private String role;

    AccountRole(String role) {
        this.role = role;
    }

    public Set<SimpleGrantedAuthority> getGrantedAuthorities(){
        Set<SimpleGrantedAuthority> permissions = new HashSet<>();
        permissions.add(new SimpleGrantedAuthority("ROLE_" + this.name()));
        return permissions;
    }
}
