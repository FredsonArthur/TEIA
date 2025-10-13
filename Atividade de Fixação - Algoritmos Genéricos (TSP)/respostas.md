==========================================================================
SIMULAÇÃO DE ALGORITMO GENÉTICO PARA O PROBLEMA DO CAIXEIRO VIAJANTE (TSP)
==========================================================================

[PASSO 1: POPULAÇÃO INICIAL] (Cromossomos fornecidos)
Indivíduo 1 (Cromossomo: BCDE) -> Rota: ABCDEA
Indivíduo 2 (Cromossomo: DEBC) -> Rota: ADEBCA
Indivíduo 3 (Cromossomo: CBED) -> Rota: ACBEDA
Indivíduo 4 (Cromossomo: EDCB) -> Rota: AEDCBA


[PASSO 2: AVALIAÇÃO] - Cálculo da Distância Total

--- Atividade 2.1: Indivíduo 1 ---
Rota: ABCDEA
A -> B: 20 km
B -> C: 30 km
C -> D: 12 km
D -> E: 24 km
E -> A: 10 km
Total: 96 km

--- Atividade 2.2: Completando a Tabela ---
Indivíduo  | Rota Completa (Meio)      | Cálculo das Distâncias         | Distância Total
-------------------------------------------------------------------------------------
1          | A->B->C->D->E->A-         | 20+30+12+24+10                 | 96              km
2          | A->D->E->B->C->A-         | 35+24+25+30+42                 | 156             km
3          | A->C->B->E->D->A-         | 42+30+25+24+35                 | 156             km
4          | A->E->D->C->B->A-         | 10+24+12+30+20                 | 96              km


[PASSO 3: SELEÇÃO POR TORNEIO]

--- TORNEIO 1 (Pai 1) ---
Competidores: Indivíduo 2 (Dist: 156 km) vs Indivíduo 4 (Dist: 96 km)
Atividade 3.1: Vencedor (Menor Distância) = Indivíduo 4 (Cromossomo: EDCB)
Pai 1 = Indivíduo 4 (Cromossomo: EDCB)

--- TORNEIO 2 (Pai 2) ---
Competidores: Indivíduo 1 (Dist: 96 km) vs Indivíduo 3 (Dist: 156 km)
Atividade 3.2: Vencedor (Menor Distância) = Indivíduo 1 (Cromossomo: BCDE)
Pai 2 = Indivíduo 1 (Cromossomo: BCDE)

CASAL 1 FORMADO: Pai 1 (EDCB) + Pai 2 (BCDE)

--- TORNEIO 3 (Pai 3) ---
Competidores: Indivíduo 1 (Dist: 96 km) vs Indivíduo 2 (Dist: 156 km)
Atividade 3.3: Vencedor (Menor Distância) = Indivíduo 1 (Cromossomo: BCDE)
Pai 3 = Indivíduo 1 (Cromossomo: BCDE)

--- TORNEIO 4 (Pai 4) ---
Competidores: Indivíduo 2 (Dist: 156 km) vs Indivíduo 4 (Dist: 96 km)
Atividade 3.4: Vencedor (Menor Distância) = Indivíduo 4 (Cromossomo: EDCB)
Pai 4 = Indivíduo 4 (Cromossomo: EDCB)

CASAL 2 FORMADO: Pai 3 (BCDE) + Pai 4 (EDCB)


[PASSO 4: RECOMBINAÇÃO (Order Crossover - OX)]

--- Atividade 4.1: CASAL 1 ---
Pai 1: EDCB | Pai 2: BCDE

* Geração Filho 1 *
Passo 1: Copiar segmento (DC) do Pai 1 (posições 2 e 3)
Filho 1 (parcial): [' ', D, C, ' ']
Passo 2: Cidades do Pai 2 (em ordem) que Faltam: ['B', 'E']
Passo 3: Preencher: BDCE
Filho 1 Final (Cromossomo): BDCE

* Geração Filho 2 (Invertida) *
Filho 2 Final (Cromossomo): ECDB

--- Atividade 4.2: CASAL 2 ---
Pai 3: BCDE | Pai 4: EDCB
Filho 3 Final (Cromossomo): ECDB
Filho 4 Final (Cromossomo): BDCE


[PASSO 5: MUTAÇÃO (Swap Mutation)]

--- Atividade 5.1: Aplique as Mutações ---
Filho | Antes da Mutação     | Posições Trocadas    | Após Mutação
-------------------------------------------------------------------
1     | BDCE                 | Sem mutação          | BDCE
2     | ECDB                 | 1<->3                | DCEB
3     | ECDB                 | 2<->4                | EBDC
4     | BDCE                 | Sem mutação          | BDCE


[PASSO 6: AVALIAÇÃO DA NOVA GERAÇÃO (Geração 1)]

--- Atividade 6.1: Calcule a distância de cada filho ---
Filho | Rota Completa (Meio)      | Cálculo                        | Distância Total
------------------------------------------------------------------------------
1     | A->B->D->C->E->A          | 20+34+12+42+10                 | 118             km
2     | A->D->C->E->B->A          | 35+12+42+25+20                 | 134             km
3     | A->E->B->D->C->A          | 10+25+34+12+42                 | 123             km
4     | A->B->D->C->E->A          | 20+34+12+42+10                 | 118             km


[PASSO 7: COMPARAÇÃO ENTRE GERAÇÕES]

--- Atividade 7.1: Compare as estatísticas ---
Métrica                        | Geração 0       | Geração 1
-----------------------------------------------------------------
Melhor Distância (menor)       | 96              | 118
Melhor Rota                    | ABCDEA          | ABDCEA
Pior Distância (maior)         | 156             | 134
Distância Média                | 126.00          | 123.25

--- Atividade 7.2: Análise ---
A população evoluiu? (A menor distância da Geração 1 é menor que da Geração 0?)
Resposta: NÃO. A melhor distância Geração 0 foi 96 km, e Geração 1 foi 118 km.

Qual foi a melhor rota encontrada até agora?
Rota: ABCDEA
Distância: 96 km


[REFLEXÃO FINAL] - Simulações e Discussões Adicionais

Papel da Mutação:
Filho 2 (Antes: ECDB | Depois: DCEB)
Distância antes: 118 km -> depois: 134 km (PIOROU)
Filho 3 (Antes: ECDB | Depois: EBDC)
Distância antes: 118 km -> depois: 123 km (PIOROU)

Comparação com Força Bruta:
Quantas rotas possíveis existem neste problema (4 cidades para ordenar)?
Com 4 cidades para ordenar: 4! = 4 x 3 x 2 x 1 = 24 rotas