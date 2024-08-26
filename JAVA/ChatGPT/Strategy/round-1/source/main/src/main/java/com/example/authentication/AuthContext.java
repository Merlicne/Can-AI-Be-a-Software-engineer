package com.example.authentication;


import javax.servlet.http.HttpServletRequest;

public class AuthContext {
    private Authenticator authenticator;

    public void setAuthenticator(Authenticator authenticator) {
        this.authenticator = authenticator;
    }

    public boolean authenticate(HttpServletRequest request) {
        if (authenticator == null) {
            throw new IllegalStateException("No authentication strategy set");
        }
        return authenticator.authenticate(request);
    }
}
