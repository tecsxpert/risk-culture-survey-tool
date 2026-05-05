package tool.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jakarta.validation.Valid;
import tool.dto.UserRequest;
import tool.entity.User;
import tool.service.UserService;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    // CREATE USER
    @PostMapping
    public User createUser(@Valid @RequestBody UserRequest request) {

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());

        return userService.saveUser(user);
    }

    // GET USERS
    @GetMapping
    public List<User> getUsers() {
        return userService.getAllUsers();
    }
}