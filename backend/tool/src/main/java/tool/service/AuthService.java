package tool.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
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

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    // ✅ REGISTER
    @Transactional
    public User register(AuthRequest request) {

        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new RuntimeException("Email already registered");
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(encoder.encode(request.getPassword()));

        Role role = roleRepository.findByName("VIEWER")
                .orElseThrow(() -> new RuntimeException("VIEWER role not found"));

        user.setRole(role);

        return userRepository.save(user);
    }

    // ✅ LOGIN (FIXED)
    public String login(AuthRequest request) {

        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (!encoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid password");
        }

        // convert to UserDetails (IMPORTANT FIX)
        UserDetails userDetails =
                customUserDetailsService.loadUserByUsername(user.getEmail());

        return jwtUtil.generateToken(userDetails);
    }

    // ✅ REFRESH TOKEN (FIXED)
    public String refreshToken(String token) {

        String email = jwtUtil.extractUsername(token);

        UserDetails userDetails =
                customUserDetailsService.loadUserByUsername(email);

        return jwtUtil.generateToken(userDetails);
    }
}