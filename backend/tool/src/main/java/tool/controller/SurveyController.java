package tool.controller;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;
import tool.entity.Survey;
import tool.entity.Status;
import tool.service.SurveyService;

import java.util.UUID;

@RestController
@RequestMapping("/surveys")
public class SurveyController {

    private final SurveyService service;

    public SurveyController(SurveyService service) {
        this.service = service;
    }

    // CREATE
    @PostMapping
    public Survey create(@RequestBody Survey survey) {
        return service.createSurvey(survey);
    }

    // UPDATE STATUS
    @PutMapping("/{id}/status")
    public Survey updateStatus(
            @PathVariable UUID id,
            @RequestParam Status status) {

        return service.updateStatus(id, status);
    }

    // LIST + SEARCH + FILTER
    @GetMapping
    public Page<Survey> list(
            @RequestParam(required = false) String q,
            @RequestParam(required = false) Status status,
            Pageable pageable) {

        return service.search(q, status, pageable);
    }
}