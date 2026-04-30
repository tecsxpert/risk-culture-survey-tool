package tool.aop;

import tool.entity.AuditLog;
import tool.repository.AuditLogRepository;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.aspectj.lang.*;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;
import org.springframework.security.core.context.SecurityContextHolder;

import java.time.LocalDateTime;
@Aspect
@Component
public class AuditAspect {

    private final AuditLogRepository auditLogRepository;
    private final ObjectMapper mapper = new ObjectMapper();

    public AuditAspect(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @Around("execution(* tool.service.*.create*(..)) || execution(* tool.service.*.update*(..)) || execution(* tool.service.*.delete*(..))")
    public Object audit(ProceedingJoinPoint joinPoint) throws Throwable {

        String method = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();

        Object oldObj = null;

        // BEFORE execution (best effort)
        if (method.startsWith("update") || method.startsWith("delete")) {
            oldObj = args.length > 0 ? args[0] : null;
        }

        Object result = joinPoint.proceed();

        Object newObj = null;

        if (method.startsWith("create") || method.startsWith("update")) {
            newObj = result;
        }

        AuditLog log = new AuditLog();
        log.setAction(method.toUpperCase());
        log.setEntityName(joinPoint.getTarget().getClass().getSimpleName());
        log.setOldValue(toJson(oldObj));
        log.setNewValue(toJson(newObj));
        log.setPerformedBy(getUser());
        log.setTimestamp(LocalDateTime.now());

        auditLogRepository.save(log);

        return result;
    }

    private String toJson(Object obj) {
        try {
            return mapper.writeValueAsString(obj);
        } catch (Exception e) {
            return "ERROR";
        }
    }

    private String getUser() {
        try {
            return SecurityContextHolder.getContext().getAuthentication().getName();
        } catch (Exception e) {
            return "SYSTEM";
        }
    }
}