# Modelo de dados

## Diagrama (esquema em estrela com fatos encadeados)

```text
 dCalendario ─┐
 dHub ────────┤
 dVeiculo ────┼──► fViagens ──┬──► fEntregas ◄── dCliente
 dMotorista ──┘               └──► fOcorrencias

 dMetas   (sem relacionamento: alimenta metas e semáforos)
 _Medidas (sem relacionamento: só guarda as medidas)
```

Todas as relações são **muitos-para-um**, com filtro em **uma direção** (do lado "um" para o lado "muitos").

## Relacionamentos (7)

| De (lado 1) | Para (lado *) | Ativo |
|-------------|---------------|:-----:|
| `dCalendario[Data]` | `fViagens[data_saida_data]` | ✅ |
| `dHub[hub_id]` | `fViagens[hub_id]` | ✅ |
| `dVeiculo[veiculo_id]` | `fViagens[veiculo_id]` | ✅ |
| `dMotorista[motorista_id]` | `fViagens[motorista_id]` | ✅ |
| `fViagens[viagem_id]` | `fEntregas[viagem_id]` | ✅ |
| `fViagens[viagem_id]` | `fOcorrencias[viagem_id]` | ✅ |
| `dCliente[cliente_id]` | `fEntregas[cliente_id]` | ✅ |

**Por que as entregas e ocorrências herdam os filtros da viagem?** Calendário, hub, veículo e motorista filtram `fViagens`, e `fViagens` filtra `fEntregas` e `fOcorrencias`. Isso evita caminhos ambíguos e permite o drill-through por `viagem_id` mostrar tudo da viagem. A data de uma entrega é, portanto, a **data de saída da viagem**.

**Atenção a filtros de cliente.** `dCliente` filtra só `fEntregas`. Medidas de entrega (OTIF, % no prazo, avaria, receita) respondem; medidas de viagem (custo, km, ocorrências) não. Por isso não mostre "Custo por Km" por cliente.

## Configurações no modelo

| Onde | O que fazer |
|------|-------------|
| `dCalendario` | Marcar como tabela de datas (coluna `Data`) |
| `dCalendario[Mês]` | Classificar por `MesNum` |
| `dCalendario[Mês/Ano]` | Classificar por `AnoMês` |
| `dCalendario[DiaSemana]` | Classificar por `DiaSemanaNum` |
| `dCliente[latitude]`, `[longitude]`, `dHub[...]`, `fOcorrencias[...]` | Categoria de dados: Latitude / Longitude; resumo: **Não resumir** |
| `dCliente[cidade]` / `[uf]` | Categoria: Cidade / Estado ou província |
| Colunas de chave (`*_id`, exceto `viagem_id` na `fViagens`) e `data_saida_data`, `hora_saida` | Ocultar na exibição de relatório |
| Colunas numéricas das tabelas fato (`km_real`, `carga_kg`…) | Resumo: **Não resumir** e ocultar (use as medidas) |
| `_Medidas` | Ocultar a coluna `Value` |
| Arquivo | Desativar *Data/hora automática* (Opções → Carregamento de dados) |

## Dicionário de dados

### dHub (4 linhas)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `hub_id` | texto | Chave (HUB01…) |
| `hub_nome` | texto | Nome do centro de distribuição |
| `cidade`, `uf` | texto | Localização |
| `latitude`, `longitude` | decimal | Coordenadas |
| `docas` | inteiro | Quantidade de docas |

### dCliente (120)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cliente_id` | texto | Chave |
| `cliente_nome` | texto | Nome fictício |
| `cidade`, `uf` | texto | Localização |
| `segmento` | texto | Varejo, Indústria, E-commerce, Farmacêutico, Alimentício, Autopeças |
| `prioridade` | texto | A, B ou C |
| `latitude`, `longitude` | decimal | Coordenadas |

### dVeiculo (40)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `veiculo_id` | texto | Chave |
| `placa` | texto | Placa fictícia |
| `tipo` | texto | VUC, Toco, Truck, Carreta |
| `marca` | texto | Fabricante |
| `ano_fabricacao` | inteiro | Ano |
| `capacidade_kg` | inteiro | Capacidade de carga |
| `consumo_nominal_kml` | decimal | Consumo de referência (km/L) |
| `idade` | inteiro | *Calculada na consulta M* |
| `veiculo_rotulo` | texto | *Calculada:* placa · tipo |

### dMotorista (55)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `motorista_id`, `motorista_nome` | texto | Identificação |
| `categoria_cnh` | texto | C, D ou E |
| `anos_experiencia` | inteiro | Experiência |
| `turno` | texto | Manhã, Tarde, Noite |

### dMetas (10)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `indicador` | texto | Nome do KPI (usado pelas medidas `Meta …` e `Cor …`) |
| `meta` | decimal | Valor-alvo |
| `limite_alerta` | decimal | Limite entre amarelo e vermelho |
| `melhor_quando` | texto | `maior` ou `menor` |

### fViagens (17.565 linhas, 1 por viagem)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `viagem_id` | texto | Chave |
| `data_saida`, `data_chegada` | data/hora | Saída do hub e retorno |
| `veiculo_id`, `motorista_id`, `hub_id` | texto | Chaves |
| `qtd_entregas` | inteiro | Paradas da viagem |
| `capacidade_kg`, `carga_kg` | número | Capacidade e carga transportada |
| `km_planejado`, `km_real` | decimal | Distância planejada e realizada |
| `duracao_planejada_h`, `duracao_real_h` | decimal | Duração em horas |
| `atraso_transito_min` | decimal | Atraso causado por trânsito e ocorrências na via (não inclui pane) |
| `litros_combustivel` | decimal | Diesel consumido |
| `custo_combustivel`, `custo_pedagio`, `custo_manutencao`, `custo_motorista` | moeda | Custos da viagem |
| `data_saida_data` | data | *Calculada:* chave do calendário |
| `hora_saida` | inteiro | *Calculada:* 0 a 23 |
| `faixa_horaria` | texto | *Calculada:* 00-05h, 06-08h, 09-11h, 12-16h, 17-19h, 20-23h |

### fEntregas (67.789 linhas, 1 por parada)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `entrega_id` | texto | Chave |
| `viagem_id`, `cliente_id` | texto | Chaves |
| `seq_parada` | inteiro | Ordem da parada na viagem |
| `data_hora_prevista`, `data_hora_entrega` | data/hora | Previsto e realizado |
| `atraso_min` | decimal | Realizado menos previsto, em minutos (negativo = adiantada) |
| `peso_kg`, `volumes` | número | Carga entregue |
| `valor_frete` | moeda | Receita da entrega |
| `no_prazo` | 0/1 | 1 se `atraso_min` ≤ 30 |
| `completa` | 0/1 | 1 se entregue por completo (*in full*) |
| `avaria` | 0/1 | 1 se houve dano na carga |
| `tentativas` | inteiro | 1 a 3 |
| `motivo_falha` | texto | Causa quando a entrega não foi OTIF ou teve avaria (vazio se tudo certo) |
| `faixa_atraso` | texto | *Calculada:* 1) no horário … 5) +120 min |

### fOcorrencias (4.589 linhas)
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `ocorrencia_id` | texto | Chave |
| `viagem_id` | texto | Chave |
| `data_hora` | data/hora | Momento da ocorrência |
| `tipo` | texto | Congestionamento, Obra na pista, Acidente na via, Clima adverso, Pane mecânica, Fiscalização, Bloqueio/Interdição |
| `rodovia` | texto | Via afetada |
| `duracao_min` | inteiro | Tempo parado |
| `gravidade` | texto | Baixa (<30 min), Média (<75 min), Alta |
| `custo_adicional` | moeda | Guincho/peças (pane) ou multa (fiscalização) |
| `latitude`, `longitude` | decimal | Posição aproximada |

## Definições dos KPIs

| KPI | Definição |
|-----|-----------|
| **OTIF %** | Entregas no prazo **e** completas ÷ total de entregas |
| **% No Prazo** | Entregas com atraso ≤ 30 min ÷ total |
| **% Completas** | Entregas entregues por completo ÷ total |
| **Taxa de Avaria %** | Entregas com dano ÷ total |
| **Atraso de Trânsito Médio** | Média de `atraso_transito_min` por viagem |
| **Índice de Tempo** | Horas reais ÷ horas planejadas (1,00 = sem perda; acima disso, perda de tempo) |
| **Ocorrências por 100 Viagens** | Ocorrências ÷ viagens × 100 |
| **Custo Total** | Combustível + pedágio + manutenção + motorista + custos de ocorrências |
| **Custo por Km** | Custo Total ÷ km rodados |
| **Margem %** | (Receita de frete − Custo Total) ÷ Receita de frete |
| **Utilização da Carga %** | Carga transportada ÷ capacidade dos veículos nas viagens |
