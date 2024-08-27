package com.example;


import com.example.authentication.*;

import javax.servlet.http.HttpServletRequest;

public class Main {

    public static void main(String[] args) {
        AuthContext authContext = new AuthContext();

        // Choose Basic Authentication Strategy
        authContext.setAuthenticator(new BasicAuthenticator());

        // Example HttpServletRequest object (Assumed)
        HttpServletRequest request = createSampleRequest();

        // Authenticate
        boolean isAuthenticated = authContext.authenticate(request);
        System.out.println("Authentication successful: " + isAuthenticated);

        // Switch to JWT Authentication
        authContext.setAuthenticator(new JWTAuthenticator());
        // Authenticate with JWT
        isAuthenticated = authContext.authenticate(request);
        System.out.println("JWT Authentication successful: " + isAuthenticated);
    }

    private static HttpServletRequest createSampleRequest() {
        // Mocked request object for demonstration
        return null; // Replace with actual HttpServletRequest in a real app
    }
}