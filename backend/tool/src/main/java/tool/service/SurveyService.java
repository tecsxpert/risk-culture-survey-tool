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

    // CREATE
    public Survey createSurvey(Survey survey) {
        return surveyRepository.save(survey);
    }

    // GET ALL ACTIVE
    public List<Survey> getAllSurveys() {
        return surveyRepository.findByDeletedFalse();
    }

    // UPDATE
    public Survey updateSurvey(Long id, Survey updatedSurvey) {

        Survey survey = surveyRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Survey not found"));

        survey.setTitle(updatedSurvey.getTitle());
        survey.setDescription(updatedSurvey.getDescription());

        return surveyRepository.save(survey);
    }

    // SOFT DELETE
    public void softDelete(Long id) {

        Survey survey = surveyRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Survey not found"));

        survey.setDeleted(true);
        surveyRepository.save(survey);
    }

    // SEARCH
    public List<Survey> searchSurvey(String query) {
        return surveyRepository
                .findByTitleContainingIgnoreCaseAndDeletedFalse(query);
    }

    // STATS
    public long getSurveyStats() {
        return surveyRepository.countByDeletedFalse();
    }
}