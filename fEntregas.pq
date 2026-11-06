let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\fato_entregas.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"entrega_id", type text}, {"viagem_id", type text}, {"cliente_id", type text},
            {"seq_parada", Int64.Type}, {"data_hora_prevista", type datetime},
            {"data_hora_entrega", type datetime}, {"atraso_min", type number},
            {"peso_kg", type number}, {"volumes", Int64.Type}, {"valor_frete", Currency.Type},
            {"no_prazo", Int64.Type}, {"completa", Int64.Type}, {"avaria", Int64.Type},
            {"tentativas", Int64.Type}, {"motivo_falha", type text}
        },
        "en-US"
    ),
    FaixaAtraso = Table.AddColumn(
        Tipos,
        "faixa_atraso",
        each
            if [atraso_min] <= 0 then "1) No horário/adiantada"
            else if [atraso_min] <= 30 then "2) 1-30 min"
            else if [atraso_min] <= 60 then "3) 31-60 min"
            else if [atraso_min] <= 120 then "4) 61-120 min"
            else "5) +120 min",
        type text
    )
in
    FaixaAtraso
