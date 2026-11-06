# Especificação do dashboard

Tela **16:9 (1280 × 720)**: *Exibir → Configurações da página → Tamanho da tela*. Tema: `theme/logistica-noturno.json`. Fonte: Segoe UI.

## Padrões visuais

| Item | Regra |
|------|-------|
| Fundo da página | `#0B1626` (vem do tema) |
| Fundo dos visuais | `#13243B`, cantos arredondados, sem borda |
| Cor de destaque | Âmbar `#F5A623` |
| Semáforo | Verde `#3DD598` · Amarelo `#F5A623` · Vermelho `#E5484D` · Cinza `#8FA3BF` |
| Margens | 24 px nas laterais, 12 a 16 px entre visuais |
| Títulos | Curtos, à esquerda, escritos como pergunta ou conclusão ("OTIF por hub") |
| Rótulos | Mostrar valores só onde ajudam; remover linhas de grade |

**Semáforo nos visuais:** em *Formatar → Cores → fx → Valor do campo*, use as medidas `Cor …` do grupo 06. Nos cartões, aplique ao valor do destaque (*Callout value*).

**Cabeçalho de todas as páginas (y = 12):** título à esquerda; à direita, `Texto Período` e `Texto Atualização` (cartões de texto pequenos); abaixo, um **navegador de páginas** (*Inserir → Botões → Navegador → Navegador de páginas*).

---

## Página 1 · Visão Executiva

**Pergunta:** "Como está a operação e o que exige atenção?"

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Logística & Tráfego · Visão Executiva         Período … · Dados até …  [nav]  │
│ [Período ▭▭▭▭] [Hub ▾] [Tipo de veículo ▾]                                    │
│ ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐                  │
│ │Entregas││ OTIF % ││% Prazo ││Custo/Km││ Avaria ││Atraso  │   6 cartões KPI  │
│ └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘                  │
│ ┌─Entregas e OTIF por mês─────┐┌─OTIF por hub──┐┌─Mapa de entregas──────┐    │
│ │ colunas + linha + meta      ││ barras + meta ││ bolhas por cidade     │    │
│ └─────────────────────────────┘└───────────────┘└───────────────────────┘    │
│ ┌─Custo por Km por mês─┐┌─Principais motivos de falha─┐┌─Painel por hub────┐  │
│ │ linha + meta         ││ barras horizontais          ││ matriz com semáforo│  │
│ └──────────────────────┘└─────────────────────────────┘└───────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

| # | Visual | Posição (x, y, w × h) | Campos |
|---|--------|-----------------------|--------|
| 1 | Segmento de datas (Entre) | 24, 60, 300 × 44 | `dCalendario[Data]` |
| 2 | Segmento (lista suspensa) | 340, 60, 200 × 44 | `dHub[hub_nome]` |
| 3 | Segmento (lista suspensa) | 556, 60, 200 × 44 | `dVeiculo[tipo]` |
| 4 a 9 | **Cartões** (6), cada 192 × 96, y = 116, espaçados 16 px | | Ver tabela abaixo |
| 10 | Combinação (colunas + linhas) | 24, 224, 560 × 236 | Eixo X `dCalendario[Mês/Ano]` · Colunas `Entregas` · Linha (eixo secundário) `OTIF %` e `Meta OTIF` (tracejada) |
| 11 | Barras agrupadas | 600, 224, 300 × 236 | Eixo Y `dHub[hub_nome]` · X `OTIF %` · Cor por `Cor OTIF` · Linha constante = `Meta OTIF` |
| 12 | Mapa (bolhas) | 916, 224, 340 × 236 | Latitude/Longitude `dCliente` · Tamanho `Entregas` · Cor por `Cor OTIF` (ou saturação por `OTIF %`) · Dica: `cliente_nome`, `OTIF %` |
| 13 | Linhas | 24, 472, 380 × 236 | Eixo X `dCalendario[Mês/Ano]` · `Custo por Km` e `Meta Custo por Km` |
| 14 | Barras horizontais | 420, 472, 380 × 236 | Eixo Y `fEntregas[motivo_falha]` · X `Entregas` · **Filtro:** `motivo_falha` não está em branco · Ordenar decrescente |
| 15 | Matriz | 816, 472, 440 × 236 | Linhas `dHub[hub_nome]` · Valores `Viagens`, `Entregas`, `OTIF %`, `Atraso de Trânsito Médio (min)`, `Custo por Km` · Cor da fonte por `Cor …` |

**Cartões KPI (visual "Cartão (novo)" com rótulo de referência):**

| Cartão | Valor | Cor do destaque | Rótulo de referência |
|--------|-------|-----------------|----------------------|
| Entregas | `Entregas` | fixa (branco) | `Var. Entregas vs Mês Anterior %` |
| OTIF | `OTIF %` | `Cor OTIF` | `Var. OTIF vs Mês Anterior (p.p.)` |
| No prazo | `% No Prazo` | `Cor % No Prazo` | `Meta % No Prazo` |
| Custo por km | `Custo por Km` | `Cor Custo por Km` | `Var. Custo por Km vs Mês Anterior %` |
| Avaria | `Taxa de Avaria %` | `Cor Taxa de Avaria` | `Meta Taxa de Avaria` |
| Atraso de trânsito | `Atraso de Trânsito Médio (min)` | `Cor Atraso de Trânsito` | `Meta Atraso de Trânsito` |

> As variações "vs mês anterior" exigem que o período filtrado seja um mês. Com período livre elas mostram o deslocamento de 1 mês e podem aparecer em branco; é o comportamento esperado.

---

## Página 2 · Entregas e SLA

**Pergunta:** "Onde e por que estamos falhando com o cliente?"

| # | Visual | Campos e notas |
|---|--------|----------------|
| 1 | Segmentos | `dCalendario[Data]` (entre), `dHub[hub_nome]`, `dCliente[segmento]`, `dCliente[uf]` |
| 2 | Cartões (5) | `Entregas`, `OTIF %`, `% No Prazo`, `% Completas`, `Taxa de Avaria %` |
| 3 | **Decomposição do OTIF** (barras agrupadas, 3 barras) | Valores: `% No Prazo`, `% Completas`, `OTIF %` com a cor da série em âmbar, azul e verde; mostra que o OTIF é limitado pelo pior dos dois |
| 4 | Distribuição de atraso (colunas) | Eixo `fEntregas[faixa_atraso]` · Valor `Entregas` · cores: duas primeiras faixas verdes, demais em degradê de âmbar a vermelho |
| 5 | Pareto de motivos (barras + linha acumulada) | Eixo `motivo_falha` (sem vazios) · `Entregas` · acumulado % por *Mostrar valor como → Total acumulado* |
| 6 | OTIF por segmento (barras) | `dCliente[segmento]` × `OTIF %` com linha de `Meta OTIF` |
| 7 | OTIF por dia da semana (colunas) | `dCalendario[DiaSemana]` × `OTIF %` |
| 8 | **Tabela "Clientes em atenção"** | `dCliente[cliente_nome]`, `dCliente[cidade]`, `Entregas`, `OTIF %`, `Atraso Médio das Atrasadas (min)`, `Taxa de Avaria %` · Filtro de visual: `Entregas` ≥ 30 · Ordenar por `OTIF %` crescente · Top N = 10 pelo `OTIF %` (inferiores) · Barras de dados em `OTIF %` |
| 9 | Primeira tentativa (medidor) | `% Primeira Tentativa` |

---

## Página 3 · Tráfego e Ocorrências

**Pergunta:** "Quando e onde o trânsito mais consome a nossa operação?"

| # | Visual | Campos e notas |
|---|--------|----------------|
| 1 | Segmentos | `dCalendario[Data]`, `dHub[hub_nome]`, `fOcorrencias[tipo]`, `fOcorrencias[gravidade]` |
| 2 | Cartões (5) | `Ocorrências por 100 Viagens`, `Tempo Parado (h)`, `Atraso de Trânsito Médio (min)`, `Velocidade Média (km/h)`, `Índice de Tempo (Real/Plan)` |
| 3 | **Mapa de calor** (matriz) | Linhas `dCalendario[DiaSemana]` · Colunas `fViagens[faixa_horaria]` · Valor `Atraso de Trânsito Médio (min)` · *Cor de fundo* em escala (verde → âmbar → vermelho). Mostra os horários e dias críticos para evitar saídas |
| 4 | Ocorrências por tipo (barras) | `fOcorrencias[tipo]` × `Ocorrências` |
| 5 | **Mapa de ocorrências** | Latitude/Longitude `fOcorrencias` · Tamanho `duracao_min` (soma) · Legenda `tipo` |
| 6 | Ranking de rodovias (barras) | `fOcorrencias[rodovia]` × `Tempo Parado (h)` · Top 8 |
| 7 | Evolução mensal (linhas) | `dCalendario[Mês/Ano]` × `Atraso de Trânsito Médio (min)` e `Meta Atraso de Trânsito` · evidencia a sazonalidade de chuva (dez a mar) |
| 8 | Cartão de texto | `Ocorrência Mais Frequente` |
| 9 | Pizza/rosca de gravidade | `fOcorrencias[gravidade]` × `Ocorrências` |

**Leitura esperada nos dados de exemplo:** os picos de atraso ocorrem nas faixas 06-08h e 17-19h; o CD Guarulhos tem o maior atraso de trânsito e o CD Ribeirão Preto, o menor; congestionamento é a ocorrência mais frequente.

---

## Página 4 · Frota e Custos

**Pergunta:** "Quanto custa rodar, e onde está o desperdício?"

| # | Visual | Campos e notas |
|---|--------|----------------|
| 1 | Segmentos | `dCalendario[Data]`, `dHub[hub_nome]`, `dVeiculo[tipo]`, `dMotorista[turno]` |
| 2 | Cartões (6) | `Custo Total`, `Custo por Km`, `Custo por Entrega`, `Consumo Médio (km/L)` (cor `Cor Consumo`), `Utilização da Carga %` (cor `Cor Utilização da Carga`), `Margem %` (cor `Cor Margem`) |
| 3 | **Custo por mês por componente** (colunas empilhadas) | Eixo `dCalendario[Mês/Ano]` · Valores `Custo Combustível`, `Custo Pedágio`, `Custo Manutenção`, `Custo Motorista`, `Custo Ocorrências` |
| 4 | **Dispersão: idade × manutenção** | Detalhes `dVeiculo[placa]` · X `dVeiculo[idade]` (média) · Y `Custo de Manutenção por Km` · Tamanho `Km Rodados` · Legenda `dVeiculo[tipo]` · mostra o custo crescendo com a idade |
| 5 | Tabela de veículos | `placa`, `tipo`, `idade`, `Viagens`, `Km Rodados`, `Consumo Médio (km/L)`, `Custo por Km`, `Panes Mecânicas` · barras de dados em `Custo por Km` |
| 6 | Dispersão de motoristas | Detalhes `dMotorista[motorista_nome]` · X `Consumo Médio (km/L)` · Y `OTIF %` · Tamanho `Viagens` |
| 7 | Custo por Km por tipo de veículo (barras) | `dVeiculo[tipo]` × `Custo por Km` com linha `Meta Custo por Km` |
| 8 | Preço do diesel (linha) | `dCalendario[Mês/Ano]` × `Preço Médio do Diesel (R$/L)` |

> **Cuidado:** não use filtros ou segmentos de **cliente** nesta página (o custo é da viagem).

---

## Página 5 · Detalhe da Viagem (drill-through)

**Como configurar:** em *Drill-through*, adicione `fViagens[viagem_id]`, deixe "Manter todos os filtros" desativado e oculte a página da barra de navegação. Em qualquer visual das páginas 1 a 4 com viagens, botão direito → *Drill-through → Detalhe da Viagem*.

| # | Visual | Campos |
|---|--------|--------|
| 1 | Cartões de cabeçalho | `fViagens[viagem_id]`, `dHub[hub_nome]`, `dVeiculo[veiculo_rotulo]`, `dMotorista[motorista_nome]`, `fViagens[data_saida]` (último valor) |
| 2 | Planejado × realizado (cartões em pares) | `Km Planejados` / `Km Rodados`, duração planejada / real, `Atraso de Trânsito Médio (min)` |
| 3 | Custos (cartões) | `Custo Total`, `Custo por Km`, `Receita de Frete`, `Margem Operacional (R$)` |
| 4 | **Tabela de paradas** | `seq_parada`, `dCliente[cliente_nome]`, `data_hora_prevista`, `data_hora_entrega`, `atraso_min`, `no_prazo`, `completa`, `avaria`, `motivo_falha` · formatação condicional no `atraso_min` |
| 5 | **Linha do tempo de ocorrências** | `data_hora`, `tipo`, `rodovia`, `duracao_min`, `gravidade` |
| 6 | Mapa de ocorrências da viagem | Latitude/Longitude `fOcorrencias` |

---

## Página de dica (tooltip) opcional

Crie uma página de 320 × 240 com *Permitir uso como dica de ferramenta*. Campos: `Entregas`, `OTIF %`, `% No Prazo`, `Atraso Médio das Atrasadas (min)`. Associe aos gráficos de hub, mapa e dispersões em *Formatar → Dica de ferramenta → Tipo: Página de relatório*.

## Interações e boas práticas

- Em *Editar interações*, desative o filtro cruzado dos **cartões** sobre os demais visuais.
- Sincronize os segmentos de **período** e **hub** entre as páginas (*Exibir → Sincronizar segmentos*).
- Adicione um botão **Limpar filtros** (marcador com "Atualizar dados" desativado) no cabeçalho.
- Configure **texto alternativo** em todos os visuais e uma ordem de tabulação lógica (acessibilidade).
- **Layout para celular** (*Exibir → Layout do celular*): coloque os 6 cartões da página 1, o combo mensal e o matriz por hub.
- Mantenha no máximo **8 visuais por página** de gráficos; o excesso vai para o drill-through.

## Atualização e publicação

1. *Publicar* no workspace e configurar o **gateway** se a fonte for local.
2. Agendar a **atualização** diária (ex.: 05h, antes da operação).
3. Criar **alertas** nos cartões de OTIF e Atraso de Trânsito (Power BI Service → Gerenciar alertas) e fixar em um painel.
4. Fazer uma **assinatura** semanal por e-mail para a diretoria com a página 1.

## Checklist de qualidade

- [ ] Valores de conferência do README batem
- [ ] Nenhum visual mostra "(Em branco)" em eixo ou legenda
- [ ] Todas as medidas têm formato (%, R$, inteiro, decimal)
- [ ] Datas, cidades e coordenadas com a categoria de dados correta
- [ ] Chaves e colunas numéricas das tabelas fato ocultas
- [ ] Metas editáveis em `dMetas` e semáforos respondendo
- [ ] Drill-through funcionando a partir das páginas 1 a 4
