import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÃO DO MAPA 8x8 (Atividade 9) ---
# O Mapa Complexo Determinístico 8x8 da Atividade 9
holes_array = np.array([
    [0, 0, 0, 0, 0, 1, 0, 0], 
    [0, 1, 1, 1, 0, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 1, 0, 1, 1, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 1, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 0, 1, 1, 0, 1, 0]   
])
def gerar_mapa_customizado(layout):
    desc = []
    rows, cols = layout.shape
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if r == 0 and c == 0: row_str += "S" 
            elif r == rows-1 and c == cols-1: row_str += "G" 
            elif layout[r][c] == 1: row_str += "H" 
            else: row_str += "F" 
        desc.append(row_str)
    return desc

mapa_8x8 = gerar_mapa_customizado(holes_array)

# --- 2. PARÂMETROS DE COMPARAÇÃO (Corrigidos) ---
TOTAL_EPISODES = 100000 
MAX_STEPS = 500         
LEARNING_RATE = 0.75    # alpha
GAMMA = 0.95            # gamma
MAX_EPSILON = 1.0
MIN_EPSILON = 0.01
# CORRIGIDO: Aumentado para 0.00008 para convergência em 100.000 episódios
DECAY_RATE = 0.00008   

WINDOW_SIZE = 500 

# Função auxiliar para calcular a média móvel
def moving_average(data, window_size=WINDOW_SIZE):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Função auxiliar para selecionar a ação (Epsilon-Greedy)
def select_action(qtable, state, epsilon, action_space):
    if np.random.uniform(0, 1) > epsilon:
        return np.argmax(qtable[state, :]) 
    else:
        return action_space.sample() 

# --- 3. ALGORITMO DE TREINAMENTO BASE (Incluindo Q-Learning e SARSA) ---
def train_agent(algorithm):
    env = gym.make("FrozenLake-v1", desc=mapa_8x8, is_slippery=False, render_mode=None)
    qtable = np.zeros((env.observation_space.n, env.action_space.n))
    rewards = []
    epsilon = MAX_EPSILON
    
    for episode in range(TOTAL_EPISODES):
        state, info = env.reset()
        done = False
        total_rewards = 0
        
        # SARSA: Precisa pré-selecionar a primeira ação (a)
        if algorithm == 'SARSA':
            action = select_action(qtable, state, epsilon, env.action_space)

        for step in range(MAX_STEPS):
            
            # Q-Learning: Seleciona a ação (a) dentro do loop
            if algorithm == 'Q-Learning':
                action = select_action(qtable, state, epsilon, env.action_space)
            
            # Executa a ação
            new_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            # Penalidade de -0.01 a cada passo
            if reward == 0 and not done:
                reward = -0.01
            
            # Seleciona a PRÓXIMA ação (a') para a próxima iteração
            next_epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
            next_action = select_action(qtable, new_state, next_epsilon, env.action_space)

            # --- ATUALIZAÇÃO DA Q-TABLE ---
            if algorithm == 'Q-Learning':
                # Off-policy: Usa o máximo (max Q(s', a'))
                max_next_q = np.max(qtable[new_state, :])
                qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
                    reward + GAMMA * max_next_q - qtable[state, action]
                )
            
            elif algorithm == 'SARSA':
                # On-policy: Usa a próxima ação real (Q(s', a'))
                qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
                    reward + GAMMA * qtable[new_state, next_action] - qtable[state, action]
                )

            # Transição de estado e ação
            state = new_state
            action = next_action 
            total_rewards += reward
            
            if done:
                break
                
        # Atualiza Epsilon
        epsilon = next_epsilon
        rewards.append(total_rewards)

    env.close()
    return rewards, qtable

# --- 4. TREINAMENTO DE AMBOS OS AGENTES ---
print(f"Iniciando Treinamento Q-Learning ({TOTAL_EPISODES} episódios)...")
rewards_q, qtable_q = train_agent('Q-Learning')

print(f"Iniciando Treinamento SARSA ({TOTAL_EPISODES} episódios)...")
rewards_sarsa, qtable_sarsa = train_agent('SARSA')

# --- 5. PLOTAGEM COMPARATIVA DA MELHORIA (TREINAMENTO) ---
plt.figure(figsize=(12, 7))
plt.plot(moving_average(rewards_q), label='Q-Learning (Off-policy)', color='blue', linewidth=1.5)
plt.plot(moving_average(rewards_sarsa), label='SARSA (On-policy)', color='red', linewidth=1.5)
plt.title(f'Comparação de Aprendizado Q-Learning vs SARSA ({TOTAL_EPISODES} Episódios)')
plt.xlabel('Episódios de Treinamento')
plt.ylabel(f'Taxa de Sucesso (Média Móvel de {WINDOW_SIZE})')
plt.legend()
plt.grid(True)
plt.show()

# --- 6. FUNÇÃO DE AVALIAÇÃO (EVALUATION) ---
def evaluate_agent(qtable, num_episodes):
    env = gym.make("FrozenLake-v1", desc=mapa_8x8, is_slippery=False, render_mode=None)
    success_count = 0
    total_reward = 0
    
    for _ in range(num_episodes):
        state, _ = env.reset()
        done = False
        
        for _ in range(MAX_STEPS):
            action = np.argmax(qtable[state, :]) 
            
            new_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            # Penalidade de -0.01 a cada passo
            if reward == 0 and not done:
                reward = -0.01
            
            state = new_state
            total_reward += reward
            
            if done:
                if state == 63: 
                    success_count += 1
                break
    
    env.close()
    return success_count / num_episodes, total_reward / num_episodes

# --- 7. AVALIAÇÃO E RESULTADOS (100 EPISÓDIOS) ---
NUM_EVAL_EPISODES = 100
print(f"\n--- Avaliação (Teste) em {NUM_EVAL_EPISODES} Episódios ---")

success_q, avg_reward_q = evaluate_agent(qtable_q, NUM_EVAL_EPISODES)
success_sarsa, avg_reward_sarsa = evaluate_agent(qtable_sarsa, NUM_EVAL_EPISODES)

print(f"Q-Learning (Off-policy): Taxa de Sucesso = {success_q*100:.2f}% | Recompensa Média = {avg_reward_q:.4f}")
print(f"SARSA (On-policy): Taxa de Sucesso = {success_sarsa*100:.2f}% | Recompensa Média = {avg_reward_sarsa:.4f}")

# --- 8. DISCUSSÃO ---
print("\n--- Discussão da Atividade 10 ---")
print("Em um ambiente determinístico (não escorregadio), ambos os algoritmos tendem a convergir para a política ótima.")

if abs(avg_reward_q - avg_reward_sarsa) < 0.001:
    print("Os agentes tiveram um desempenho **virtualmente idêntico** na avaliação, o que é esperado em ambientes determinísticos, pois a rota ótima é a mais rápida e segura para ambos.")
elif avg_reward_q > avg_reward_sarsa:
    print(f"**Resultado:** O agente Q-Learning ({avg_reward_q:.4f}) foi marginalmente superior ao SARSA ({avg_reward_sarsa:.4f}) na recompensa média, confirmando a tendência teórica de o Q-Learning (Off-policy) convergir um pouco mais rápido para o ótimo.")
else:
    print(f"**Resultado:** O agente SARSA ({avg_reward_sarsa:.4f}) foi marginalmente superior ao Q-Learning ({avg_reward_q:.4f}). Isso pode ocorrer devido à aleatoriedade inicial da exploração, mas ambos são eficazes.")

print("\nConclusão da Avaliação (100 Episódios):")
print("Em ambientes sem incerteza, a diferença prática entre os dois algoritmos é mínima após um treinamento extensivo.")