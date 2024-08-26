import com.example.authentication.APIKeyAuthenticator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.HttpServletRequest;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

class APIKeyAuthenticatorTest {

    private APIKeyAuthenticator authenticator;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        authenticator = new APIKeyAuthenticator();
        request = Mockito.mock(HttpServletRequest.class);
    }

    @Test
    void testAuthenticateValidAPIKey() {
        when(request.getHeader("API-Key")).thenReturn("key1");
        assertTrue(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateInvalidAPIKey() {
        when(request.getHeader("API-Key")).thenReturn("invalidKey");
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateMissingAPIKey() {
        when(request.getHeader("API-Key")).thenReturn(null);
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateAPIKeyAsQueryParameter() {
        // Assuming the API Key should be in headers, not query parameters
        when(request.getParameter("API-Key")).thenReturn("key1");
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateMalformedAPIKey() {
        when(request.getHeader("API-Key")).thenReturn("malformedKey");
        assertFalse(authenticator.authenticate(request));
    }
}
