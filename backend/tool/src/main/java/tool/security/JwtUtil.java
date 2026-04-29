package tool.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;

@Component
public class JwtUtil {

    // ✅ 256-bit secure key
    private final SecretKey SECRET_KEY =
            Keys.secretKeyFor(SignatureAlgorithm.HS256);

    public String extractUsername(String token) {
        return extractAllClaims(token).getSubject();
    }

    public String generateToken(String username) {

        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(new Date())
                .setExpiration(
                        new Date(System.currentTimeMillis() + 1000 * 60 * 60)
                )
                .signWith(SECRET_KEY)
                .compact();
    }

    public boolean validateToken(String token, UserDetails userDetails) {

        final String username = extractUsername(token);
        return username.equals(userDetails.getUsername());
    }

    private Claims extractAllClaims(String token) {

        return Jwts.parserBuilder()
                .setSigningKey(SECRET_KEY)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}