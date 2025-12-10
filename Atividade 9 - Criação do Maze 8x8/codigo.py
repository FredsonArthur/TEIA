import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONSTRUÇÃO DO MAPA (Conforme Atividade 9) ---
# Matriz extraída do slide/gist fornecido
holes_array = np.array([
    [0, 0, 0, 0, 0, 1, 0, 0],  # S . . . . H . .
    [0, 1, 1, 1, 0, 1, 0, 1],  # . H H H . H . H
    [0, 0, 0, 0, 0, 0, 0, 0],  # . . . . . . . .
    [1, 1, 0, 1, 1, 1, 1, 0],  # H H . H H H H . (O corredor difícil)
    [0, 0, 0, 0, 0, 0, 0, 0],  # . . . . . . . .
    [0, 1, 1, 1, 1, 1, 0, 1],  # . H H H H H . H
    [0, 0, 0, 0, 0, 0, 0, 0],  # . . . . . . . .
    [0, 1, 0, 1, 1, 0, 1, 0]   # . H . H H . H G
])

def gerar_mapa_customizado(layout):
    """Transforma a matriz numérica em letras para o Gym (S, F, H, G)"""
    desc = []
    rows, cols = layout.shape
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if r == 0 and c == 0: row_str += "S" # Start
            elif r == rows-1 and c == cols-1: row_str += "G" # Goal
            elif layout[r][c] == 1: row_str += "H" # Hole/Wall
            else: row_str += "F" # Frozen/Floor
        desc.append(row_str)
    return desc

mapa_8x8 = gerar_mapa_customizado(holes_array)

# --- 2. HIPERPARÂMETROS (O SEGREDO ESTÁ AQUI) ---
TOTAL_EPISODES = 20000  # Mais episódios para garantir convergência
MAX_STEPS = 200         # Aumentado (era 100): precisa de tempo para cruzar 8x8
LEARNING_RATE = 0.9     # Aprendizado rápido quando achar a recompensa
GAMMA = 0.99            # Foco total no objetivo final
MAX_EPSILON = 1.0
MIN_EPSILON = 0.01
DECAY_RATE = 0.0003     # <--- Decaimento LENTO. Se for rápido, ele desiste antes de achar.

# --- 3. CONFIGURAÇÃO DO AMBIENTE ---
# is_slippery=False é essencial para simular um "Maze" (Labirinto determinístico)
env = gym.make("FrozenLake-v1", desc=mapa_8x8, is_slippery=False, render_mode=None)
qtable = np.zeros((env.observation_space.n, env.action_space.n))

rewards = []
epsilon = MAX_EPSILON
primeira_vitoria = False

print("Treinando... (Aguarde a mensagem de sucesso)")

# --- 4. LOOP DE TREINAMENTO ---
for episode in range(TOTAL_EPISODES):
    state, info = env.reset()
    done = False
    total_rewards = 0
    
    for step in range(MAX_STEPS):
        # Ação (Epsilon-Greedy)
        if np.random.uniform(0, 1) > epsilon:
            action = np.argmax(qtable[state, :]) # Exploit
        else:
            action = env.action_space.sample()   # Explore
            
        new_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # Atualização Q-Table
        qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
            reward + GAMMA * np.max(qtable[new_state, :]) - qtable[state, action]
        )
        
        state = new_state
        total_rewards += reward
        
        if done:
            # DEBUG: Verifica se chegou no objetivo (G)
            if reward == 1.0 and not primeira_vitoria:
                print(f"--> SUCESSO! O agente encontrou a saída pela 1ª vez no ep {episode}!")
                primeira_vitoria = True
            break
            
    # Atualiza Epsilon
    epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
    rewards.append(total_rewards)

env.close()

# --- 5. RESULTADO ---
def moving_average(data, window_size=500):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

plt.figure(figsize=(12, 6))
plt.plot(moving_average(rewards), color='green', linewidth=1.5)
plt.title('Aprendizado no Maze 8x8 (Ajustado)')
plt.xlabel('Episódios')
plt.ylabel('Taxa de Sucesso (Média Móvel)')
plt.grid(True)
plt.show()

if not primeira_vitoria:
    print("ALERTA: O agente não conseguiu resolver. Tente aumentar MAX_STEPS.")