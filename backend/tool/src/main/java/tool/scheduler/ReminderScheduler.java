package tool.scheduler;

import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import tool.repository.SurveyRepository;

@Component
@RequiredArgsConstructor
public class ReminderScheduler {

    private final SurveyRepository repo;

    @Scheduled(cron="0 0 9 * * *")
    public void dailyReminder(){
        System.out.println("Checking overdue surveys: "
                + repo.count());
    }
}