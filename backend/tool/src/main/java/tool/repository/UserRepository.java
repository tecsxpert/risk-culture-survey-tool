package tool.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import tool.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // ✅ REQUIRED FOR LOGIN
    Optional<User> findByEmail(String email);
}