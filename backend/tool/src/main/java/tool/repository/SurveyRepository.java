package tool.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import tool.entity.Survey;
import tool.entity.Status;

import java.util.UUID;

public interface SurveyRepository extends JpaRepository<Survey, UUID> {

    Page<Survey> findByTitleContaining(String title, Pageable pageable);

    Page<Survey> findByStatus(Status status, Pageable pageable);

    Page<Survey> findByTitleContainingAndStatus(String title, Status status, Pageable pageable);
}