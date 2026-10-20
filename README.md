## Mathematical & Physical Modeling, Simple PDE: Wave Equation

The project simulates the propagation of two-dimensional waves (ripples on a water basin) by solving the classical wave equation for vibrating strings and membranes:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

Where:
* $u(x, y, t)$ represents the amplitude (water height) at point $(x, y)$ and time $t$.
* $c$ is the wave propagation speed in the medium.
* The right-hand side corresponds to the spatial Laplacian operator $\Delta u$, which measures the local curvature of the water surface.

### Numerical Discretization (Finite Differences)

To implement this equation algorithmically, we use an explicit second-order centered finite difference scheme in space and time:

$$u_{i,j}^{n+1} = 2u_{i,j}^n - u_{i,j}^{n-1} + \left(\frac{c \Delta t}{\Delta x}\right)^2 \left( u_{i+1,j}^n + u_{i-1,j}^n + u_{i,j+1}^n + u_{i,j-1}^n - 4u_{i,j}^n \right)$$

### Boundary Conditions & Obstacles

* **Boundary conditions:** The edges of the domain impose a zero amplitude ($u = 0$), acting as fixed or absorbing walls.
* **Obstacle (Rock):** A spatial boolean mask is applied to block wave propagation (`u_next[rock_mask] = 0.0`), creating realistic physical phenomena of **reflection** and **diffraction** as waves flow around the central island.
* **Damping:** An attenuation factor is applied at each time step to naturally dissipate energy, simulating fluid viscosity.

  
<img width="1450" height="720" alt="image" src="https://github.com/user-attachments/assets/3709ab11-5e46-4e8f-b4c2-ebd2f32315ee" />
