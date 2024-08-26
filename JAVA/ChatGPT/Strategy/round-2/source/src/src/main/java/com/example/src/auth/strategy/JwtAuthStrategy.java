package com.example.src.auth.strategy;


import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureException;

import javax.servlet.http.HttpServletRequest;

public class JwtAuthStrategy implements Authenticator {
    private static final String SECRET_KEY = "your_secret_key";

    @Override
    public boolean authenticate(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring("Bearer ".length()).trim();
            try {
                Claims claims = Jwts.parser()
                        .setSigningKey(SECRET_KEY)
                        .parseClaimsJws(token)
                        .getBody();
                return true; // Token is valid
            } catch (SignatureException e) {
                return false; // Invalid token
            }
        }
        return false;
    }
}