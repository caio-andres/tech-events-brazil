package com.api.eventos.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.api.eventos.enums.EventType;
import com.api.eventos.enums.UF;
import com.api.eventos.model.Event;

import java.util.List;
import java.util.Locale;

public record EventDTO(
        @JsonProperty("nome")   String nome,
        @JsonProperty("data")   List<String> data,
        @JsonProperty("url")    String url,
        @JsonProperty("cidade") String cidade,
        @JsonProperty("uf")     String uf,
        @JsonProperty("tipo")   String tipo
) {
    public Event toDomain() {
        Event e = new Event();
        e.setName(nome);
        e.setData(data);
        e.setUrl(url);
        e.setCity(cidade);
        e.setUf(parseUf(uf));
        e.setEventType(parseEventType(tipo));
        return e;
    }

    private static UF parseUf(String raw) {
        if (raw == null || raw.isBlank()) return null;
        String code = raw.trim().toUpperCase(Locale.ROOT);
        try { return UF.valueOf(code); } catch (IllegalArgumentException ex) { return null; }
    }

    private static EventType parseEventType(String raw) {
        if (raw == null || raw.isBlank()) return null;
        String n = raw.trim().toLowerCase(Locale.ROOT);
        if (n.startsWith("onli")) return EventType.ONLINE;
        if (n.startsWith("presen")) return EventType.PRESENCIAL;
        if (n.startsWith("hibr") || n.startsWith("híbr")) return EventType.HIBRIDO;
        try { return EventType.valueOf(n.toUpperCase(Locale.ROOT)); } catch (IllegalArgumentException ex) { return null; }
    }
}
