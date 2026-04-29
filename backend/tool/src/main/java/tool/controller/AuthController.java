package tool.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import tool.dto.AuthRequest;
import tool.dto.AuthResponse;
import tool.service.AuthService;

@RestController
@RequestMapping("/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    // ✅ REGISTER USER
    @PostMapping("/register")
    public AuthResponse register(@RequestBody AuthRequest request) {

        authService.register(request);

        return new AuthResponse("User registered successfully");
    }

    // ✅ LOGIN USER
    @PostMapping("/login")
    public AuthResponse login(@RequestBody AuthRequest request) {

        String token = authService.login(request);

        return new AuthResponse(token);
    }

    // ✅ REFRESH TOKEN
    @PostMapping("/refresh")
    public AuthResponse refresh(
            @RequestHeader("Authorization") String header) {

        String token = header.replace("Bearer ", "");

        String newToken = authService.refreshToken(token);

        return new AuthResponse(newToken);
    }
}