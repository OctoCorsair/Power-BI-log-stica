let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\fato_ocorrencias.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"ocorrencia_id", type text}, {"viagem_id", type text}, {"data_hora", type datetime},
            {"tipo", type text}, {"rodovia", type text}, {"duracao_min", Int64.Type},
            {"gravidade", type text}, {"custo_adicional", Currency.Type},
            {"latitude", type number}, {"longitude", type number}
        },
        "en-US"
    )
in
    Tipos
