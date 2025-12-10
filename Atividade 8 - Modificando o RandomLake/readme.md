# Atividade 8 - Modificando o RandomLake

Este projeto responde à atividade sobre o impacto da estocasticidade no ambiente RandomLake e implementa uma solução para permitir o aprendizado do agente.

## 1. Análise do Problema (Por que falhou?)

**Pergunta:** "Ao desenvolver o ambiente RandomLake, foi percebido que o aprendizado do agente foi impactado pela estocasticidade da disposição dos buracos no lago. Por que isso aconteceu?"

**Resposta:** O algoritmo Q-Learning tabular assume que o ambiente é estacionário. No RandomLake, a disposição dos buracos muda a cada episódio.
*   Em um episódio, a posição X pode ser segura.
*   No próximo, a mesma posição X pode ser um buraco.

Como o agente observa apenas sua posição atual (e não o mapa inteiro), ele recebe recompensas contraditórias para o mesmo estado. A Q-Table não consegue convergir para uma política ótima porque a "melhor ação" muda aleatoriamente.

## 2. Solução Proposta

**Mudança:** Fixar o mapa (tornar o ambiente determinístico/estacionário) durante o treinamento.

Para que o agente aprenda, geramos o mapa aleatório **uma única vez** antes do início dos episódios e utilizamos esse mesmo layout durante todo o treinamento.

## 3. Implementação e Testes

O arquivo `codigo.py` executa um experimento comparativo entre as duas abordagens:

1.  **Cenário Original (RandomLake):** O mapa é recriado a cada episódio.
2.  **Cenário Proposto (FixedLake):** O mapa é fixado no início.

### Execução
```bash
pip install gymnasium numpy matplotlib
python codigo.py
```

## 4. Resultados Alcançados

O script gera um gráfico comparativo de "Recompensa Média x Episódios":

![Gráfico de Resultados](resultado.png)

*   **Versão Dinâmica (Vermelho):** O agente não aprende. A curva de recompensa permanece próxima de zero ou oscila aleatoriamente, pois o conhecimento adquirido em um mapa é inútil (ou prejudicial) no próximo.
*   **Versão Fixa (Verde):** O agente aprende com sucesso. A curva de recompensa cresce e se estabiliza, indicando que o agente memorizou o caminho seguro até o objetivo no mapa fixado.

Isso confirma que a estocasticidade da estrutura do ambiente (mudança de layout) impede o aprendizado de agentes tabulares simples que não observam a estrutura do mapa como parte do estado.