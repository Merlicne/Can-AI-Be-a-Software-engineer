import com.example.authentication.JWTAuthenticator;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.HttpServletRequest;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

class JWTAuthenticatorTest {

    private JWTAuthenticator authenticator;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        authenticator = new JWTAuthenticator();
        request = Mockito.mock(HttpServletRequest.class);
    }

    @Test
    void testGenerateToken() {
        String token = authenticator.generateToken("user1");
        assertTrue(token != null && !token.isEmpty());
    }

    @Test
    void testAuthenticateValidJWT() {
        String token = authenticator.generateToken("user1");
        when(request.getHeader("Authorization")).thenReturn("Bearer " + token);
        assertTrue(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateExpiredJWT() {
        // Set token expiration to a past date
        String token = Jwts.builder()
                .setSubject("user1")
                .setExpiration(new Date(System.currentTimeMillis() - 1000))
                .signWith(SignatureAlgorithm.HS256, JWTAuthenticator.SECRET_KEY)
                .compact();
        when(request.getHeader("Authorization")).thenReturn("Bearer " + token);
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateInvalidJWT() {
        when(request.getHeader("Authorization")).thenReturn("Bearer invalidToken");
        assertFalse(authenticator.authenticate(request));
    }

    @Test
    void testAuthenticateMissingJWT() {
        when(request.getHeader("Authorization")).thenReturn(null);
        assertFalse(authenticator.authenticate(request));
    }

    // Optional: Test for token refresh if implemented
}
