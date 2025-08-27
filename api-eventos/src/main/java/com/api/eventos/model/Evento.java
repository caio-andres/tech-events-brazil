package com.api.eventos.model;

import com.api.eventos.enums.TipoEvento;

import java.util.List;

public class Evento {
    private String nome;
    private List<String> data;
    private String url;
    private String cidade;
    private String uf;
    private TipoEvento tipo;
}
