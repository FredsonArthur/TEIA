# Atividade 10: Comparação Q-Learning vs SARSA (Maze 8x8)

Este projeto implementa e compara dois algoritmos clássicos de Aprendizado por Reforço (Reinforcement Learning) — **Q-Learning** e **SARSA** — aplicados à resolução de um labirinto determinístico 8x8 (Ambiente FrozenLake customizado da Atividade 9).

O objetivo principal é analisar como cada algoritmo converge para a solução ótima em um ambiente sem incerteza (`is_slippery=False`).

##  Descrição do Problema

O agente deve navegar de um ponto inicial (S) até um objetivo (G) em um grid 8x8, evitando buracos (H) e caminhando sobre o gelo (F).

*   **Ambiente:** FrozenLake-v1 (Gymnasium) com mapa customizado.
*   **Dinâmica:** Determinística. O agente sempre vai para a direção escolhida.
*   **Sistema de Recompensas:**
    *   **Objetivo (G):** +1.0
    *   **Buraco (H):** 0.0 (Fim do episódio)
    *   **Passo no Gelo (F):** -0.01 (Penalidade para incentivar o caminho mais curto).

##  Algoritmos Comparados

### 1. Q-Learning (Off-Policy)
O agente aprende a utilidade de uma ação baseando-se na melhor ação possível no próximo estado ($max\_Q(s', a')$), independentemente da ação que ele realmente vai tomar.
*   **Característica:** Busca a otimalidade "gananciosa" (greedy). Tende a encontrar o caminho mais curto possível, assumindo que não haverá erros.

### 2. SARSA (On-Policy)
O agente aprende baseando-se na próxima ação real que ele vai tomar ($Q(s', a')$), seguindo sua política atual (que inclui exploração aleatória).
*   **Nome:** State-Action-Reward-State-Action.
*   **Característica:** Leva em conta a sua própria política de exploração. Em ambientes perigosos (com vento ou gelo escorregadio), o SARSA costuma aprender caminhos mais seguros (longe dos buracos) do que o Q-Learning.

## ⚙️ Configuração e Hiperparâmetros

Os seguintes parâmetros foram utilizados para garantir a convergência em 100.000 episódios:

| Parâmetro | Valor | Descrição |
| :--- | :---: | :--- |
| **Episódios** | 100.000 | Total de ciclos de treinamento. |
| **Learning Rate ($\alpha$)** | 0.75 | Taxa de aprendizado (velocidade de atualização da Q-Table). |
| **Gamma ($\gamma$)** | 0.95 | Fator de desconto (importância das recompensas futuras). |
| **Epsilon ($\epsilon$)** | 1.0 $\to$ 0.01 | Taxa de exploração (cai exponencialmente). |
| **Decay Rate** | 0.00008 | Ajuste fino para manter a exploração ativa por tempo suficiente. |

## 📊 Resultados Esperados

Ao executar o código, dois resultados principais são gerados:

1.  **Gráfico de Convergência:** Mostra a evolução da recompensa média ao longo do tempo.
    *   *Expectativa:* Em um ambiente determinístico, as curvas do Q-Learning e do SARSA devem ser muito parecidas, ambas subindo e estabilizando próximas à recompensa máxima.
2.  **Avaliação (Teste Cego):** Após o treino, os agentes são testados por 100 episódios sem exploração ($\epsilon = 0$).
    *   *Conclusão Típica:* Ambos os algoritmos atingem 100% de taxa de sucesso e recompensas idênticas, provando que, sem aleatoriedade no ambiente, a política ótima é a mesma para ambos.

## 🚀 Como Executar

Certifique-se de ter as dependências instaladas:

```bash
pip install gymnasium numpy matplotlib
```

Basta executar o script Python fornecido. O script irá treinar ambos os agentes sequencialmente e exibir o gráfico comparativo ao final.