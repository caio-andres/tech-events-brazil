package com.api.eventos.dto;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.*;
import java.io.IOException;
import java.time.LocalDate;
import java.time.Month;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.Map;

class MonthPtBrDeserializer extends JsonDeserializer<Month> {
    private static final Locale PT_BR = new Locale("pt","BR");

    @Override
    public Month deserialize(JsonParser p, DeserializationContext c) throws IOException {
        String raw = p.getValueAsString();
        if (raw == null) return null;
        String s = raw.trim().toLowerCase(PT_BR);

        Month m = getMonth(s);
        if (m != null) return m;

        try {
            var fmt = DateTimeFormatter.ofPattern("dd LLLL yyyy", PT_BR);
            return LocalDate.parse("01 " + raw + " 2000", fmt).getMonth();
        } catch (Exception e) {
            throw new JsonMappingException(p, "Mês inválido: " + raw);
        }
    }

    private static Month getMonth(String s) {
        Map<String, Month> map = Map.ofEntries(
                Map.entry("janeiro", Month.JANUARY),  Map.entry("fevereiro", Month.FEBRUARY),
                Map.entry("março", Month.MARCH),      Map.entry("marco", Month.MARCH),
                Map.entry("abril", Month.APRIL),      Map.entry("maio", Month.MAY),
                Map.entry("junho", Month.JUNE),       Map.entry("julho", Month.JULY),
                Map.entry("agosto", Month.AUGUST),    Map.entry("setembro", Month.SEPTEMBER),
                Map.entry("outubro", Month.OCTOBER),  Map.entry("novembro", Month.NOVEMBER),
                Map.entry("dezembro", Month.DECEMBER)
        );
        Month m = map.get(s);
        return m;
    }
}
