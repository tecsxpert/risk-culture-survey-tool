package tool.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import tool.entity.Survey;
import tool.entity.Status;
import tool.repository.SurveyRepository;

import jakarta.servlet.http.HttpServletResponse;
import java.io.PrintWriter;
import java.util.List;
import java.util.UUID;

@Service
public class SurveyService {

    private static final Logger log = LoggerFactory.getLogger(SurveyService.class);

    private final SurveyRepository surveyRepository;
    private final EmailService emailService;
    private final AuditService auditService;

    public SurveyService(SurveyRepository surveyRepository,
                         EmailService emailService,
                         AuditService auditService) {
        this.surveyRepository = surveyRepository;
        this.emailService = emailService;
        this.auditService = auditService;
    }

    // CREATE + EMAIL + AUDIT
    public Survey createSurvey(Survey survey) {

        Survey saved = surveyRepository.save(survey);

        try {
            auditService.log(
                    "SURVEY",
                    saved.getId().toString(),
                    "CREATE",
                    null,
                    "title=" + saved.getTitle() + ", status=" + saved.getStatus(),
                    "SYSTEM"
            );
        } catch (Exception e) {
            log.error("Audit failed but ignored", e);
        }

        try {
            emailService.sendSurveyCreatedEmail(saved);
        } catch (Exception e) {
            log.error("Email failed but ignored", e);
        }

        return saved;
    }

    // UPDATE STATUS + AUDIT
    public Survey updateStatus(UUID id, Status status) {

        Survey survey = surveyRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Survey not found"));

        Status oldStatus = survey.getStatus();

        survey.setStatus(status);
        Survey updated = surveyRepository.save(survey);

        try {
            auditService.log(
                    "SURVEY",
                    id.toString(),
                    "STATUS_UPDATE",
                    oldStatus.toString(),
                    status.toString(),
                    "SYSTEM"
            );
        } catch (Exception e) {
            log.error("Audit failed but ignored", e);
        }

        return updated;
    }

    // SEARCH + FILTER
    public Page<Survey> search(String q, Status status, Pageable pageable) {

        if (q != null && status != null) {
            return surveyRepository.findByTitleContainingAndStatus(q, status, pageable);
        } else if (q != null) {
            return surveyRepository.findByTitleContaining(q, pageable);
        } else if (status != null) {
            return surveyRepository.findByStatus(status, pageable);
        } else {
            return surveyRepository.findAll(pageable);
        }
    }

    // CSV EXPORT (FIXED TRY-WITH-RESOURCES)
    public void exportToCsv(HttpServletResponse response) throws Exception {

        List<Survey> surveys = surveyRepository.findAll();

        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=surveys.csv");

        try (PrintWriter writer = response.getWriter()) {

            writer.println("ID,Title,Status");

            for (Survey s : surveys) {
                writer.println(
                        s.getId() + "," +
                        escapeCsv(s.getTitle()) + "," +
                        s.getStatus()
                );
            }

            writer.flush();
        }
    }

    private String escapeCsv(String value) {
        if (value == null) return "";
        return value.replace(",", " ");
    }
}