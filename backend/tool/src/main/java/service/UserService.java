package tool.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.entity.User;
import tool.repository.UserRepository;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // SAVE USER
    public User saveUser(User user) {
        return userRepository.save(user);
    }

    // GET ALL USERS
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
}