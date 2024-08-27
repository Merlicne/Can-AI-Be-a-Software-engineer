package com.example.src.strategies;


import javax.servlet.http.HttpServletRequest;

public interface Authenticator {
    boolean authenticate(HttpServletRequest request);
}
