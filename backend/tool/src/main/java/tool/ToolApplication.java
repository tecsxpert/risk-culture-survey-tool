package tool;

import java.util.TimeZone;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ToolApplication {

    public static void main(String[] args) {

        // ✅ FORCE CORRECT TIMEZONE
        TimeZone.setDefault(TimeZone.getTimeZone("Asia/Kolkata"));

        SpringApplication.run(ToolApplication.class, args);
    }
}