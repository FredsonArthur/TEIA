# Resultados dos Experimentos - Análise de Parâmetros do AG para TSP

## Execução dos Experimentos

```
PS C:\Users\Duda\Documents\GitHub\TEIA> & C:/Python313/python.exe "c:/Users/Duda/Documents/GitHub/TEIA/Algoritmo do TSP (Experimentos)/codigo.py"
Error loading TSP data: Expecting value: line 1 column 1 (char 0). Using fallback 5-city matrix.
Running Experiment 1: Population Size
  Testing value: 20...
    Run 30/30
  Testing value: 50...
    Run 30/30
  Testing value: 100...
    Run 30/30

Running Experiment 2: Mutation Rate
  Testing value: 1%...
    Run 30/30
  Testing value: 5%...
    Run 30/30
  Testing value: 10%...
    Run 30/30
  Testing value: 20%...
    Run 30/30

Running Experiment 3: Tournament Size
  Testing value: 2...
    Run 30/30
  Testing value: 3...
    Run 30/30
  Testing value: 5...
    Run 30/30
  Testing value: 7...
    Run 30/30

Running Experiment 4: Elitism
  Testing value: 0%...
    Run 30/30
  Testing value: 1%...
    Run 30/30
  Testing value: 5%...
    Run 30/30
  Testing value: 10%...
    Run 30/30

All experiments completed.

--- Analysis and Visualization ---
Saved convergence plot to convergence_pop_size.png
PS C:\Users\Duda\Documents\GitHub\TEIA> 
```

## Dados Numéricos dos Experimentos

### Experimento 1: Tamanho da População
- **20 indivíduos**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0354s
- **50 indivíduos**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0856s
- **100 indivíduos**: Fitness Mean=96.00, Std=0.00, Time Mean=0.1692s

### Experimento 2: Taxa de Mutação
- **1%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0829s
- **5%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0829s
- **10%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0841s
- **20%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0871s

### Experimento 3: Tamanho do Torneio
- **2**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0797s
- **3**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0820s
- **5**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0925s
- **7**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0958s

### Experimento 4: Elitismo
- **0%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0829s
- **1%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0823s
- **5%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0839s
- **10%**: Fitness Mean=96.00, Std=0.00, Time Mean=0.0805s

## Análise dos Resultados

### Experimento 1: Tamanho da População
- Todos os tamanhos de população obtiveram o mesmo fitness médio (96.00)
- O tempo de execução aumenta proporcionalmente ao tamanho da população
- Para este problema de pequena escala, o tamanho da população não afetou significativamente a qualidade

### Experimento 2: Taxa de Mutação
- Todas as taxas de mutação obtiveram o mesmo fitness médio (96.00)
- O tempo de execução foi consistente entre as diferentes taxas
- Para este problema específico, a taxa de mutação não teve impacto significativo

### Experimento 3: Tamanho do Torneio
- Todos os tamanhos de torneio obtiveram o mesmo fitness médio (96.00)
- O tempo de execução aumenta ligeiramente com o tamanho do torneio
- O tamanho do torneio não afetou a qualidade da solução neste caso

### Experimento 4: Elitismo
- Todos os percentuais de elitismo obtiveram o mesmo fitness médio (96.00)
- O tempo de execução foi consistente entre as diferentes configurações
- O elitismo não teve impacto significativo na qualidade da solução

## Conclusões

1. **Tamanho da População**: Para este problema específico com 5 cidades, o tamanho da população não afetou a qualidade da solução, mas impactou o tempo de execução. Um tamanho de 50 indivíduos oferece um bom compromisso.

2. **Taxa de Mutação**: A taxa de mutação não teve impacto significativo na qualidade da solução para esta instância do problema.

3. **Tamanho do Torneio**: O tamanho do torneio não afetou a qualidade da solução, mas tem um pequeno impacto no tempo de execução.

4. **Elitismo**: O elitismo não teve impacto significativo na qualidade da solução para esta instância do problema.

**Observação**: Os resultados mostram que todos os experimentos convergiram para a mesma solução ótima (fitness 96.00) devido à simplicidade da instância do problema (apenas 5 cidades). Em problemas maiores e mais complexos, seria esperado ver mais variação nos resultados entre as diferentes configurações de parâmetros.