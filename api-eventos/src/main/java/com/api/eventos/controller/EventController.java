package com.api.eventos.controller;

import com.api.eventos.model.MonthEvent;
import com.api.eventos.service.EventService;
import org.springframework.web.bind.annotation.*;

import java.time.Month;
import java.util.List;

@RestController
@RequestMapping("/api/event")
public class EventController {

    private final EventService eventService;

    public EventController(EventService eventService) {
        this.eventService = eventService;
    }

    @GetMapping("/months")
    public List<MonthEvent> getByMonth(
            @RequestParam(name = "init_month") Month init_month,
            @RequestParam(name = "finish_month") Month finish_month
    ) {
        return eventService.filterMonths(init_month, finish_month);
    }


}
