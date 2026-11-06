let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\dim_metas.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"indicador", type text}, {"meta", type number},
            {"limite_alerta", type number}, {"melhor_quando", type text}
        },
        "en-US"
    )
in
    Tipos
