package com.api.eventos.model;

import lombok.Getter;
import lombok.Setter;

import java.time.Month;
import java.util.List;

@Getter
@Setter
public class MonthEvent {
    private Month month;
    private boolean archived;
    private List<Event> events;
}
