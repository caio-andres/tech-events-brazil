package com.api.eventos.dto;

import com.api.eventos.model.Event;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.api.eventos.model.MonthEvent;

import java.time.Month;
import java.util.ArrayList;
import java.util.List;

public record MonthEventDTO(
        @JsonProperty("mes") String mes,
        @JsonProperty("arquivado") boolean arquivado,
        @JsonProperty("eventos") List<EventDTO> eventos
) {
    public MonthEvent toDomain() {
        MonthEvent m = new MonthEvent();
        m.setMonth(parseMes(mes));  // conversão aqui
        m.setArchived(arquivado);

        List<Event> list = new ArrayList<>();
        if (eventos != null) {
            for (EventDTO e : eventos) list.add(e.toDomain());
        }
        m.setEvents(list);
        return m;
    }

    private static Month parseMes(String raw) {
        if (raw == null || raw.isBlank()) return null;
        return switch (raw.trim().toLowerCase()) {
            case "janeiro"   -> Month.JANUARY;
            case "fevereiro" -> Month.FEBRUARY;
            case "março", "marco" -> Month.MARCH;
            case "abril"     -> Month.APRIL;
            case "maio"      -> Month.MAY;
            case "junho"     -> Month.JUNE;
            case "julho"     -> Month.JULY;
            case "agosto"    -> Month.AUGUST;
            case "setembro"  -> Month.SEPTEMBER;
            case "outubro"   -> Month.OCTOBER;
            case "novembro"  -> Month.NOVEMBER;
            case "dezembro"  -> Month.DECEMBER;
            default -> throw new IllegalArgumentException("Mês inválido: " + raw);
        };
    }
}

