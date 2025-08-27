package com.api.eventos.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class YearEvent {
    private int year;
    private boolean archived;
    private List<MonthEvent> months;
}
