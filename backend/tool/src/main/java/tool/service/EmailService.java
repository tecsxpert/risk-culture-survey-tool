package tool.service;

import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import tool.entity.Survey;
@Service
public class EmailService {

    private final JavaMailSender mailSender;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendSurveyCreatedEmail(Survey survey) {

        SimpleMailMessage message = new SimpleMailMessage();

        message.setTo("demo@test.com");
        message.setSubject("New Survey Created");
        message.setText(
                "Title: " + survey.getTitle() +
                "\nStatus: " + survey.getStatus()
        );

        mailSender.send(message);
    }
}