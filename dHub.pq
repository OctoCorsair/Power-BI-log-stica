let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\dim_hub.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"hub_id", type text}, {"hub_nome", type text}, {"cidade", type text}, {"uf", type text},
            {"latitude", type number}, {"longitude", type number}, {"docas", Int64.Type}
        },
        "en-US"
    )
in
    Tipos
