package tool.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;

import tool.entity.Task;
import tool.repository.TaskRepository;

import java.io.PrintWriter;
import java.util.List;

@Service
public class TaskService {

    @Autowired
    private TaskRepository taskRepository;

    // ✅ PAGINATION LOGIC
    public Page<Task> getAllTasks(int page, int size, String sortBy, String sortDir) {

        Sort sort = sortDir.equalsIgnoreCase("desc")
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();

        Pageable pageable = PageRequest.of(page, size, sort);

        return taskRepository.findAll(pageable);
    }

    // ✅ CSV EXPORT METHOD (FIX for your error)
    public void exportTasksToCSV(PrintWriter writer) {

        List<Task> tasks = taskRepository.findAll();

        // header row
        writer.println("id,title,description,dueDate,completed");

        // data rows
        for (Task task : tasks) {
            writer.println(
                    task.getId() + "," +
                    task.getTitle() + "," +
                    task.getDescription() + "," +
                    task.getDueDate() + "," +
                    task.isCompleted()
            );
        }
    }
}