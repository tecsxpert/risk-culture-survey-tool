package tool.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import tool.dto.AuthRequest;
import tool.entity.Role;
import tool.entity.User;
import tool.repository.RoleRepository;
import tool.repository.UserRepository;
import tool.security.JwtUtil;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private PasswordEncoder encoder;

    @Autowired
    private JwtUtil jwtUtil;

    // ✅ REGISTER USER
    @Transactional
    public User register(AuthRequest request) {

        // check existing user
        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new RuntimeException("Email already registered");
        }

        User user = new User();

        user.setName(request.getName());
        user.setEmail(request.getEmail());

        if (request.getPassword() == null || request.getPassword().isEmpty()) {
            throw new RuntimeException("Password cannot be empty");
        }

        // hash password
        user.setPassword(encoder.encode(request.getPassword()));

        // assign VIEWER role
        Role viewerRole = roleRepository
                .findByName("VIEWER")
                .orElseThrow(() -> new RuntimeException("VIEWER role not found in DB"));

        user.setRole(viewerRole);

        return userRepository.save(user);
    }

    // ✅ LOGIN
    public String login(AuthRequest request) {

        User user = userRepository
                .findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (!encoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid password");
        }

        // generate JWT
        return jwtUtil.generateToken(user.getEmail());
    }

    // ✅ REFRESH TOKEN
    public String refreshToken(String token) {

        String email = jwtUtil.extractUsername(token);

        return jwtUtil.generateToken(email);
    }
}