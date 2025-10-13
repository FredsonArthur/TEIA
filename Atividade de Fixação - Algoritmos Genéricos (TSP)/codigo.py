import numpy as np # pyright: ignore[reportMissingImports]

# A matriz de distâncias fornecida no PDF
# Cidades: A=0, B=1, C=2, D=3, E=4
DISTANCIA_MATRIX = np.array([
    # A   B   C   D   E
    [ 0, 20, 42, 35, 10],  # A
    [20,  0, 30, 34, 25],  # B
    [42, 30,  0, 12, 42],  # C
    [35, 34, 12,  0, 24],  # D
    [10, 25, 42, 24,  0]   # E
])

# Mapeamento de letras para índices e vice-versa (facilita o cálculo)
MAP_CIDADES_TO_IDX = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
MAP_IDX_TO_CIDADES = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

class Individuo:
    def __init__(self, cromossomo):
        """
        Cromossomo é a ordem das cidades do meio (B, C, D, E)
        Ex: 'BCDE'
        """
        self.cromossomo_meio = cromossomo # Ex: 'BCDE'
        self.rota_completa = 'A' + cromossomo + 'A' # Ex: 'ABCDEA'
        self.distancia_total = self._calcular_distancia()
        self.fitness = 1 / self.distancia_total # Inverso da distância para otimização

    def _calcular_distancia(self):
        rota = [MAP_CIDADES_TO_IDX[c] for c in self.rota_completa]
        distancia = 0
        for i in range(len(rota) - 1):
            cidade_atual = rota[i]
            proxima_cidade = rota[i+1]
            distancia += DISTANCIA_MATRIX[cidade_atual, proxima_cidade]
        return distancia

    def __repr__(self):
        return f"Rota: {self.rota_completa} | Distância: {self.distancia_total} km"
    
    def get_rota_como_lista(self):
        return list(self.cromossomo_meio)

def get_distancia_passo_a_passo(rota_completa):
    """Gera a string de cálculo para as atividades 2.1 e 2.2"""
    rota = [MAP_CIDADES_TO_IDX[c] for c in rota_completa]
    passos = []
    calculo = []
    
    for i in range(len(rota) - 1):
        cidade_origem = MAP_IDX_TO_CIDADES[rota[i]]
        cidade_destino = MAP_IDX_TO_CIDADES[rota[i+1]]
        distancia = DISTANCIA_MATRIX[rota[i], rota[i+1]]
        passos.append(f"{cidade_origem} -> {cidade_destino}: {distancia} km")
        calculo.append(str(distancia))
        
    total = sum(DISTANCIA_MATRIX[rota[i], rota[i+1]] for i in range(len(rota) - 1))
    
    calculo_str = "+".join(calculo)
    
    return "\n".join(passos), calculo_str, total

def tournament_selection(populacao, idx1, idx2):
    """Seleciona o indivíduo com menor distância entre dois índices."""
    ind1 = populacao[idx1]
    ind2 = populacao[idx2]
    
    if ind1.distancia_total <= ind2.distancia_total:
        return ind1, ind1.cromossomo_meio, idx1 + 1 # Retorna o objeto, cromossomo e ID (1-based)
    else:
        return ind2, ind2.cromossomo_meio, idx2 + 1
    
def order_crossover_ox(pai1_cromossomo, pai2_cromossomo, corte_inicio, corte_fim):
    """Implementa o Order Crossover (OX) para o TSP.
       Os índices de corte são 0-based para o cromossomo de 4 cidades."""
    
    pai1 = list(pai1_cromossomo)
    pai2 = list(pai2_cromossomo)
    n = len(pai1) # 4
    
    # --- Filho 1 (Segmento do Pai 1, preenchido com ordem do Pai 2) ---
    filho1 = [''] * n
    
    # 1. Copiar segmento do Pai 1
    segmento1 = pai1[corte_inicio:corte_fim]
    filho1[corte_inicio:corte_fim] = segmento1
    
    # 2. Cidades do Pai 2 na ordem
    cidades_pai2_ordenadas = []
    for cidade in pai2:
        if cidade not in segmento1:
            cidades_pai2_ordenadas.append(cidade)
            
    # 3. Preencher posições vazias
    idx_pai2 = 0
    for i in range(n):
        if filho1[i] == '':
            filho1[i] = cidades_pai2_ordenadas[idx_pai2]
            idx_pai2 += 1
            
    # --- Filho 2 (Segmento do Pai 2, preenchido com ordem do Pai 1) ---
    filho2 = [''] * n
    
    # 1. Copiar segmento do Pai 2
    segmento2 = pai2[corte_inicio:corte_fim]
    filho2[corte_inicio:corte_fim] = segmento2
    
    # 2. Cidades do Pai 1 na ordem
    cidades_pai1_ordenadas = []
    for cidade in pai1:
        if cidade not in segmento2:
            cidades_pai1_ordenadas.append(cidade)
            
    # 3. Preencher posições vazias
    idx_pai1 = 0
    for i in range(n):
        if filho2[i] == '':
            filho2[i] = cidades_pai1_ordenadas[idx_pai1]
            idx_pai1 += 1
            
    # Retorna o cromossomo (string)
    return "".join(filho1), "".join(filho2)

def swap_mutation(cromossomo, pos1, pos2):
    """Aplica a Mutação por Swap. Pos1 e Pos2 são 1-based (como no PDF)."""
    cromossomo_lista = list(cromossomo)
    
    # Converte para 0-based
    idx1 = pos1 - 1
    idx2 = pos2 - 1
    
    # Troca as posições
    cromossomo_lista[idx1], cromossomo_lista[idx2] = cromossomo_lista[idx2], cromossomo_lista[idx1]
    
    return "".join(cromossomo_lista)

def formatar_tabela_comparacao(geracao):
    """Calcula estatísticas para a Geração."""
    distancias = [ind.distancia_total for ind in geracao]
    
    melhor_distancia = min(distancias)
    melhor_rota_ind = [ind for ind in geracao if ind.distancia_total == melhor_distancia][0]
    
    pior_distancia = max(distancias)
    
    distancia_media = np.mean(distancias)
    
    return melhor_distancia, melhor_rota_ind.rota_completa, pior_distancia, distancia_media


def executar_simulacao():
    
    print("==========================================================================")
    print("SIMULAÇÃO DE ALGORITMO GENÉTICO PARA O PROBLEMA DO CAIXEIRO VIAJANTE (TSP)")
    print("==========================================================================")
    
    # PASSO 1: POPULAÇÃO INICIAL
    rotas_iniciais = ['BCDE', 'DEBC', 'CBED', 'EDCB']
    populacao_geracao_0 = [Individuo(rota) for rota in rotas_iniciais]
    
    print("\n[PASSO 1: POPULAÇÃO INICIAL] (Cromossomos fornecidos)")
    for i, ind in enumerate(populacao_geracao_0):
        print(f"Indivíduo {i+1} (Cromossomo: {ind.cromossomo_meio}) -> Rota: {ind.rota_completa}")

    # =================================================================================
    # PASSO 2: AVALIAÇÃO (Cálculo da Distância Total)
    print("\n\n[PASSO 2: AVALIAÇÃO] - Cálculo da Distância Total")
    
    # Atividade 2.1
    print("\n--- Atividade 2.1: Indivíduo 1 ---")
    passos_ind1, calculo_ind1, total_ind1 = get_distancia_passo_a_passo(populacao_geracao_0[0].rota_completa)
    print(f"Rota: {populacao_geracao_0[0].rota_completa}")
    print(passos_ind1)
    print(f"Total: {total_ind1} km")
    
    # Atividade 2.2
    print("\n--- Atividade 2.2: Completando a Tabela ---")
    
    # Indivíduo 1 (já fornecido como exemplo)
    # Rota: A->B->C->D->E->A. Distâncias: 20+30+12+24+10 = 96 km.
    
    # Indivíduo 2
    _, calculo_ind2, total_ind2 = get_distancia_passo_a_passo(populacao_geracao_0[1].rota_completa) # 'ADEBCA'
    # Rota: A->D->E->B->C->A. Distâncias: 35+24+25+30+42 = 156 km.
    populacao_geracao_0[1].distancia_total = total_ind2 # Atualiza o objeto
    
    # Indivíduo 3
    _, calculo_ind3, total_ind3 = get_distancia_passo_a_passo(populacao_geracao_0[2].rota_completa) # 'ACBED A'
    # Rota: A->C->B->E->D->A. Distâncias: 42+30+25+24+35 = 156 km.
    populacao_geracao_0[2].distancia_total = total_ind3
    
    # Indivíduo 4
    _, calculo_ind4, total_ind4 = get_distancia_passo_a_passo(populacao_geracao_0[3].rota_completa) # 'AEDCBA'
    # Rota: A->E->D->C->B->A. Distâncias: 10+24+12+30+20 = 96 km.
    populacao_geracao_0[3].distancia_total = total_ind4
    
    tabela_avaliacao = [
        ("1", populacao_geracao_0[0].rota_completa.replace('A', 'A->').replace('B', 'B->').replace('C', 'C->').replace('D', 'D->').replace('E', 'E->').strip('>'), calculo_ind1, total_ind1),
        ("2", populacao_geracao_0[1].rota_completa.replace('A', 'A->').replace('B', 'B->').replace('C', 'C->').replace('D', 'D->').replace('E', 'E->').strip('>'), calculo_ind2, total_ind2),
        ("3", populacao_geracao_0[2].rota_completa.replace('A', 'A->').replace('B', 'B->').replace('C', 'C->').replace('D', 'D->').replace('E', 'E->').strip('>'), calculo_ind3, total_ind3),
        ("4", populacao_geracao_0[3].rota_completa.replace('A', 'A->').replace('B', 'B->').replace('C', 'C->').replace('D', 'D->').replace('E', 'E->').strip('>'), calculo_ind4, total_ind4),
    ]

    print(f"{'Indivíduo':<10} | {'Rota Completa (Meio)':<25} | {'Cálculo das Distâncias':<30} | {'Distância Total':<15}")
    print("-" * 85)
    for ind, rota, calc, total in tabela_avaliacao:
        print(f"{ind:<10} | {rota:<25} | {calc:<30} | {total:<15} km")

    # =================================================================================
    # PASSO 3: SELEÇÃO POR TORNEIO
    print("\n\n[PASSO 3: SELEÇÃO POR TORNEIO]")

    # TORNEIO 1 (Pai 1)
    print("\n--- TORNEIO 1 (Pai 1) ---")
    pai1_ind, pai1_cromo, pai1_id = tournament_selection(populacao_geracao_0, 1, 3) # Ind 2 vs Ind 4 (indices 1 e 3)
    
    print(f"Competidores: Indivíduo 2 (Dist: {populacao_geracao_0[1].distancia_total} km) vs Indivíduo 4 (Dist: {populacao_geracao_0[3].distancia_total} km)")
    print(f"Atividade 3.1: Vencedor (Menor Distância) = Indivíduo {pai1_id} (Cromossomo: {pai1_cromo})")
    print(f"Pai 1 = Indivíduo {pai1_id} (Cromossomo: {pai1_cromo})")
    
    # TORNEIO 2 (Pai 2)
    print("\n--- TORNEIO 2 (Pai 2) ---")
    pai2_ind, pai2_cromo, pai2_id = tournament_selection(populacao_geracao_0, 0, 2) # Ind 1 vs Ind 3 (indices 0 e 2)
    
    print(f"Competidores: Indivíduo 1 (Dist: {populacao_geracao_0[0].distancia_total} km) vs Indivíduo 3 (Dist: {populacao_geracao_0[2].distancia_total} km)")
    print(f"Atividade 3.2: Vencedor (Menor Distância) = Indivíduo {pai2_id} (Cromossomo: {pai2_cromo})")
    print(f"Pai 2 = Indivíduo {pai2_id} (Cromossomo: {pai2_cromo})")
    
    casal1_pai1_cromo = pai1_cromo
    casal1_pai2_cromo = pai2_cromo
    print(f"\nCASAL 1 FORMADO: Pai 1 ({casal1_pai1_cromo}) + Pai 2 ({casal1_pai2_cromo})")
    
    # TORNEIO 3 (Pai 3)
    print("\n--- TORNEIO 3 (Pai 3) ---")
    pai3_ind, pai3_cromo, pai3_id = tournament_selection(populacao_geracao_0, 0, 1) # Ind 1 vs Ind 2 (indices 0 e 1)
    
    print(f"Competidores: Indivíduo 1 (Dist: {populacao_geracao_0[0].distancia_total} km) vs Indivíduo 2 (Dist: {populacao_geracao_0[1].distancia_total} km)")
    print(f"Atividade 3.3: Vencedor (Menor Distância) = Indivíduo {pai3_id} (Cromossomo: {pai3_cromo})")
    print(f"Pai 3 = Indivíduo {pai3_id} (Cromossomo: {pai3_cromo})")

    # TORNEIO 4 (Pai 4)
    print("\n--- TORNEIO 4 (Pai 4) ---")
    # O PDF tem um erro na Atividade 3.4 (Competidores: Indivíduo 2 vs Indivíduo 4; distâncias 3 e 4), vou seguir a ordem do sorteio 2 vs 4
    pai4_ind, pai4_cromo, pai4_id = tournament_selection(populacao_geracao_0, 1, 3) # Ind 2 vs Ind 4 (indices 1 e 3)
    
    print(f"Competidores: Indivíduo 2 (Dist: {populacao_geracao_0[1].distancia_total} km) vs Indivíduo 4 (Dist: {populacao_geracao_0[3].distancia_total} km)")
    print(f"Atividade 3.4: Vencedor (Menor Distância) = Indivíduo {pai4_id} (Cromossomo: {pai4_cromo})")
    print(f"Pai 4 = Indivíduo {pai4_id} (Cromossomo: {pai4_cromo})")

    casal2_pai3_cromo = pai3_cromo
    casal2_pai4_cromo = pai4_cromo
    print(f"\nCASAL 2 FORMADO: Pai 3 ({casal2_pai3_cromo}) + Pai 4 ({casal2_pai4_cromo})")
    
    # =================================================================================
    # PASSO 4: RECOMBINAÇÃO (Order Crossover - OX)
    print("\n\n[PASSO 4: RECOMBINAÇÃO (Order Crossover - OX)]")
    
    # Pontos de corte: Posições 2 e 3 (índices 1 e 2 em 0-based)
    corte_inicio = 1 # B C D E
    corte_fim = 3   # 0 1 2 3
    
    # Atividade 4.1: CASAL 1
    print("\n--- Atividade 4.1: CASAL 1 ---")
    filho1_cromo, filho2_cromo = order_crossover_ox(casal1_pai1_cromo, casal1_pai2_cromo, corte_inicio, corte_fim)
    
    print(f"Pai 1: {casal1_pai1_cromo} | Pai 2: {casal1_pai2_cromo}")
    
    # Passos
    print("\n* Geração Filho 1 *")
    print(f"Passo 1: Copiar segmento ({casal1_pai1_cromo[corte_inicio:corte_fim]}) do Pai 1 (posições {corte_inicio+1} e {corte_fim})")
    print(f"Filho 1 (parcial): [' ', {casal1_pai1_cromo[1]}, {casal1_pai1_cromo[2]}, ' ']")
    
    segmento1 = list(casal1_pai1_cromo[corte_inicio:corte_fim])
    cidades_pai2_ordenadas = [c for c in list(casal1_pai2_cromo) if c not in segmento1]
    
    print(f"Passo 2: Cidades do Pai 2 (em ordem) que Faltam: {cidades_pai2_ordenadas}")
    print(f"Passo 3: Preencher: {filho1_cromo}")
    print(f"Filho 1 Final (Cromossomo): {filho1_cromo}")

    print("\n* Geração Filho 2 (Invertida) *")
    print(f"Filho 2 Final (Cromossomo): {filho2_cromo}")
    
    # Atividade 4.2: CASAL 2
    print("\n--- Atividade 4.2: CASAL 2 ---")
    filho3_cromo, filho4_cromo = order_crossover_ox(casal2_pai3_cromo, casal2_pai4_cromo, corte_inicio, corte_fim)
    
    print(f"Pai 3: {casal2_pai3_cromo} | Pai 4: {casal2_pai4_cromo}")
    print(f"Filho 3 Final (Cromossomo): {filho3_cromo}")
    print(f"Filho 4 Final (Cromossomo): {filho4_cromo}")
    
    # =================================================================================
    # PASSO 5: MUTAÇÃO (Swap Mutation)
    print("\n\n[PASSO 5: MUTAÇÃO (Swap Mutation)]")
    
    filhos_antes_mutacao = [filho1_cromo, filho2_cromo, filho3_cromo, filho4_cromo]
    
    # Mutação em Filho 2 (Trocar posições 1 <-> 3)
    posicao_swap_f2 = "1<->3"
    filho2_apos_mutacao = swap_mutation(filhos_antes_mutacao[1], 1, 3)
    
    # Mutação em Filho 3 (Trocar posições 2 <-> 4)
    posicao_swap_f3 = "2<->4"
    filho3_apos_mutacao = swap_mutation(filhos_antes_mutacao[2], 2, 4)
    
    filhos_apos_mutacao = [
        filhos_antes_mutacao[0], 
        filho2_apos_mutacao, 
        filho3_apos_mutacao, 
        filhos_antes_mutacao[3]
    ]
    
    print("\n--- Atividade 5.1: Aplique as Mutações ---")
    tabela_mutacao = [
        ("1", filhos_antes_mutacao[0], "Sem mutação", filhos_apos_mutacao[0]),
        ("2", filhos_antes_mutacao[1], posicao_swap_f2, filhos_apos_mutacao[1]),
        ("3", filhos_antes_mutacao[2], posicao_swap_f3, filhos_apos_mutacao[2]),
        ("4", filhos_antes_mutacao[3], "Sem mutação", filhos_apos_mutacao[3]),
    ]
    
    print(f"{'Filho':<5} | {'Antes da Mutação':<20} | {'Posições Trocadas':<20} | {'Após Mutação':<20}")
    print("-" * 67)
    for f, antes, swap, depois in tabela_mutacao:
        print(f"{f:<5} | {antes:<20} | {swap:<20} | {depois:<20}")

    # =================================================================================
    # PASSO 6: AVALIAÇÃO DA NOVA GERAÇÃO (Geração 1)
    print("\n\n[PASSO 6: AVALIAÇÃO DA NOVA GERAÇÃO (Geração 1)]")
    
    populacao_geracao_1 = [Individuo(cromo) for cromo in filhos_apos_mutacao]

    print("\n--- Atividade 6.1: Calcule a distância de cada filho ---")
    
    tabela_avaliacao_g1 = []
    
    for i, ind in enumerate(populacao_geracao_1):
        _, calculo, total = get_distancia_passo_a_passo(ind.rota_completa)
        
        rota_display = ind.rota_completa.replace('A', 'A->').replace('B', 'B->').replace('C', 'C->').replace('D', 'D->').replace('E', 'E->').strip('->')
        
        tabela_avaliacao_g1.append((
            str(i+1),
            rota_display,
            calculo,
            total
        ))
        
    print(f"{'Filho':<5} | {'Rota Completa (Meio)':<25} | {'Cálculo':<30} | {'Distância Total':<15}")
    print("-" * 78)
    for ind, rota, calc, total in tabela_avaliacao_g1:
        print(f"{ind:<5} | {rota:<25} | {calc:<30} | {total:<15} km")
        
    # =================================================================================
    # PASSO 7: COMPARAÇÃO ENTRE GERAÇÕES
    print("\n\n[PASSO 7: COMPARAÇÃO ENTRE GERAÇÕES]")
    
    estats_g0 = formatar_tabela_comparacao(populacao_geracao_0)
    estats_g1 = formatar_tabela_comparacao(populacao_geracao_1)
    
    melhor_distancia_g0, melhor_rota_g0, pior_distancia_g0, media_g0 = estats_g0
    melhor_distancia_g1, melhor_rota_g1, pior_distancia_g1, media_g1 = estats_g1
    
    tabela_comparacao = [
        ("Melhor Distância (menor)", melhor_distancia_g0, melhor_distancia_g1),
        ("Melhor Rota", melhor_rota_g0, melhor_rota_g1),
        ("Pior Distância (maior)", pior_distancia_g0, pior_distancia_g1),
        ("Distância Média", f"{media_g0:.2f}", f"{media_g1:.2f}"),
    ]
    
    print("\n--- Atividade 7.1: Compare as estatísticas ---")
    print(f"{'Métrica':<30} | {'Geração 0':<15} | {'Geração 1':<15}")
    print("-" * 65)
    for metrica, g0, g1 in tabela_comparacao:
        print(f"{metrica:<30} | {g0:<15} | {g1:<15}")
        
    # Atividade 7.2: Análise
    print("\n--- Atividade 7.2: Análise ---")
    evoluiu = melhor_distancia_g1 < melhor_distancia_g0
    print(f"A população evoluiu? (A menor distância da Geração 1 é menor que da Geração 0?)")
    print(f"Resposta: {'SIM' if evoluiu else 'NÃO'}. A melhor distância Geração 0 foi {melhor_distancia_g0} km, e Geração 1 foi {melhor_distancia_g1} km.")
    
    melhor_geral = min(melhor_distancia_g0, melhor_distancia_g1)
    
    if melhor_geral == melhor_distancia_g0:
        rota_final = melhor_rota_g0
    else:
        rota_final = melhor_rota_g1

    print(f"\nQual foi a melhor rota encontrada até agora?")
    print(f"Rota: {rota_final}")
    print(f"Distância: {melhor_geral} km")

    # REFLEXÃO FINAL
    print("\n\n[REFLEXÃO FINAL] - Simulações e Discussões Adicionais")
    
    # Análise da Mutação (Filho 2 e 3)
    f2_antes = Individuo(filhos_antes_mutacao[1]).distancia_total
    f2_depois = populacao_geracao_1[1].distancia_total
    f3_antes = Individuo(filhos_antes_mutacao[2]).distancia_total
    f3_depois = populacao_geracao_1[2].distancia_total

    print("\nPapel da Mutação:")
    print(f"Filho 2 (Antes: {filhos_antes_mutacao[1]} | Depois: {filhos_apos_mutacao[1]})")
    print(f"Distância antes: {f2_antes} km -> depois: {f2_depois} km ({'MELHOROU' if f2_depois < f2_antes else 'PIOROU' if f2_depois > f2_antes else 'MANTEVE'})")
    print(f"Filho 3 (Antes: {filhos_antes_mutacao[2]} | Depois: {filhos_apos_mutacao[2]})")
    print(f"Distância antes: {f3_antes} km -> depois: {f3_depois} km ({'MELHOROU' if f3_depois < f3_antes else 'PIOROU' if f3_depois > f3_antes else 'MANTEVE'})")
    
    # Comparação com Força Bruta
    print("\nComparação com Força Bruta:")
    print(f"Quantas rotas possíveis existem neste problema (4 cidades para ordenar)?")
    print(f"Com 4 cidades para ordenar: 4! = 4 x 3 x 2 x 1 = {4*3*2*1} rotas")


if __name__ == "__main__":
    executar_simulacao()