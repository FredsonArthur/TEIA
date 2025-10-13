Erro ao carregar os dados TSP (após ignorar SSL): Expecting value: line 1 column 1 (char 0)
Usando matriz de fallback (5 cidades: A, B, C, D, E).

--- TESTE DE PREPARAÇÃO TSP/AG ---
Matriz de Distâncias carregada. Número de cidades: 5 (índices 0 a 4)
Cidades Intermediárias esperadas: [1, 2, 3, 4]

--- TESTE DE VALIDAÇÃO DE ROTAS ---
Rota [1, 2, 3, 4]: True - Rota válida.
Rota [1, 1, 3, 4]: False - Cidades repetidas ou faltando.
Rota [1, 2, 3]: False - Tamanho incorreto: Esperado 4, Encontrado 3.

--- TESTE DE CÁLCULO DE FITNESS (DISTÂNCIA) ---
Cromossomo: [1 2 3 4] | Rota: [0, np.int64(1), np.int64(2), np.int64(3), np.int64(4), 0] | Distância: 96.00 km | Fitness (1/D): 0.01042 | Status: Válido
Cromossomo: [1 1 3 4] | Rota: [0, np.int64(1), np.int64(1), np.int64(3), np.int64(4), 0] | Distância: inf km | Fitness (1/D): 0.00000 | Status: INVÁLIDO: Cidades repetidas ou faltando.

Cálculo Exemplo (0 -> 1):
Distância 0 -> 1: 20
Distância 4 -> 0: 10
Distância Total da rota ordenada (0-1-2-3-4-0): 96.00 km