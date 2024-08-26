package com.example.src.auth.strategy;


import javax.servlet.http.HttpServletRequest;
import java.util.HashSet;
import java.util.Set;

public class ApiKeyAuthStrategy implements Authenticator {
    private static final Set<String> validApiKeys = new HashSet<>();

    @Override
    public boolean authenticate(HttpServletRequest request) {
        String apiKey = request.getHeader("Authorization");
        if (apiKey != null) {
            return validApiKeys.contains(apiKey);
        }
        return false;
    }
}