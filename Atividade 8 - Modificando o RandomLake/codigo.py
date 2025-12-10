import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import numpy as np
import matplotlib.pyplot as plt

# --- PARÂMETROS ---
TOTAL_EPISODES = 2000
MAX_STEPS = 100
LEARNING_RATE = 0.8
GAMMA = 0.95
MAX_EPSILON = 1.0
MIN_EPSILON = 0.01
DECAY_RATE = 0.005

def train_agent(fixar_mapa=False):
    """
    Treina o agente.
    Se fixar_mapa = True, usa o mesmo layout para todos os episódios.
    Se fixar_mapa = False, gera um novo layout a cada episódio.
    """
    rewards = []
    epsilon = MAX_EPSILON

    # Se formos fixar o mapa, geramos ele UMA vez aqui
    if fixar_mapa:
        mapa_fixo = generate_random_map(size=4, p=0.8)
        env = gym.make("FrozenLake-v1", desc=mapa_fixo, is_slippery=False, render_mode=None)
        qtable = np.zeros((env.observation_space.n, env.action_space.n))
    else:
        # Se o mapa muda, inicializamos a tabela para o tamanho padrão (4x4 = 16 estados)
        qtable = np.zeros((16, 4))
        env = None

    for episode in range(TOTAL_EPISODES):
        
        # Se o mapa não é fixo, recria o ambiente a cada episódio
        if not fixar_mapa:
            mapa_random = generate_random_map(size=4, p=0.8)
            env = gym.make("FrozenLake-v1", desc=mapa_random, is_slippery=False, render_mode=None)
        
        state, info = env.reset()
        total_rewards = 0
        done = False

        for step in range(MAX_STEPS):
            # 1. Escolha da ação (Epsilon-Greedy)
            if np.random.uniform(0, 1) > epsilon:
                action = np.argmax(qtable[state, :]) # Exploit
            else:
                action = env.action_space.sample()   # Explore

            # 2. Executar ação
            new_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # 3. Atualizar Q-Table
            qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
                reward + GAMMA * np.max(qtable[new_state, :]) - qtable[state, action]
            )

            state = new_state
            total_rewards += reward

            if done:
                break

        # Atualiza Epsilon
        epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
        rewards.append(total_rewards)

        if not fixar_mapa:
            env.close()

    if fixar_mapa:
        env.close()

    return rewards

# --- EXECUÇÃO ---
print("Treinando cenário ORIGINAL (Mapa muda a cada episódio)...")
rewards_original = train_agent(fixar_mapa=False)

print("Treinando cenário PROPOSTO (Mapa fixo)...")
rewards_fixed = train_agent(fixar_mapa=True)

# --- VISUALIZAÇÃO ---
def moving_average(data, window_size=50):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

plt.figure(figsize=(10, 6))
plt.plot(moving_average(rewards_original), label='Original (Mapa Dinâmico)', color='red', alpha=0.6)
plt.plot(moving_average(rewards_fixed), label='Proposta (Mapa Fixo)', color='green')
plt.title('Comparação: RandomLake vs FixedLake')
plt.xlabel('Episódios')
plt.ylabel('Recompensa Média')
plt.legend()
plt.grid(True)
plt.savefig('resultado.png')
plt.show()