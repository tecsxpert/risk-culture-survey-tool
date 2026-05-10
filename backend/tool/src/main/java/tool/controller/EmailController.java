package tool.controller;

import java.util.UUID;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import tool.entity.Status;
import tool.entity.Survey;
import tool.service.EmailService;

@RestController
@RequestMapping("/api/email")
public class EmailController {

    private final EmailService emailService;

    public EmailController(EmailService emailService) {
        this.emailService = emailService;
    }

    @GetMapping("/test")
    public String sendTestEmail() {

        Survey survey = new Survey();

        // simulate saved survey
        survey.setId(UUID.randomUUID());

        survey.setTitle("Risk Culture Survey");
        survey.setStatus(Status.OPEN);

        emailService.sendSurveyCreatedEmail(survey);

        return "✅ Email sent successfully!";
    }
}