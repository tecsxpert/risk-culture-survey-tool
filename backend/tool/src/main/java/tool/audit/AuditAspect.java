package tool.audit;

import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class AuditAspect {

    private static final Logger log =
            LoggerFactory.getLogger(AuditAspect.class);

    @Before("execution(* tool.service.*.*(..))")
    public void auditLog() {
        log.info("AUDIT LOG -> Service method executed");
    }
}