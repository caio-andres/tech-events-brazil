package com.api.eventos.model;

import com.api.eventos.enums.EventType;
import com.api.eventos.enums.UF;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class Event {
    private String name;
    private List<String> data;
    private String url;
    private String city;
    private UF uf;
    private EventType eventType;
}
