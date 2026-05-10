package com.internship.tool.repository;

import com.internship.tool.entity.RiskSurvey;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RiskSurveyRepository extends JpaRepository<RiskSurvey, Long> {

}