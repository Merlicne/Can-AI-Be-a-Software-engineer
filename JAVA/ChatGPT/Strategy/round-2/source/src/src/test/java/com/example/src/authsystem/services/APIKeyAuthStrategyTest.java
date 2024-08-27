package com.example.src.authsystem.services;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import javax.servlet.http.HttpServletRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.example.src.strategies.APIKeyAuthStrategy;

class APIKeyAuthStrategyTest {

    private APIKeyAuthStrategy apiKeyAuthStrategy;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        apiKeyAuthStrategy = new APIKeyAuthStrategy();
        request = mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticate_SuccessHeader() {
        // Mock a valid API key in the header
        when(request.getHeader("Authorization")).thenReturn("valid_api_key");

        boolean result = apiKeyAuthStrategy.authenticate(request);
        assertTrue(result);  // Success case (header)
    }

    @Test
    void testAuthenticate_SuccessQueryParameter() {
        // Mock a valid API key as a query parameter
        when(request.getHeader("Authorization")).thenReturn(null);
        when(request.getParameter("apiKey")).thenReturn("valid_api_key");

        boolean result = apiKeyAuthStrategy.authenticate(request);
        assertTrue(result);  // Success case (query parameter)
    }

    @Test
    void testAuthenticate_InvalidAPIKey() {
        // Mock an invalid API key
        when(request.getHeader("Authorization")).thenReturn("invalid_api_key");

        boolean result = apiKeyAuthStrategy.authenticate(request);
        assertFalse(result);  // Invalid API key case
    }

    @Test
    void testAuthenticate_MissingAPIKey() {
        // No API key in header or query parameter
        when(request.getHeader("Authorization")).thenReturn(null);
        when(request.getParameter("apiKey")).thenReturn(null);

        boolean result = apiKeyAuthStrategy.authenticate(request);
        assertFalse(result);  // Missing API key case
    }
}

