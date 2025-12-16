import numpy as np
import matplotlib.pyplot as plt

# --- 1. MAPA E CONFIGURAÇÃO ---
# 0: Gelo, 1: Buraco, 2: Porta
layout_grid = np.array([
    [0, 0, 0, 0, 0, 1, 0, 0], 
    [0, 1, 1, 1, 0, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 1, 2, 1, 1, 1, 1, 2], # Portas (3,2) e (3,7)
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 1, 1, 2, 1], # Porta (5,6)
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 0, 1, 1, 0, 1, 0]   
])

# --- 2. AMBIENTE (LÓGICA DAS PORTAS) ---
class MazeWithDoors:
    def __init__(self, grid):
        self.initial_grid = grid.copy()
        self.grid = grid.copy()
        self.rows, self.cols = grid.shape
        self.state = 0
        self.action_space_n = 4
        self.observation_space_n = self.rows * self.cols

    def reset(self):
        self.state = 0
        self.grid = self.initial_grid.copy() # Reseta as portas fechadas
        return self.state, {}

    def step(self, action):
        row = self.state // self.cols
        col = self.state % self.cols
        
        # Movimentação
        new_row, new_col = row, col
        if action == 0: new_col = max(col - 1, 0)       # Left
        elif action == 1: new_row = min(row + 1, self.rows - 1) # Down
        elif action == 2: new_col = min(col + 1, self.cols - 1) # Right
        elif action == 3: new_row = max(row - 1, 0)     # Up
        
        target_cell = self.grid[new_row, new_col]
        
        reward = 0
        terminated = False
        truncated = False
        
        # Lógica de Colisão
        if target_cell == 1: # Buraco
            self.state = new_row * self.cols + new_col
            reward = 0 # Morte
            terminated = True
            
        elif target_cell == 2: # Porta Fechada
            self.grid[new_row, new_col] = 0 # Abre a porta
            reward = 0.5 # Recompensa por abrir porta (incentivo)
            # Agente não anda, mas o caminho abre
            
        else: # Caminho Livre
            self.state = new_row * self.cols + new_col
            if new_row == 7 and new_col == 7: # OBJETIVO
                reward = 10.0 # <--- O SEGREDO (Recompensa alta atrai o agente)
                terminated = True
            else:
                reward = -0.01 # Custo do passo
                
        return self.state, reward, terminated, truncated, {}

# --- 3. TREINAMENTO (Q-LEARNING) ---
env = MazeWithDoors(layout_grid)
TOTAL_EPISODES = 20000 
MAX_STEPS = 200        
LEARNING_RATE = 0.1    
GAMMA = 0.99           
MAX_EPSILON = 1.0
MIN_EPSILON = 0.01
DECAY_RATE = 0.0002    

qtable = np.zeros((env.observation_space_n, env.action_space_n))
rewards = []
epsilon = MAX_EPSILON

print("Treinando...")
for episode in range(TOTAL_EPISODES):
    state, _ = env.reset()
    total_rewards = 0
    
    for step in range(MAX_STEPS):
        if np.random.uniform(0, 1) > epsilon:
            action = np.argmax(qtable[state, :])
        else:
            action = np.random.randint(0, 4)
            
        new_state, reward, terminated, _, _ = env.step(action)
        
        max_next_q = np.max(qtable[new_state, :])
        qtable[state, action] = qtable[state, action] + LEARNING_RATE * (
            reward + GAMMA * max_next_q - qtable[state, action]
        )
        
        state = new_state
        total_rewards += reward
        if terminated: break
            
    epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
    rewards.append(total_rewards)

# --- 4. RESULTADO VISUAL ---
def moving_average(data, window_size=500):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

plt.figure(figsize=(10, 6))
plt.plot(moving_average(rewards), color='green') # Verde de sucesso!
plt.title('Resultado Correto: Maze 8x8 com Portas (Convergência Estável)')
plt.ylabel('Recompensa Acumulada')
plt.xlabel('Episódios')
plt.grid()
plt.show()