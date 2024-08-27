import com.example.authentication.SessionAuthenticator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

class SessionAuthenticatorTest {

    private SessionAuthenticator authenticator;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        authenticator = new SessionAuthenticator();
        request = Mockito.mock(HttpServletRequest.class);
    }

    @Test
    void testCreateSession() {
        String sessionId = authenticator.createSession("user1");
        assertTrue(authenticator.authenticate(createRequestWithCookie(sessionId)));
    }

    @Test
    void testAuthenticateValidSession() {
        String sessionId = authenticator.createSession("user1");
        assertTrue(authenticator.authenticate(createRequestWithCookie(sessionId)));
    }

    @Test
    void testAuthenticateInvalidSession() {
        assertFalse(authenticator.authenticate(createRequestWithCookie("invalidSessionId")));
    }

    @Test
    void testAuthenticateMissingSessionCookie() {
        when(request.getCookies()).thenReturn(null);
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testLogoutFunctionality() {
        String sessionId = authenticator.createSession("user1");
        authenticator.invalidateSession(sessionId); // Implement invalidate method to remove session
        assertFalse(authenticator.authenticate(createRequestWithCookie(sessionId)));
    }

    private HttpServletRequest createRequestWithCookie(String sessionId) {
        HttpServletRequest request = Mockito.mock(HttpServletRequest.class);
        Cookie cookie = new Cookie("SESSIONID", sessionId);
        when(request.getCookies()).thenReturn(new Cookie[]{cookie});
        return request;
    }
}
