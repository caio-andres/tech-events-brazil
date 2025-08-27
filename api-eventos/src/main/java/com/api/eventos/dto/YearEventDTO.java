package com.api.eventos.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.api.eventos.model.YearEvent;

import java.util.ArrayList;
import java.util.List;

public record YearEventDTO(
        @JsonProperty("ano") int ano,
        @JsonProperty("arquivado") boolean arquivado,
        @JsonProperty("meses") List<MonthEventDTO> meses
) {
    public YearEvent toDomain() {
        YearEvent y = new YearEvent();
        y.setYear(ano);
        y.setArchived(arquivado);
        List<com.api.eventos.model.MonthEvent> list = new ArrayList<>();
        if (meses != null) {
            for (MonthEventDTO m : meses) list.add(m.toDomain());
        }
        y.setMonths(list);
        return y;
    }
}