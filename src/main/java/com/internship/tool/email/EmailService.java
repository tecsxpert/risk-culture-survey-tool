package com.internship.tool.email;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;

import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;

import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

@Service
public class EmailService {

    private final JavaMailSender mailSender;
    private final TemplateEngine templateEngine;

    public EmailService(

        JavaMailSender mailSender,

        TemplateEngine templateEngine

) {

    this.mailSender = mailSender;

    this.templateEngine = templateEngine;
}

    public void sendRiskSurveyCreatedEmail(

            String toEmail,

            String surveyTitle

    ) {

        try {

            MimeMessage message =
                    mailSender.createMimeMessage();

            MimeMessageHelper helper =
                    new MimeMessageHelper(message, true);

            helper.setTo(toEmail);

            helper.setSubject("Risk Survey Created");

           Context context = new Context();

context.setVariable(

        "surveyTitle",

        surveyTitle
);

String htmlContent =

        templateEngine.process(

                "risk-survey-created",

                context
        );

helper.setText(

        htmlContent,

        true
);
            mailSender.send(message);

            System.out.println("Email sent successfully");

        } catch (MessagingException e) {

            throw new RuntimeException("Failed to send email");
        }

    }
    public void sendOverdueEmail(

        String toEmail,

        String surveyTitle

) {

    try {

        MimeMessage message =
                mailSender.createMimeMessage();

        MimeMessageHelper helper =
                new MimeMessageHelper(message, true);

        helper.setTo(toEmail);

        helper.setSubject("Risk Survey Overdue");

        Context context = new Context();

        context.setVariable(

                "surveyTitle",

                surveyTitle
        );

        String htmlContent =

                templateEngine.process(

                        "risk-survey-overdue",

                        context
                );

        helper.setText(

                htmlContent,

                true
        );

        mailSender.send(message);

        System.out.println("Overdue email sent");

    } catch (MessagingException e) {

        throw new RuntimeException(

                "Failed to send overdue email"
        );
    }

}

}