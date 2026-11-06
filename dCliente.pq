let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\dim_cliente.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"cliente_id", type text}, {"cliente_nome", type text}, {"cidade", type text},
            {"uf", type text}, {"segmento", type text}, {"prioridade", type text},
            {"latitude", type number}, {"longitude", type number}
        },
        "en-US"
    )
in
    Tipos
