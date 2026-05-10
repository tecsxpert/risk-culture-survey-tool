package tool.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import tool.entity.AuditLog;
import java.util.UUID;

public interface AuditLogRepository extends JpaRepository<AuditLog, UUID> {
}