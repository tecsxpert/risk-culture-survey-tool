package tool.controller;

import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;

import tool.repository.SurveyRepository;
import tool.entity.Survey;

import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

@RestController
@RequestMapping("/export")
public class ExportController {

    private final SurveyRepository surveyRepository;

    public ExportController(SurveyRepository surveyRepository) {
        this.surveyRepository = surveyRepository;
    }

    @GetMapping("/csv")
    public void export(HttpServletResponse response) throws Exception {

        // ✅ Excel-friendly headers
        response.setContentType("text/csv; charset=UTF-8");
        response.setCharacterEncoding("UTF-8");
        response.setHeader("Content-Disposition",
                "attachment; filename=surveys.csv");

        PrintWriter writer = response.getWriter();

        // ✅ CSV Header
        writer.println("ID,Title,Status");

        for (Survey s : surveyRepository.findAll()) {

            String id = safe(s.getId());
            String title = safe(s.getTitle());
            String status = safe(s.getStatus());

            writer.println(id + "," + title + "," + status);
        }

        writer.flush();
        writer.close();
    }

    // ✅ Safe null + Excel-safe formatting
    private String safe(Object value) {
        if (value == null) return "";

        String str = value.toString().trim();

        // Optional: prevent CSV breaking if commas exist
        if (str.contains(",")) {
            str = "\"" + str + "\"";
        }

        return str;
    }
}