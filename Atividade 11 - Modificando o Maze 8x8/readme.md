# Atividade 11: Solução do Maze 8x8 com Portas Dinâmicas

Este projeto implementa um agente de Aprendizado por Reforço (Q-Learning) capaz de resolver um labirinto 8x8 complexo que contém obstáculos dinâmicos (portas). A atividade é uma evolução do ambiente FrozenLake clássico, exigindo a criação de uma classe de ambiente personalizada e ajustes finos na função de recompensa.

O objetivo é treinar um agente para navegar do ponto S (Start) ao G (Goal), abrindo portas (P1, P2, P3) que bloqueiam o caminho.

**Desafio:** O ambiente não é estático. Uma porta começa como "parede" e se torna "chão" após a interação.

## Implementação Técnica

### 1. Ambiente Personalizado (MazeWithDoors)
Como o Gymnasium padrão não suporta alterações dinâmicas no mapa durante o episódio, foi desenvolvida uma classe Python simulando a interface do Gym (`reset` e `step`).

**Lógica das Portas:**
*   O grid utiliza o valor `2` para representar portas fechadas.
*   Quando o agente tenta mover-se para uma célula com valor `2`:
    *   O agente permanece no mesmo local (perde a vez).
    *   O valor da célula no grid muda de `2` para `0` (torna-se chão navegável).
    *   O agente recebe uma pequena recompensa (`+0.5`) pelo desbloqueio.

### 2. O Problema da Convergência ("The Suicide Trap")
Nas primeiras tentativas, observou-se que o agente convergia para uma estratégia de auto-sabotagem.

*   **Causa:** O caminho até o objetivo é longo, exigindo muitos passos para abrir as portas. Como cada passo custa `-0.01` (penalidade), o custo acumulado para chegar ao final (ex: `-0.80`) competia com a recompensa final original (`+1.0`).
*   **Consequência:** O agente "descobriu" que pular em um buraco logo no início (custo `-0.01`) era matematicamente mais vantajoso do que tentar resolver o labirinto e falhar (custo `-0.50`).

### 3. Solução: Reward Shaping (Modelagem de Recompensa)
Para corrigir a instabilidade, aplicamos a técnica de Reward Shaping, alterando drasticamente a proporção de risco/recompensa.

**Ajustes Realizados:**

| Parâmetro | Valor Antigo | Valor Novo | Justificativa |
| :--- | :---: | :---: | :--- |
| **Goal Reward** | +1.0 | +10.0 | Garante que o prêmio final supere qualquer custo acumulado de passos, eliminando a "armadilha do suicídio". |
| **Door Reward** | 0 | +0.5 | Incentivo intermediário (shaping) para encorajar a interação com objetos. |
| **Learning Rate** | 0.8 | 0.1 | Uma taxa menor evitou o "esquecimento catastrófico" após o agente encontrar o caminho. |
| **Episodes** | 10k | 20k | Aumento necessário devido à complexidade extra das portas. |

## Resultados Alcançados

O gráfico de treinamento final demonstra uma curva de aprendizado robusta:

1.  **Fase de Exploração:** O agente aprende a abrir as portas e mapear o ambiente.
2.  **Convergência Estável:** A recompensa média estabiliza próxima de `+10.0`, indicando que o agente aprendeu a rota ótima e a executa consistentemente sem cair em buracos ou loops.

## Como Executar

### Pré-requisitos

```bash
pip install gymnasium numpy matplotlib
```

### Execução
O código principal está contido no Notebook. A classe `MazeWithDoors` é autossuficiente e não depende de instalação de pacotes externos do Gym, pois é um mock environment.