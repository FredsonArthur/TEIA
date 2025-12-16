# Atividade 9: Solução do Labirinto 8x8 Customizado (FrozenLake)

Este projeto consiste na criação e resolução de um ambiente **FrozenLake 8x8 customizado**. Diferente das atividades anteriores, aqui definimos manualmente a disposição dos buracos (H) e do caminho seguro (F), criando um labirinto determinístico que o agente deve resolver utilizando **Q-Learning**.

## O Mapa Customizado

O ambiente foi construído sobre uma matriz 8x8 específica, onde:
*   **S (Start):** Ponto de partida (0,0).
*   **G (Goal):** Objetivo (7,7).
*   **H (Hole):** Buracos que encerram o episódio (Morte).
*   **F (Frozen):** Superfície segura para caminhar.

O layout definido no código (`holes_array`) força o agente a navegar por corredores estreitos para alcançar o objetivo.

## Explicação do Código

### 1. Geração do Mapa
A função `gerar_mapa_customizado` converte uma matriz binária (numpy array) no formato de lista de strings exigido pelo Gymnasium (`desc=["SFFF...", ...]`). Isso permite desenhar qualquer labirinto facilmente editando a matriz `holes_array`.

### 2. Configuração do Ambiente
Utilizamos o `FrozenLake-v1` com `is_slippery=False`.
*   **Determinístico:** Se o agente decide ir para a direita, ele *sempre* vai para a direita. Isso simplifica o aprendizado inicial e permite focar na propagação da recompensa sem o ruído da incerteza.

### 3. O Algoritmo Q-Learning
O agente utiliza a fórmula clássica de Bellman para atualizar a Q-Table:

$$ Q(s,a) = Q(s,a) + \alpha [R + \gamma \max Q(s',a') - Q(s,a)] $$

*   **Penalidade de Passo:** Foi adicionada uma penalidade de `-0.01` a cada passo (`reward = -0.01`). Isso incentiva o agente a encontrar o **caminho mais curto**, pois quanto mais tempo ele demora, menor é sua pontuação final acumulada.

### 4. Hiperparâmetros
*   **Episódios:** 40.000 (Garante exploração suficiente para mapas complexos).
*   **Learning Rate ($\alpha$):** 0.75 (Aprendizado rápido).
*   **Gamma ($\gamma$):** 0.95 (Alto valor para focar no objetivo final distante).
*   **Epsilon Decay:** Decaimento exponencial lento para garantir que o agente explore todo o mapa antes de convergir para uma solução.

## Resultados Obtidos

Ao executar o script, o comportamento esperado é:

1.  **Fase Inicial:** O agente explora aleatoriamente e morre frequentemente nos buracos. A recompensa média é baixa ou negativa.
2.  **Descoberta:** O agente encontra o objetivo (G) pela primeira vez. A recompensa alta (+1.0) começa a ser propagada para os estados anteriores (backpropagation).
3.  **Convergência:** O gráfico de "Média Móvel de Recompensas" sobe rapidamente e se estabiliza no topo.
    *   Isso indica que o agente aprendeu a rota perfeita e não cai mais em buracos.

**Saída do Terminal:**
O código imprime a **Política Aprendida** ao final, que é uma sequência de números representando a melhor ação para cada quadrado do grid:
*   `0`: Esquerda
*   `1`: Baixo
*   `2`: Direita
*   `3`: Cima

## Como Executar

```bash
pip install gymnasium numpy matplotlib
```

Basta executar o arquivo `codigo.py`. O script exibirá o mapa no terminal, treinará o agente e plotará o gráfico de desempenho ao final.