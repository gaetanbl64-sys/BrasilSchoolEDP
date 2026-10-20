import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Paramètres de la simulation ---
N = 120         # Résolution équilibrée (120x120) pour préserver la fluidité de la double vue 3D+2D
dx = 1.0 
dt = 0.2        # Pas de temps
c = 2.0         # Vitesse de propagation de l'onde
damping = 0.996 # Facteur d'amortissement
factor = (c * dt / dx) ** 2

# --- 2. Initialisation des matrices d'état et grille 3D ---
u_prev = np.zeros((N, N))
u_curr = np.zeros((N, N))
u_next = np.zeros((N, N))

x = np.linspace(0, N, N)
y = np.linspace(0, N, N)
X, Y = np.meshgrid(x, y)

# --- 3. Configuration de la figure avec 2 sous-vues (2D à gauche, 3D à droite) ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 7))
fig.suptitle("Bassin de vagues interactif - Comparaison 2D & 3D\n(Cliquez ou glissez la souris sur l'une ou l'autre des vues pour créer des vagues)", fontsize=12, color='cyan')

# Sous-graphique 1 : Vue 2D (à gauche)
ax_2d = fig.add_subplot(1, 2, 1)
im = ax_2d.imshow(u_curr, cmap='ocean', vmin=-1.0, vmax=1.0, interpolation='bicubic')
ax_2d.set_title("Vue 2D (Carte de chaleur)", fontsize=10)
ax_2d.axis('off')

# Sous-graphique 2 : Vue 3D (à droite)
ax_3d = fig.add_subplot(1, 2, 2, projection='3d')
surf = [ax_3d.plot_surface(X, Y, u_curr, cmap='ocean', edgecolor='none', rstride=2, cstride=2, antialiased=True)]
ax_3d.set_zlim(-1.0, 1.0)
ax_3d.set_title("Vue 3D (Relief)", fontsize=10)
ax_3d.axis('off')
ax_3d.view_init(elev=35, azim=-45)

# --- 4. Gestion interactive (Clics et dessin sur les deux axes) ---
mouse_pressed = False

def on_press(event):
    global mouse_pressed
    mouse_pressed = True
    add_wave(event)

def on_release(event):
    global mouse_pressed
    mouse_pressed = False

def on_motion(event):
    if mouse_pressed:
        add_wave(event)

def add_wave(event):
    global u_curr
    # Vérifie si le clic/mouvement est dans l'un des deux axes de simulation
    if event.inaxes in [ax_2d, ax_3d] and event.xdata is not None and event.ydata is not None:
        ix = int(np.clip(event.xdata, 0, N - 1))
        iy = int(np.clip(event.ydata, 0, N - 1))
        
        r = 6
        ymin, ymax = max(0, iy - r), min(N, iy + r + 1)
        xmin, xmax = max(0, ix - r), min(N, ix + r + 1)
        
        YY, XX = np.ogrid[ymin:ymax, xmin:xmax]
        dist_sq = (XX - ix)**2 + (YY - iy)**2
        
        # Injection d'une impulsion gaussienne douce et contrôlée (amplitude des vagues de 1.5)
        u_curr[ymin:ymax, xmin:xmax] += 0.5 * np.exp(-dist_sq / 4.0)

# Connexion des événements de souris à la fenêtre
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# --- 5. Fonction de mise à jour (Boucle physique commune) ---
def update(frame):
    global u_prev, u_curr, u_next, surf
    
    # Calcul vectorisé du laplacien spatial sur la grille intérieure
    laplacian = (
        u_curr[2:, 1:-1] + u_curr[:-2, 1:-1] +
        u_curr[1:-1, 2:] + u_curr[1:-1, :-2] -
        4 * u_curr[1:-1, 1:-1]
    )
    
    # Résolution de l'équation d'onde discrète avec amortissement
    u_next[1:-1, 1:-1] = (2 * u_curr[1:-1, 1:-1] - u_prev[1:-1, 1:-1] + factor * laplacian) * damping
    
    # Conditions aux limites (bords fixes à 0)
    u_next[0, :] = 0
    u_next[-1, :] = 0
    u_next[:, 0] = 0
    u_next[:, -1] = 0
    
    # Rotation des états pour le pas de temps suivant
    u_prev[:] = u_curr
    u_curr[:] = u_next
    
    # Mise à jour de la vue 2D
    im.set_array(u_curr)
    
    # Mise à jour de la vue 3D
    surf[0].remove()
    surf[0] = ax_3d.plot_surface(X, Y, u_curr, cmap='ocean', edgecolor='none', rstride=2, cstride=2, antialiased=True)
    
    return [im, surf[0]]

# --- 6. Lancement de l'animation ---
# blit=False est nécessaire pour le rendu combiné de la surface 3D
ani = animation.FuncAnimation(fig, update, interval=25, blit=False)

plt.show()