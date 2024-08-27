package com.example.src.authsystem.services;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Base64;
import javax.servlet.http.HttpServletRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.example.src.strategies.BasicAuthStrategy;

class BasicAuthStrategyTest {

    private BasicAuthStrategy basicAuthStrategy;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        basicAuthStrategy = new BasicAuthStrategy();
        request = mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticate_Success() {
        // Mock a valid Authorization header
        String credentials = "admin:password";
        String encodedCredentials = "Basic " + Base64.getEncoder().encodeToString(credentials.getBytes());
        when(request.getHeader("Authorization")).thenReturn(encodedCredentials);

        boolean result = basicAuthStrategy.authenticate(request);
        assertTrue(result);  // Success case
    }

    @Test
    void testAuthenticate_InvalidHeader() {
        // No Authorization header
        when(request.getHeader("Authorization")).thenReturn(null);

        boolean result = basicAuthStrategy.authenticate(request);
        assertFalse(result);  // Missing Authorization header
    }

    @Test
    void testAuthenticate_InvalidCredentials() {
        // Mock an Authorization header with wrong credentials
        String credentials = "user:wrongpassword";
        String encodedCredentials = "Basic " + Base64.getEncoder().encodeToString(credentials.getBytes());
        when(request.getHeader("Authorization")).thenReturn(encodedCredentials);

        boolean result = basicAuthStrategy.authenticate(request);
        assertFalse(result);  // Invalid credentials case
    }
}
