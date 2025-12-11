package com.daribear.pi_alarm_backend.IncomeClasses;

import com.daribear.pi_alarm_backend.AccountRole;
import lombok.Data;

@Data
public class RegisterDto {
    private String login;
    private String password;
    private AccountRole accountRole;
}
