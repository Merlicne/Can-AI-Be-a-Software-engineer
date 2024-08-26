package com.example.src.auth.strategy;

import javax.servlet.http.HttpServletRequest;

public interface Authenticator {
    boolean authenticate(HttpServletRequest request);
}