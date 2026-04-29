package tool.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import tool.entity.Survey;
import tool.service.SurveyService;

@RestController
@RequestMapping("/surveys")
public class SurveyController {

    @Autowired
    private SurveyService surveyService;

    // CREATE SURVEY
    @PostMapping
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
    public String deleteSurvey(@PathVariable Long id) {

        surveyService.softDelete(id);
        return "Survey soft deleted successfully";
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