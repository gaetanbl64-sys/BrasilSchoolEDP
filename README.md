## Modélisation Mathématique & Physique, EDP simple: equation d'onde

Le projet simule la propagation des ondes bidimensionnelles (vagues à la surface d'un bassin) en résolvant l'équation d'onde classique des cordes et membranes vibrantes :

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

Où :
* $u(x, y, t)$ représente l'amplitude (hauteur de l'eau) au point $(x, y)$ et à l'instant $t$.
* $c$ est la vitesse de propagation de l'onde dans le milieu.
* Le terme de droite correspond à l'opérateur laplacien spatial $\Delta u$, qui mesure la courbure locale de la surface de l'eau.

### Discrétisation Numérique (Différences Finies)

Pour implémenter cette équation sous forme algorithmique, nous utilisons un schéma explicite aux différences finies centré au second ordre en espace et en temps :

$$u_{i,j}^{n+1} = 2u_{i,j}^n - u_{i,j}^{n-1} + \left(\frac{c \Delta t}{\Delta x}\right)^2 \left( u_{i+1,j}^n + u_{i-1,j}^n + u_{i,j+1}^n + u_{i,j-1}^n - 4u_{i,j}^n \right)$$

### Conditions aux Limites

* **Conditions aux limites :** Les bords du domaine imposent une amplitude nulle ($u = 0$), agissant comme des parois absorbantes ou fixes.
* **Obstacle (Rocher) :** Un masque booléen spatial est appliqué pour bloquer la propagation de l'onde (`u_next[rock_mask] = 0.0`), créant ainsi des phénomènes physiques réalistes de **réflexion** et de **diffraction** lorsque les ondes contournent l'îlot central.
* **Amortissement :** Un facteur d'atténuation est appliqué à chaque pas de temps pour dissiper l'énergie de manière naturelle, simulant la viscosité du fluide.
* 
<img width="1450" height="720" alt="image" src="https://github.com/user-attachments/assets/3709ab11-5e46-4e8f-b4c2-ebd2f32315ee" />
