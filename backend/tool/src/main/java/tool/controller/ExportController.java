package tool.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;

import tool.repository.SurveyRepository;
import tool.entity.Survey;

import java.io.PrintWriter;

@RestController
@RequiredArgsConstructor
@RequestMapping("/export")
public class ExportController {

    private final SurveyRepository repo;

    @GetMapping("/csv")
    public void export(HttpServletResponse response) throws Exception {

        response.setContentType("text/csv");
        response.setHeader("Content-Disposition",
                "attachment; filename=survey.csv");

        PrintWriter writer = response.getWriter();

        writer.println("ID,Title,Status");

        for(Survey s : repo.findAll()){
            writer.println(
                s.getId()+","+
                s.getTitle()+","+
                s.getStatus());
        }

        writer.flush();
    }
}