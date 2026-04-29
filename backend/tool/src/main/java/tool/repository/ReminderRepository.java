package tool.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import tool.entity.Reminder;

public interface ReminderRepository extends JpaRepository<Reminder, Long> {
}