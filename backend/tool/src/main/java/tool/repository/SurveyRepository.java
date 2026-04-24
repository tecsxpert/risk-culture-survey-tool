package tool.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import tool.entity.Survey;

public interface SurveyRepository extends JpaRepository<Survey, Long> {

    // GET only active surveys
    List<Survey> findByDeletedFalse();

    // SEARCH
    List<Survey> findByTitleContainingIgnoreCaseAndDeletedFalse(String title);

    // STATS
    long countByDeletedFalse();
}