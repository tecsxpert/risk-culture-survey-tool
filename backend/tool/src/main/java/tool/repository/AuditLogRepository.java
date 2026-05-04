package tool.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import tool.entity.AuditLog;

public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {
}