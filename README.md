# 2D Wave Equation & Membrane Simulation

A Python-based scientific simulation exploring two-dimensional wave propagation and elastic membrane vibrations. This project bridges theoretical mathematical modeling (partial differential equations and separation of variables) with efficient numerical methods (finite difference schemes) implemented via NumPy and Matplotlib.

---

## 🔬 Mathematical & Physical Modeling

### 1. The Continuous Wave Equation
The physical system is governed by the classical two-dimensional wave equation for vibrating media:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = c^2 \Delta u$$

Where:
* $u(x, y, t)$ represents the displacement amplitude at point $(x, y)$ and time $t$.
* $c$ is the wave propagation speed in the medium.
* $\Delta u$ is the spatial Laplacian operator, which measures the local curvature of the surface.

### 2. Analytical Approach: Separation of Variables
To find exact theoretical modes of vibration for ideal geometries (such as a square membrane with fixed edges), one can use the **separation of variables method** by setting:
$$u(x, y, t) = X(x) Y(y) T(t)$$

This leads to harmonic solutions combining spatial sine profiles and temporal oscillations (Fourier modes):
$$u(x,y,t) = \sum_{m,n} A_{mn} \sin\left(\frac{m \pi x}{L}\right) \sin\left(\frac{n \pi y}{L}\right) \cos(\omega_{mn} t)$$
where $\omega_{mn} = c \pi \sqrt{(m/L)^2 + (n/L)^2}$ represents the natural angular frequencies of the system.

### 3. Numerical Approach: Finite Differences
While analytical Fourier expansions are ideal for steady-state modes, handling dynamic user interactions or complex geometries requires a **numerical discretization** using an explicit second-order centered finite difference scheme:

* **Temporal Derivative:** 
  $$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_{i,j}^{n+1} - 2u_{i,j}^n + u_{i,j}^{n-1}}{dt^2}$$
* **Spatial Laplacian (5-point stencil):** 
  $$\Delta u \approx \frac{u_{i+1,j}^n + u_{i-1,j}^n + u_{i,j+1}^n + u_{i,j-1}^n - 4u_{i,j}^n}{dx^2}$$

Combining these yields the explicit time-stepping recurrence relation:
$$u_{i,j}^{n+1} = 2u_{i,j}^n - u_{i,j}^{n-1} + \left( \frac{c \cdot dt}{dx} \right)^2 \Delta u_{spatial}$$

---

## ⚙️ Numerical Implementation Details

* **Vectorized Computations:** Spatial operators are computed efficiently across the grid matrices using NumPy vectorization.
* **Stability & CFL Condition:** Governed by the factor $\left(\frac{c \cdot dt}{dx}\right)^2$, ensuring numerical convergence without exploding values.
* **Energy Dissipation (Damping):** A selective attenuation factor is applied at each time step to naturally dissipate energy and simulate material/fluid viscosity.
* **Boundary Conditions:** Dirichlet boundary conditions ($u = 0$) lock the outer edges of the domain to simulate fixed or absorbing walls where waves reflect.

---

  
<img width="1450" height="720" alt="image" src="https://github.com/user-attachments/assets/3709ab11-5e46-4e8f-b4c2-ebd2f32315ee" />
