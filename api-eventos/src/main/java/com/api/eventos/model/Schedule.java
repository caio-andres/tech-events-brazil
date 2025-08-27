package com.api.eventos.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class Schedule {
    private List<YearEvent> years;
}
