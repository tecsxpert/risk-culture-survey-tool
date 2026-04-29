package tool.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.entity.Survey;
import tool.repository.SurveyRepository;

@Service
public class SurveyService {

    @Autowired
    private SurveyRepository surveyRepository;

    // ✅ CREATE SURVEY
    public Survey createSurvey(Survey survey) {

        if (survey == null) {
            throw new IllegalArgumentException("Survey cannot be null");
        }

        return surveyRepository.save(survey);
    }

    // ✅ GET ALL ACTIVE SURVEYS
    public List<Survey> getAllSurveys() {
        return surveyRepository.findByDeletedFalse();
    }

    // ✅ UPDATE SURVEY
    public Survey updateSurvey(Long id, Survey updatedSurvey) {

        if (id == null) {
            throw new IllegalArgumentException("Survey id cannot be null");
        }

        if (updatedSurvey == null) {
            throw new IllegalArgumentException("Updated survey cannot be null");
        }

        Survey survey = surveyRepository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException("Survey not found"));

        survey.setTitle(updatedSurvey.getTitle());
        survey.setDescription(updatedSurvey.getDescription());

        return surveyRepository.save(survey);
    }

    // ✅ SOFT DELETE SURVEY
    public void softDelete(Long id) {

        if (id == null) {
            throw new IllegalArgumentException("Survey id cannot be null");
        }

        Survey survey = surveyRepository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException("Survey not found"));

        survey.setDeleted(true);

        surveyRepository.save(survey);
    }

    // ✅ SEARCH SURVEY
    public List<Survey> searchSurvey(String query) {

        if (query == null || query.isBlank()) {
            return getAllSurveys();
        }

        return surveyRepository
                .findByTitleContainingIgnoreCaseAndDeletedFalse(query);
    }

    // ✅ SURVEY STATISTICS
    public long getSurveyStats() {
        return surveyRepository.countByDeletedFalse();
    }
}