package tool.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;
import tool.entity.Task;
import tool.service.TaskService;

import java.io.IOException;

@RestController
@RequestMapping("/tasks")
public class TaskController {

    @Autowired
    private TaskService taskService;

    // ✅ PAGINATION + SORTING
    @GetMapping
    public Page<Task> getAllTasks(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir
    ) {
        return taskService.getAllTasks(page, size, sortBy, sortDir);
    }

    // ✅ CSV EXPORT ENDPOINT
    @GetMapping("/export")
    public void exportCSV(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=tasks.csv");

        taskService.exportTasksToCSV(response.getWriter());
    }
}