package com.daribear.pi_alarm_backend.Entities;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class JWTToken {
    private String accessCode;
}
