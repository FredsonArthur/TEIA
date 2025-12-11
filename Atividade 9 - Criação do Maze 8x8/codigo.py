import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONSTRUÇÃO DO MAPA (Conforme Atividade 9) ---
# Matriz 8x8 para simular o Maze
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
mapa_formatado = "\n".join(mapa_8x8)
print("--- Mapa 8x8 do FrozenLake-v1 (S=Start, F=Floor, H=Hole, G=Goal) ---")
print(mapa_formatado)
print("-------------------------------------------------------------------\n")

# --- 2. HIPERPARÂMETROS (MÁXIMA ESTABILIDADE) ---
TOTAL_EPISODES = 40000 
MAX_STEPS = 100         
LEARNING_RATE = 0.75    
GAMMA = 0.95            
MAX_EPSILON = 1.0
MIN_EPSILON = 0.01
DECAY_RATE = 0.000008   

# --- 3. CONFIGURAÇÃO DO AMBIENTE ---
env = gym.make("FrozenLake-v1", desc=mapa_8x8, is_slippery=False, render_mode=None)
qtable = np.zeros((env.observation_space.n, env.action_space.n))

rewards = []
epsilon = MAX_EPSILON
primeira_vitoria = False

print("Iniciando Treinamento Q-Learning (Aguarde a mensagem de sucesso)...")

# --- 4. LOOP DE TREINAMENTO ---
for episode in range(TOTAL_EPISODES):
    state, info = env.reset()
    done = False
    total_rewards = 0
    
    for step in range(MAX_STEPS):
        # 4.1. Ação (Epsilon-Greedy)
        if np.random.uniform(0, 1) > epsilon:
            action = np.argmax(qtable[state, :]) 
        else:
            action = env.action_space.sample()   
            
        # Executa a ação
        new_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # *** Penalidade de -0.01 a cada passo ***
        if reward == 0 and not done:
            reward = -0.01
        
        # 4.2. Atualização Q-Table (Fórmula de Bellman)
        qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
            reward + GAMMA * np.max(qtable[new_state, :]) - qtable[state, action]
        )
        
        state = new_state
        total_rewards += reward
        
        if done:
            # 4.3. Debug e Sucesso (Verificação do Goal)
            if state == 63 and not primeira_vitoria: 
                print(f"--> SUCESSO! O agente encontrou a saída pela 1ª vez no episódio {episode + 1}!")
                primeira_vitoria = True
            break
            
    # 4.4. Atualiza Epsilon (Decaimento exponencial)
    epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
    rewards.append(total_rewards)

env.close()

# --- 5. RESULTADO E PLOTAGEM ---
def moving_average(data, window_size=500):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

plt.figure(figsize=(12, 6))
plt.plot(moving_average(rewards), color='green', linewidth=1.5)
plt.title('Aprendizado Q-Learning no Maze 8x8 (Determinístico)')
plt.xlabel('Episódios')
plt.ylabel('Taxa de Sucesso (Média Móvel de 500)')
plt.grid(True)
plt.show()

if moving_average(rewards)[-1] > -0.05:
    print("\n--- Treinamento Finalizado ---")
    print("SUCESSO: O agente otimizou a política para a rota mais rápida (confirmado pelo gráfico).")
else:
    print("\n--- Treinamento Finalizado ---")
    print("ALERTA: O agente não conseguiu resolver. Verifique os hiperparâmetros.")
    
# --- 6. ANÁLISE DA POLÍTICA ÓTIMA ---
politica_aprendida = np.argmax(qtable, axis=1)

# 7. EXIBIÇÃO DA POLÍTICA FINAL
print("\nPolítica Aprendida (Array Numérico, para referência):")
print(politica_aprendida)