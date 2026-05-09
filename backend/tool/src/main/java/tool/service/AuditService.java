package tool.service;

import org.springframework.stereotype.Service;
import tool.entity.AuditLog;
import tool.repository.AuditLogRepository;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    public AuditService(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    public void log(String entityType,
                    String entityId,
                    String action,
                    String oldValue,
                    String newValue,
                    String performedBy) {

        AuditLog log = new AuditLog();

        log.setId(UUID.randomUUID());
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setAction(action);
        log.setOldValue(oldValue);
        log.setNewValue(newValue);
        log.setPerformedBy(performedBy);
        log.setCreatedAt(LocalDateTime.now());

        auditLogRepository.save(log);
    }
}