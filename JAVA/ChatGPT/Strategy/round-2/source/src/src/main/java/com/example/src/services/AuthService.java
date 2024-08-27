package com.example.src.services;

import javax.servlet.http.HttpServletRequest;
import com.example.src.strategies.Authenticator;

public class AuthService {
    private Authenticator authenticator;

    public AuthService(Authenticator authenticator) {
        this.authenticator = authenticator;
    }

    public void setAuthenticator(Authenticator authenticator) {
        this.authenticator = authenticator;
    }

    public boolean authenticate(HttpServletRequest request) {
        return authenticator.authenticate(request);
    }
}
