import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Paramètres de la membrane et de la simulation ---
N = 200          # Résolution de la grille
L = np.pi        # Taille du domaine spatial [0, L]
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

c = 1.0          # Vitesse de propagation

# --- 2. Fonction calculant la solution analytique exacte ---
# Basée sur la séparation des variables : u(x, y, t) = X(x) * Y(y) * T(t)
def get_wave(t):
    u = np.zeros((N, N))
    
    # Définition de modes propres (m, n) avec leurs amplitudes initiales
    modes = [
        {"m": 1, "n": 1, "A": 1.0},
        {"m": 2, "n": 1, "A": 0.6},
        {"m": 1, "n": 2, "A": 0.5},
        {"m": 2, "n": 2, "A": 0.3}
    ]
    
    for mode in modes:
        m, n, A = mode["m"], mode["n"], mode["A"]
        
        # Pulsation propre omega_mn issue de la séparation en temps
        omega_mn = c * np.pi * np.sqrt((m / L)**2 + (n / L)**2)
        
        # Formule analytique : sin(m*pi*x/L) * sin(n*pi*y/L) * cos(omega_mn * t)
        spatial_x = np.sin(m * X * np.pi / L)
        spatial_y = np.sin(n * Y * np.pi / L)
        temporal = np.cos(omega_mn * t)
        
        u += A * spatial_x * spatial_y * temporal
        
    return u

# --- 3. Configuration de la figure graphique ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 7))

# Affichage du premier état à t = 0
im = ax.imshow(get_wave(0), cmap='ocean', animated=True, vmin=-2.0, vmax=2.0, interpolation='bicubic')
cbar = plt.colorbar(im, label="Amplitude de la membrane")
cbar.ax.yaxis.set_tick_params(color='white')

ax.set_title("Vibration d'une membrane carrée — Séparation des variables\n(Superposition de modes propres analytiques)", fontsize=11, color='cyan')
ax.axis('off')

  
<img width="1450" height="720" alt="image" src="https://github.com/user-attachments/assets/3709ab11-5e46-4e8f-b4c2-ebd2f32315ee" />
