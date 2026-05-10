package tool.exception;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ApiException.class)
    public ResponseEntity<?> handle(ApiException ex) {

        return ResponseEntity
                .badRequest()
                .body(Map.of("error", ex.getMessage()));
    }
}