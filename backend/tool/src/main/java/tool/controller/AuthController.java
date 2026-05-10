package tool.controller;

import org.springframework.web.bind.annotation.*;

import tool.entity.User;
import tool.service.AuthService;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public String register(@RequestParam String name,
                           @RequestParam String email,
                           @RequestParam String password) {

        User user = authService.register(name, email, password);

        return "User Registered Successfully : " + user.getEmail();
    }
}