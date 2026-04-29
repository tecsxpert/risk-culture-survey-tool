package tool.scheduler;

import tool.entity.Task;
import tool.repository.TaskRepository;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class ReminderScheduler {

    private final TaskRepository taskRepository;

    public ReminderScheduler(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Scheduled(cron = "0/30 * * * * ?")
    public void sendOverdueReminders() {

        LocalDate today = LocalDate.now();

        List<Task> overdueTasks =
                taskRepository.findByCompletedFalseAndDueDateBefore(today);

        System.out.println("\n=== OVERDUE TASK REMINDER ===");

        if (overdueTasks.isEmpty()) {
            System.out.println("No overdue tasks 🎉");
            return;
        }

        for (Task task : overdueTasks) {
            System.out.println("OVERDUE: " + task.getTitle()
                    + " (Was due: " + task.getDueDate() + ")");
        }
    }

    @Scheduled(cron = "0/30 * * * * ?")
    public void sendUpcomingDeadlineAlerts() {

        LocalDate today = LocalDate.now();
        LocalDate nextWeek = today.plusDays(7);

        List<Task> upcomingTasks =
                taskRepository.findByCompletedFalseAndDueDateBetween(today, nextWeek);

        System.out.println("\n=== UPCOMING DEADLINES ===");

        if (upcomingTasks.isEmpty()) {
            System.out.println("No upcoming tasks in next 7 days.");
            return;
        }

        for (Task task : upcomingTasks) {
            System.out.println("UPCOMING: " + task.getTitle()
                    + " (Due: " + task.getDueDate() + ")");
        }
    }

    @Scheduled(cron = "0 0 9 * * MON")
    public void weeklySummary() {

        LocalDate today = LocalDate.now();
        LocalDate nextWeek = today.plusDays(7);

        List<Task> allTasks =
                taskRepository.findByDueDateBetween(today, nextWeek);

        long completed = allTasks.stream()
                .filter(Task::isCompleted)
                .count();

        long pending = allTasks.stream()
                .filter(t -> !t.isCompleted())
                .count();

        System.out.println("\n=== WEEKLY SUMMARY REPORT ===");
        System.out.println("Total Tasks (This Week): " + allTasks.size());
        System.out.println("Completed Tasks: " + completed);
        System.out.println("Pending Tasks: " + pending);
    }
}