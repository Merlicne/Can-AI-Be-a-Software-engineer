package com.example.src.strategies;

import javax.servlet.http.HttpServletRequest;

public class APIKeyAuthStrategy implements Authenticator {
    @Override
    public boolean authenticate(HttpServletRequest request) {
        String apiKey = request.getHeader("Authorization");
        if (apiKey == null) {
            apiKey = request.getParameter("apiKey");
        }

        // Verify the API key
        return "valid_api_key".equals(apiKey);
    }
}