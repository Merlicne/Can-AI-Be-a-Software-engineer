package com.example.src.auth.service;


import com.example.auth.strategy.Authenticator;
import javax.servlet.http.HttpServletRequest;

public class AuthService {
    private final Authenticator authenticator;

    public AuthService(Authenticator authenticator) {
        this.authenticator = authenticator;
    }

    public boolean authenticate(HttpServletRequest request) {
        return authenticator.authenticate(request);
    }
}