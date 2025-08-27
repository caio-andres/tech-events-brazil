package com.api.eventos.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.api.eventos.model.Schedule;

import java.util.ArrayList;
import java.util.List;

public record ScheduleDTO(
        @JsonProperty("eventos") List<YearEventDTO> eventos
) {
    public Schedule toDomain() {
        Schedule s = new Schedule();
        List<com.api.eventos.model.YearEvent> list = new ArrayList<>();
        if (eventos != null) {
            for (YearEventDTO y : eventos) list.add(y.toDomain());
        }
        s.setYears(list);
        return s;
    }
}