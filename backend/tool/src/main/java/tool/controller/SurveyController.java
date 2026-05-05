package tool.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import tool.entity.Survey;
import tool.service.SurveyService;

@RestController
@RequestMapping("/surveys")
public class SurveyController {

    @Autowired
    private SurveyService surveyService;

    // CREATE SURVEY
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Survey createSurvey(@RequestBody Survey survey) {
        return surveyService.createSurvey(survey);
    }

    // GET ALL SURVEYS
    @GetMapping
    public List<Survey> getAllSurveys() {
        return surveyService.getAllSurveys();
    }

    // UPDATE SURVEY
    @PutMapping("/{id}")
    public Survey updateSurvey(
            @PathVariable Long id,
            @RequestBody Survey survey) {

        return surveyService.updateSurvey(id, survey);
    }

    // SOFT DELETE
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteSurvey(@PathVariable Long id) {
        surveyService.softDelete(id);
    }

    // SEARCH
    @GetMapping("/search")
    public List<Survey> searchSurvey(@RequestParam String q) {
        return surveyService.searchSurvey(q);
    }

    // STATS
    @GetMapping("/stats")
    public long getStats() {
        return surveyService.getSurveyStats();
    }
}