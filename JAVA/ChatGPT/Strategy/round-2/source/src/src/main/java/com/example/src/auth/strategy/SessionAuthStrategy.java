package com.example.src.auth.strategy;

import javax.servlet.http.HttpServletRequest;
import java.util.HashSet;
import java.util.Set;

public class SessionAuthStrategy implements Authenticator {
    private static final Set<String> validSessions = new HashSet<>();

    @Override
    public boolean authenticate(HttpServletRequest request) {
        String sessionId = request.getCookies() != null ? 
            Arrays.stream(request.getCookies())
                  .filter(cookie -> "SESSIONID".equals(cookie.getName()))
                  .map(Cookie::getValue)
                  .findFirst()
                  .orElse(null) : null;
        return sessionId != null && validSessions.contains(sessionId);
    }
}