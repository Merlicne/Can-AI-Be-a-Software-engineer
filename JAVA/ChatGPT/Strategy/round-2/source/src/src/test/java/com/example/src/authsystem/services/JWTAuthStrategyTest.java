package com.example.src.authsystem.services;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import io.jsonwebtoken.*;
import javax.servlet.http.HttpServletRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.example.src.strategies.JWTAuthStrategy;

class JWTAuthStrategyTest {

    private JWTAuthStrategy jwtAuthStrategy;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        jwtAuthStrategy = new JWTAuthStrategy();
        request = mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticate_Success() {
        // Mock a valid JWT token
        String validToken = Jwts.builder()
                .setSubject("user")
                .signWith(SignatureAlgorithm.HS256, "secret")
                .compact();
        when(request.getHeader("Authorization")).thenReturn("Bearer " + validToken);

        boolean result = jwtAuthStrategy.authenticate(request);
        assertTrue(result);  // Success case
    }

    @Test
    void testAuthenticate_InvalidToken() {
        // Mock an invalid JWT token
        when(request.getHeader("Authorization")).thenReturn("Bearer invalidToken");

        boolean result = jwtAuthStrategy.authenticate(request);
        assertFalse(result);  // Invalid token case
    }

    @Test
    void testAuthenticate_MissingHeader() {
        // No Authorization header
        when(request.getHeader("Authorization")).thenReturn(null);

        boolean result = jwtAuthStrategy.authenticate(request);
        assertFalse(result);  // Missing header case
    }
}
