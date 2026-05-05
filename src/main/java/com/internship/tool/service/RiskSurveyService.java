package com.internship.tool.service;

import java.util.List;

import com.internship.tool.email.EmailService;
import com.internship.tool.entity.RiskSurvey;
import com.internship.tool.exception.InvalidRiskSurveyException;
import com.internship.tool.exception.RiskSurveyNotFoundException;
import com.internship.tool.repository.RiskSurveyRepository;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.CacheEvict;

import org.springframework.stereotype.Service;

@Service
public class RiskSurveyService {

    private final RiskSurveyRepository riskSurveyRepository;

    private final EmailService emailService;

    public RiskSurveyService(

            RiskSurveyRepository riskSurveyRepository,

            EmailService emailService

    ) {

        this.riskSurveyRepository = riskSurveyRepository;

        this.emailService = emailService;
    }

    @CacheEvict(value = {"riskSurveys", "riskSurvey"}, allEntries = true)
    public RiskSurvey createRiskSurvey(RiskSurvey riskSurvey) {

        validateRiskSurvey(riskSurvey);

        RiskSurvey savedSurvey =
                riskSurveyRepository.save(riskSurvey);

        emailService.sendRiskSurveyCreatedEmail(

                "sanjanasiddu123@gmail.com",

                savedSurvey.getTitle()

        );

        return savedSurvey;
    }

    @Cacheable(value = "riskSurveys")
    public List<RiskSurvey> getAllRiskSurveys() {

        return riskSurveyRepository.findAll();
    }

    @Cacheable(value = "riskSurvey", key = "#id")
    public RiskSurvey getRiskSurveyById(Long id) {

        return riskSurveyRepository.findById(id)

                .orElseThrow(() ->

                        new RiskSurveyNotFoundException(

                                "Risk Survey not found with id: " + id
                        )
                );
    }

    private void validateRiskSurvey(RiskSurvey riskSurvey) {

        if (riskSurvey.getTitle() == null ||

                riskSurvey.getTitle().trim().isEmpty()) {

            throw new InvalidRiskSurveyException(

                    "Title cannot be empty"
            );
        }
    }

}