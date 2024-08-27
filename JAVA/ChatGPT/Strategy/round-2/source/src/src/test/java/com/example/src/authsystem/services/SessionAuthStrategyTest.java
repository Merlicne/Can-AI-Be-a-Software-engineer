package com.example.src.authsystem.services;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.example.src.strategies.SessionAuthStrategy;

class SessionAuthStrategyTest {

    private SessionAuthStrategy sessionAuthStrategy;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        sessionAuthStrategy = new SessionAuthStrategy();
        request = mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticate_Success() {
        // Mock a valid session cookie
        Cookie[] cookies = {new Cookie("SESSIONID", "valid_session")};
        when(request.getCookies()).thenReturn(cookies);

        boolean result = sessionAuthStrategy.authenticate(request);
        assertTrue(result);  // Success case
    }

    @Test
    void testAuthenticate_MissingCookie() {
        // No cookies in the request
        when(request.getCookies()).thenReturn(null);

        boolean result = sessionAuthStrategy.authenticate(request);
        assertFalse(result);  // Missing cookie case
    }

    @Test
    void testAuthenticate_InvalidSession() {
        // Mock a session cookie with invalid session ID
        Cookie[] cookies = {new Cookie("SESSIONID", "invalid_session")};
        when(request.getCookies()).thenReturn(cookies);

        boolean result = sessionAuthStrategy.authenticate(request);
        assertFalse(result);  // Invalid session ID case
    }
}
