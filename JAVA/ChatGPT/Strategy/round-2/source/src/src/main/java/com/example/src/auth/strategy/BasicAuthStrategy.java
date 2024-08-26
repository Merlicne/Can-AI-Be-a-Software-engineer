package com.example.src.auth.strategy;

import javax.servlet.http.HttpServletRequest;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class BasicAuthStrategy implements Authenticator {
    private static final Map<String, String> users = new HashMap<>();
    
    static {
        // Example predefined users
        users.put("user", "password");
    }

    @Override
    public boolean authenticate(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Basic ")) {
            String base64Credentials = authHeader.substring("Basic ".length()).trim();
            String credentials = new String(Base64.getDecoder().decode(base64Credentials));
            String[] values = credentials.split(":", 2);
            String username = values[0];
            String password = values[1];
            return users.containsKey(username) && users.get(username).equals(password);
        }
        return false;
    }
}