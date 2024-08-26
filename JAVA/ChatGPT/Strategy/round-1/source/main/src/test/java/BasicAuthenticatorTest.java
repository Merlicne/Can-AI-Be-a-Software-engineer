import com.example.authentication.BasicAuthenticator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.HttpServletRequest;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

class BasicAuthenticatorTest {

    private BasicAuthenticator authenticator;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        authenticator = new BasicAuthenticator();
        request = Mockito.mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticateValidCredentials() {
        when(request.getHeader("Authorization")).thenReturn("Basic " + java.util.Base64.getEncoder().encodeToString("user1:password1".getBytes()));
        assertTrue(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateInvalidCredentials() {
        when(request.getHeader("Authorization")).thenReturn("Basic " + java.util.Base64.getEncoder().encodeToString("user1:wrongPassword".getBytes()));
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateMissingAuthorizationHeader() {
        when(request.getHeader("Authorization")).thenReturn(null);
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateMalformedAuthorizationHeader() {
        when(request.getHeader("Authorization")).thenReturn("Basic malformed");
        assertFalse(authenticator.authenticate(request));
    }
}
