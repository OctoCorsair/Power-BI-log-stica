let
    Fonte = Csv.Document(
        File.Contents(Text.TrimEnd(PastaDados, {"\", "/"}) & "\fato_viagens.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Cabecalho,
        {
            {"viagem_id", type text}, {"data_saida", type datetime}, {"data_chegada", type datetime},
            {"veiculo_id", type text}, {"motorista_id", type text}, {"hub_id", type text},
            {"qtd_entregas", Int64.Type}, {"capacidade_kg", Int64.Type}, {"carga_kg", type number},
            {"km_planejado", type number}, {"km_real", type number},
            {"duracao_planejada_h", type number}, {"duracao_real_h", type number},
            {"atraso_transito_min", type number}, {"litros_combustivel", type number},
            {"custo_combustivel", Currency.Type}, {"custo_pedagio", Currency.Type},
            {"custo_manutencao", Currency.Type}, {"custo_motorista", Currency.Type}
        },
        "en-US"
    ),
    DataSaida = Table.AddColumn(Tipos, "data_saida_data", each DateTime.Date([data_saida]), type date),
    HoraSaida = Table.AddColumn(
        DataSaida, "hora_saida", each Time.Hour(DateTime.Time([data_saida])), Int64.Type
    ),
    FaixaHoraria = Table.AddColumn(
        HoraSaida,
        "faixa_horaria",
        each
            if [hora_saida] < 6 then "00-05h"
            else if [hora_saida] < 9 then "06-08h"
            else if [hora_saida] < 12 then "09-11h"
            else if [hora_saida] < 17 then "12-16h"
            else if [hora_saida] < 20 then "17-19h"
            else "20-23h",
        type text
    )
in
    FaixaHoraria
