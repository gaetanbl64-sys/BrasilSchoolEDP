import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Paramètres de la simulation ---
N = 200          # Résolution augmentée (200x200) pour un rendu beaucoup plus fin
dx = 1.0         
dt = 0.2         # Pas de temps
c = 1.0          # Vitesse de propagation de l'onde
damping = 0.993  # Facteur d'amortissement pour dissiper l'énergie comme de vraie eau
factor = (c * dt / dx) ** 2

# --- 2. Initialisation des matrices d'état ---
u_prev = np.zeros((N, N))
u_curr = np.zeros((N, N))
u_next = np.zeros((N, N))

# --- 3. Configuration de la figure graphique (Style pro / sombre) ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 7))

# Utilisation d'une palette 'ocean' ou 'cubehelix' et d'une interpolation bicubique pour le réalisme
im = ax.imshow(u_curr, cmap='ocean', animated=True, vmin=-1.5, vmax=1.5, interpolation='bicubic')
cbar = plt.colorbar(im, label="Amplitude de l'onde")
cbar.ax.yaxis.set_tick_params(color='white')

ax.set_title("Bassin de vagues interactif - Équation d'onde 2D\n(Cliquez sur l'image pour créer des vagues)", fontsize=11, color='cyan')
ax.axis('off')

# --- 4. Gestion du clic utilisateur (Création de foyers interactifs) ---
def on_click(event):
    global u_curr
    # Vérifie que le clic est bien dans la zone de la simulation
    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
        # Récupération des coordonnées du clic et conversion en indices de grille
        ix = int(np.clip(event.xdata, 0, N - 1))
        iy = int(np.clip(event.ydata, 0, N - 1))
        
        # Zone d'impact de la goutte d'eau (gère les bords en toute sécurité)
        r = 6
        ymin, ymax = max(0, iy - r), min(N, iy + r + 1)
        xmin, xmax = max(0, ix - r), min(N, ix + r + 1)
        
        YY, XX = np.ogrid[ymin:ymax, xmin:xmax]
        dist_sq = (XX - ix)**2 + (YY - iy)**2
        
        # Injection d'une impulsion gaussienne douce (effet goutte d'eau)
        u_curr[ymin:ymax, xmin:xmax] += 8.0 * np.exp(-dist_sq / 4.0)

# Connexion de l'événement de clic à la figure Matplotlib
fig.canvas.mpl_connect('button_press_event', on_click)

# --- 5. Fonction de mise à jour (Boucle physique) ---
def update(frame):
    global u_prev, u_curr, u_next
    
    # Calcul vectorisé du laplacien spatial sur la grille intérieure
    laplacian = (
        u_curr[2:, 1:-1] + u_curr[:-2, 1:-1] +
        u_curr[1:-1, 2:] + u_curr[1:-1, :-2] -
        4 * u_curr[1:-1, 1:-1]
    )
    
    # Résolution de l'équation d'onde discrète avec prise en compte de l'amortissement
    u_next[1:-1, 1:-1] = (2 * u_curr[1:-1, 1:-1] - u_prev[1:-1, 1:-1] + factor * laplacian) * damping
    
    # Conditions aux limites (bords fixes à 0)
    u_next[0, :] = 0
    u_next[-1, :] = 0
    u_next[:, 0] = 0
    u_next[:, -1] = 0
    
    # Rotation des états pour le pas de temps suivant
    u_prev[:] = u_curr
    u_curr[:] = u_next
    
    # Mise à jour de l'affichage de l'image
    im.set_array(u_curr)
    return [im]

# --- 6. Lancement de l'animation ---
ani = animation.FuncAnimation(fig, update, interval=25, blit=True)

plt.show()