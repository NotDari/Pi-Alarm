package com.daribear.pi_alarm_backend.Controllers;

import com.daribear.pi_alarm_backend.Auth.TokenProvider;
import com.daribear.pi_alarm_backend.Entities.JWTToken;
import com.daribear.pi_alarm_backend.IncomeClasses.LoginDto;
import com.daribear.pi_alarm_backend.IncomeClasses.RegisterDto;
import com.daribear.pi_alarm_backend.Services.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.User;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/v1/auth")
public class AuthController {
    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired
    private AuthService service;
    @Autowired
    private TokenProvider tokenService;

    @PostMapping("/register")
    public ResponseEntity<?> signUp(@RequestBody RegisterDto data) {
        service.signUp(data);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @PostMapping("/login")
    public ResponseEntity<JWTToken> signIn(@RequestBody LoginDto data) {
        UsernamePasswordAuthenticationToken usernamePassword = new UsernamePasswordAuthenticationToken(data.getLogin(), data.getPassword());
        Authentication authUser = authenticationManager.authenticate(usernamePassword);
        var accessToken = tokenService.generateJWTAccessToken((User) authUser.getPrincipal());
        return ResponseEntity.ok(new JWTToken(accessToken));
    }
}
