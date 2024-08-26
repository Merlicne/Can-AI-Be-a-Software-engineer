import com.example.authentication.AuthContext;
import com.example.authentication.BasicAuthenticator;
import com.example.authentication.JWTAuthenticator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.HttpServletRequest;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AuthContextTest {

    private AuthContext authContext;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        authContext = new AuthContext();
        request = Mockito.mock(HttpServletRequest.class);
    }

    @Test
    void testSwitchingStrategies() {
        authContext.setAuthenticator(new BasicAuthenticator());
        when(request.getHeader("Authorization")).thenReturn("Basic " + java.util.Base64.getEncoder().encodeToString("user1:password1".getBytes()));
        assertTrue(authContext.authenticate(request));

        authContext.setAuthenticator(new JWTAuthenticator());
        String token = new JWTAuthenticator().generateToken("user1");
        when(request.getHeader("Authorization")).thenReturn("Bearer " + token);
        assertTrue(authContext.authenticate(request));
    }

    @Test
    void testNoStrategySelected() {
        try {
            authContext.authenticate(request);
        } catch (IllegalStateException e) {
            assertTrue(e.getMessage().contains("No authentication strategy set"));
        }
    }
}
