package com.example.src.strategies;


import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;

public class SessionAuthStrategy implements Authenticator {
    private static final String SESSION_ID = "SESSIONID";

    @Override
    public boolean authenticate(HttpServletRequest request) {
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if (SESSION_ID.equals(cookie.getName()) && isValidSession(cookie.getValue())) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean isValidSession(String sessionId) {
        // Validate session ID against stored sessions
        return "valid_session".equals(sessionId);
    }
}