# 🚚 Dashboard Power BI: Gestão de Tráfego e Logística

Kit completo para montar, em poucas horas, um dashboard de **operação logística e tráfego rodoviário**: entregas no prazo (OTIF), ocorrências nas rodovias, desempenho da frota e custos, com metas e semáforos.

> **Sobre o arquivo `.pbix`:** ele só pode ser criado dentro do Power BI Desktop, então este kit entrega tudo o que alimenta o relatório já pronto e testado (dados, consultas, modelo, 78 medidas DAX, tema e a especificação página a página). Você monta os visuais seguindo [`docs/ESPECIFICACAO_DASHBOARD.md`](docs/ESPECIFICACAO_DASHBOARD.md); com o modelo pronto, isso leva em torno de uma hora.

## O que o dashboard responde

| Pergunta de gestão | Página |
|--------------------|--------|
| Estamos entregando no prazo e completo? Onde estão os problemas? | 1 · Visão Executiva, 2 · Entregas e SLA |
| Quando e onde o trânsito mais atrapalha a operação? | 3 · Tráfego e Ocorrências |
| Quanto custa cada km e cada entrega? Quais veículos custam mais? | 4 · Frota e Custos |
| O que aconteceu nesta viagem específica? | 5 · Detalhe da Viagem (drill-through) |

## Conteúdo do kit

```text
PowerBI-Logistica/
├── data/                  # 8 CSVs sintéticos (≈ 17,5 mil viagens, 67,8 mil entregas, 4,6 mil ocorrências)
├── powerquery/            # consultas M (uma por tabela) + parâmetro PastaDados
├── dax/
│   ├── 00_tabelas_calculadas.dax   # _Medidas e dCalendario
│   └── 01_medidas.dax              # 78 medidas organizadas em 7 grupos
├── theme/logistica-noturno.json    # tema escuro (importar no Power BI)
├── docs/
│   ├── MODELO_DE_DADOS.md          # relacionamentos e dicionário de dados
│   └── ESPECIFICACAO_DASHBOARD.md  # páginas, visuais, campos, cores e interações
└── scripts/gerar_dados.py          # regenera os dados (Python puro, sem dependências)
```

Os dados são **sintéticos** (São Paulo e arredores, jan/2025 a out/2026), com sazonalidade (Black Friday, Natal), horários de pico, chuva no verão e quebras que crescem com a idade do veículo, para que os gráficos tenham histórias reais para contar.

## Montagem passo a passo

1. **Parâmetro.** Em *Transformar dados*, crie o parâmetro `PastaDados` (texto) com o caminho da pasta `data` (ex.: `C:\PowerBI-Logistica\data`). O arquivo `powerquery/00_PastaDados.pq` mostra o código.
2. **Consultas.** Para cada arquivo `.pq`: *Nova fonte → Consulta em branco → Editor Avançado*, cole o conteúdo e **renomeie a consulta** com o nome do arquivo (`dHub`, `dCliente`, `dVeiculo`, `dMotorista`, `dMetas`, `fViagens`, `fEntregas`, `fOcorrencias`). Clique em *Fechar e aplicar*.
3. **Tabelas calculadas.** Em *Modelagem → Nova tabela*, crie `_Medidas` e `dCalendario` (arquivo `dax/00_tabelas_calculadas.dax`). Marque `dCalendario` como **tabela de datas**.
4. **Relacionamentos e propriedades.** Siga [`docs/MODELO_DE_DADOS.md`](docs/MODELO_DE_DADOS.md): 7 relacionamentos, classificação de colunas, categorias de dados (cidade, latitude, longitude) e ocultar chaves.
5. **Medidas.** Abra o modo **Consulta DAX**, cole `dax/01_medidas.dax` e clique em *Atualizar modelo com alterações*. Depois formate as medidas (inteiro, %, R$, decimal) e oculte a coluna da `_Medidas`.
6. **Tema.** *Exibir → Temas → Procurar temas* e escolha `theme/logistica-noturno.json`.
7. **Visuais.** Monte as 5 páginas com a especificação (tamanho de tela 1280 × 720).
8. **Conferência.** Compare com a tabela abaixo antes de publicar.

## Valores de conferência (sem filtros)

Se estes números baterem, o modelo e as medidas estão corretos.

| Medida | Valor |
|--------|------:|
| Viagens | 17.565 |
| Entregas | 67.789 |
| Ocorrências | 4.589 |
| Km Rodados | 10.165.441 |
| OTIF % | 87,5% |
| % No Prazo | 89,5% |
| % Completas | 97,8% |
| Taxa de Avaria % | 0,58% |
| Custo Total | R$ 32.980.782 |
| Receita de Frete | R$ 36.656.983 |
| Margem % | 10,0% |
| Custo por Km | R$ 3,24 |
| Custo por Entrega | R$ 486,52 |
| Consumo Médio (km/L) | 3,04 |
| Utilização da Carga % | 71,5% |
| Atraso de Trânsito Médio (min) | 23,7 |
| Ocorrências por 100 Viagens | 26,1 |
| Tempo Parado (h) | 3.505 |
| Velocidade Média (km/h) | 40,5 |
| Ocorrência Mais Frequente | Congestionamento |

Com o filtro **out/2026**: 935 viagens · 3.601 entregas · OTIF 88,4% · Custo por Km R$ 3,32 · Atraso de trânsito 22,1 min.
Com o filtro **Hub = CD Guarulhos**: 6.989 viagens · 26.952 entregas · OTIF 85,9% · Atraso de trânsito 27,5 min.

## Usando seus dados reais

1. Mantenha os nomes das colunas do [dicionário](docs/MODELO_DE_DADOS.md) e troque a origem nas consultas M (CSV por SQL Server, ERP, TMS, planilha…).
2. A coluna `no_prazo` já vem calculada (atraso de até 30 min = no prazo). Em produção, calcule-a na consulta a partir de `data_hora_prevista` e `data_hora_entrega` com a tolerância do seu contrato.
3. Ajuste as metas em `dim_metas.csv` (ou numa tabela do seu banco). Os semáforos mudam sem mexer em DAX.
4. Para dividir o acesso por unidade, crie funções de segurança (RLS) filtrando `dHub[hub_id]`.

## Regenerar os dados

```bash
python scripts/gerar_dados.py                                # padrão (seed 2026)
python scripts/gerar_dados.py --seed 7 --viagens-por-dia 40  # outro cenário
```

Se regenerar com outra seed ou parâmetros, os valores de conferência acima deixam de valer.

## Limites conhecidos

- O calendário vai até 31/12/2026, então meses sem dados aparecem vazios; filtre o período no segmento de datas.
- Medidas de **custo** não respondem a filtros de cliente (o custo é da viagem, não da parada), e a **margem** só faz sentido por hub, veículo, motorista, período ou viagem. A especificação indica onde usar cada uma.
- Os dados são fictícios: nomes de empresas, placas e motoristas foram gerados aleatoriamente.
