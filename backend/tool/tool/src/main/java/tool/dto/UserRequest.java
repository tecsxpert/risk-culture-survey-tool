package tool.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public class UserRequest {

    @NotBlank
    private String name;

    @Email
    private String email;

    // GETTERS
    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    // SETTERS
    public void setName(String name) {
        this.name = name;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}