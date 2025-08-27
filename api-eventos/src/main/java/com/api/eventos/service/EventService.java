package com.api.eventos.service;

import com.api.eventos.dto.ScheduleDTO;
import com.api.eventos.model.MonthEvent;
import com.api.eventos.model.Schedule;
import com.api.eventos.model.YearEvent;
import kong.unirest.Unirest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.time.Month;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class EventService {

    @Value("${url.database}")
    private String urlDatabase;

    private Schedule schedule;

    @PostConstruct
    public void init() {
        this.schedule = fetchSchedule();
    }

    public Schedule fetchSchedule() {
        ScheduleDTO dto = Unirest.get(urlDatabase)
                .asObject(ScheduleDTO.class)
                .getBody();
        return dto.toDomain();
    }

    public List<MonthEvent> filterMonths(Month start, Month end) {
        List<MonthEvent> result = new ArrayList<>();

        for (YearEvent year : schedule.getYears()) {
            if (year.isArchived()) continue;

            List<MonthEvent> months = year.getMonths().stream()
                    .filter(m -> !m.isArchived())
                    .filter(m -> isBetween(m.getMonth(), start, end))
                    .toList();

            result.addAll(months);
        }

        return result;
    }

    private boolean isBetween(Month target, Month start, Month end) {
        int t = target.getValue();
        int s = start.getValue();
        int e = end.getValue();
        return t >= s && t <= e;
    }
}