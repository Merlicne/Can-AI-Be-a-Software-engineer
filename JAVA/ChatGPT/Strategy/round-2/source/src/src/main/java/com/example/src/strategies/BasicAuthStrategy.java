package com.example.src.strategies;


import java.util.Base64;
import javax.servlet.http.HttpServletRequest;

public class BasicAuthStrategy implements Authenticator {
    @Override
    public boolean authenticate(jakarta.servlet.http.HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Basic ")) {
            String encodedCredentials = authHeader.substring(6);
            String decodedCredentials = new String(Base64.getDecoder().decode(encodedCredentials));
            String[] userDetails = decodedCredentials.split(":");

            String username = userDetails[0];
            String password = userDetails[1];

            // Compare with predefined users
            return "admin".equals(username) && "password".equals(password);
        }
        return false;
    }
}