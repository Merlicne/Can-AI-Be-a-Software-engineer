package com.example.authentication;

import javax.servlet.http.HttpServletRequest;


public interface Authenticator {
    boolean authenticate(HttpServletRequest request);
}
