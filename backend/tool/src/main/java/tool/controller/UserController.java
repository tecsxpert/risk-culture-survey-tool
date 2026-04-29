package tool.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import tool.dto.UserRequest;
import tool.entity.User;
import tool.service.UserService;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    // ✅ ADMIN ONLY
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public User createUser(@Valid @RequestBody UserRequest request) {

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());

        return userService.saveUser(user);
    }

    // ✅ ADMIN + MANAGER CAN VIEW USERS
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public List<User> getUsers() {
        return userService.getAllUsers();
    }
}