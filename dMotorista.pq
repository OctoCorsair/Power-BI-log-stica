let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\dim_motorista.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"motorista_id", type text}, {"motorista_nome", type text}, {"categoria_cnh", type text},
            {"anos_experiencia", Int64.Type}, {"turno", type text}
        },
        "en-US"
    )
in
    Tipos
