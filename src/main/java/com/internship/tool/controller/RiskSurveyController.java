package com.internship.tool.controller;

import com.internship.tool.entity.RiskSurvey;
import com.internship.tool.service.RiskSurveyService;

import jakarta.validation.Valid;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;

import java.util.List;
import com.internship.tool.email.EmailService;

@RestController
@RequestMapping("/api/risk-surveys")

public class RiskSurveyController {

    private final RiskSurveyService riskSurveyService;
    private final EmailService emailService;

    public RiskSurveyController(

        RiskSurveyService riskSurveyService,

        EmailService emailService

) {

    this.riskSurveyService = riskSurveyService;

    this.emailService = emailService;
}

    @GetMapping("/all")
    public ResponseEntity<Page<RiskSurvey>> getAllRiskSurveys(

            @RequestParam(defaultValue = "0") int page,

            @RequestParam(defaultValue = "5") int size

    ) {

        List<RiskSurvey> surveys = riskSurveyService.getAllRiskSurveys();

        int start = Math.min(page * size, surveys.size());

        int end = Math.min(start + size, surveys.size());

        Page<RiskSurvey> paginatedResult =
                new PageImpl<>(
                        surveys.subList(start, end),
                        PageRequest.of(page, size),
                        surveys.size()
                );

        return ResponseEntity.ok(paginatedResult);
    }

    @GetMapping("/{id}")
    public ResponseEntity<RiskSurvey> getRiskSurveyById(@PathVariable Long id) {

        RiskSurvey riskSurvey =
                riskSurveyService.getRiskSurveyById(id);

        return ResponseEntity.ok(riskSurvey);
    }

    @PostMapping("/create")
    public ResponseEntity<RiskSurvey> createRiskSurvey(

            @Valid @RequestBody RiskSurvey riskSurvey

    ) {

        RiskSurvey createdSurvey =
                riskSurveyService.createRiskSurvey(riskSurvey);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(createdSurvey);
    }
    @GetMapping("/test-email")
public String testEmail() {

    emailService.sendRiskSurveyCreatedEmail(

            "sanjanasiddu123@gmail.com",

            "Test Risk Survey"

    );

    return "Test email sent successfully";
}
@GetMapping("/test-overdue-email")
public String testOverdueEmail() {

    emailService.sendOverdueEmail(

            "sanjanasiddu123@gmail.com",

            "Pending Risk Survey"

    );

    return "Overdue email sent";
}

}