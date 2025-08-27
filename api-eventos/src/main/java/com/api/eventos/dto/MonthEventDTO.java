package com.api.eventos.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.api.eventos.model.MonthEvent;

import java.time.Month;
import java.util.ArrayList;
import java.util.List;

public record MonthEventDTO(
        @JsonProperty("mes") @JsonDeserialize(using = MonthPtBrDeserializer.class) Month mes,
        @JsonProperty("arquivado") boolean arquivado,
        @JsonProperty("eventos") List<EventDTO> eventos
) {
    public MonthEvent toDomain() {
        MonthEvent m = new MonthEvent();
        m.setMonth(mes);
        m.setArchived(arquivado);
        List<com.api.eventos.model.Event> list = new ArrayList<>();
        if (eventos != null) {
            for (EventDTO e : eventos) list.add(e.toDomain());
        }
        m.setEvents(list);
        return m;
    }
}