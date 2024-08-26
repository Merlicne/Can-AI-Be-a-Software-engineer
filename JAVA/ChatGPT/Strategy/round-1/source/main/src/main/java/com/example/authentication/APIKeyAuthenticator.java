package com.example.authentication;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;

public class APIKeyAuthenticator implements Authenticator {
    private static final Map<String, String> apiKeys = new HashMap<>();

    static {
        apiKeys.put("user1", "key1");
        apiKeys.put("user2", "key2");
    }

    public boolean authenticate(HttpServletRequest request) {
        String apiKey = request.getHeader("API-Key");
        return apiKeys.containsValue(apiKey);
    }
}