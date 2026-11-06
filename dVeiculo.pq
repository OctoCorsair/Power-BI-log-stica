let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\dim_veiculo.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"veiculo_id", type text}, {"placa", type text}, {"tipo", type text}, {"marca", type text},
            {"ano_fabricacao", Int64.Type}, {"capacidade_kg", Int64.Type},
            {"consumo_nominal_kml", type number}
        },
        "en-US"
    ),
    Idade = Table.AddColumn(
        Tipos, "idade", each Date.Year(DateTime.LocalNow()) - [ano_fabricacao], Int64.Type
    ),
    Rotulo = Table.AddColumn(Idade, "veiculo_rotulo", each [placa] & " · " & [tipo], type text)
in
    Rotulo
