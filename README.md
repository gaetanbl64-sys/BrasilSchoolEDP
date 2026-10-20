# 2D Wave Equation & Membrane Simulation

This repository explores the modeling and simulation of the **two-dimensional wave equation**, comparing the traditional analytical approach (separation of variables) with a high-performance numerical approach using finite differences in Python.

---

## 🔬 Theoretical Background: Analytical vs. Numerical

### 1. The Continuous Wave Equation
The physical phenomenon governing both wave basins and vibrating membranes is the 2D wave equation:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = c^2 \Delta u$$

Where:
* $u(x, y, t)$ is the wave amplitude / membrane displacement.
* $c$ is the wave propagation speed.
* $\Delta u$ is the spatial Laplacian.

---

### 2. The Analytical Approach: Separation of Variables
In classical mathematical physics, one assumes a solution of the form:
$$u(x, y, t) = X(x) Y(y) T(t)$$

By separating variables and applying homogeneous Dirichlet boundary conditions ($u = 0$ at the borders), the spatial modes are expressed as combinations of sine functions:
$$u(x, y, t) = \sum_{m,n} A_{mn} \sin\left(\frac{m \pi x}{L}\right) \sin\left(\frac{n \pi y}{L}\right) \cos(\omega_{mn} t)$$

* **Pros:** Exact mathematical solution; perfect for finding natural resonant frequencies ( eigenmodes ) of ideal rectangular geometries.
* **Cons:** Becomes computationally intractable or analytically impossible when dealing with local interactive disturbances (like clicking to drop a Gaussian droplet) or complex, irregular boundaries.

---

### 3. The Numerical Approach: Finite Differences Method (FDM)
To overcome the limitations of analytical series expansion for real-time interactivity, we discretize the continuous domain into a grid of indices $u_{i,j}^n$ where $x = i \cdot dx$, $y = j \cdot dx$, and $t = n \cdot dt$.

#### A. Temporal Discretization (Centered Taylor Series)
$$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_{i,j}^{n+1} - 2u_{i,j}^n + u_{i,j}^{n-1}}{dt^2}$$

#### B. Spatial Discretization (5-Point Stencil Laplacian)
$$\Delta u \approx \frac{u_{i+1,j}^n + u_{i-1,j}^n + u_{i,j+1}^n + u_{i,j-1}^n - 4u_{i,j}^n}{dx^2}$$

#### C. Explicit Time-Stepping Update Rule
Combining these approximations yields the explicit recurrence formula implemented in our simulation loop:

$$u_{i,j}^{n+1} = \left( 2u_{i,j}^n - u_{i,j}^{n-1} + \left(\frac{c \cdot dt}{dx}\right)^2 \Delta u_{\text{spatial}} \right) \times \text{damping}$$

---

## ⚙️ Key Numerical Parameters

* **$\text{factor} = \left(\frac{c \cdot dt}{dx}\right)^2$**: Governs the Courant-Friedrichs-Lewy (CFL) stability criterion. Ensuring this ratio remains within stable bounds prevents numerical divergence.
* **$\text{damping}$ (e.g., $0.993$):** Introduces energy dissipation (mimicking fluid viscosity or internal material friction) to prevent infinite reflections.
* **Boundary Conditions:** Fixed edges enforced by setting boundary matrices to zero ($u = 0$).

---

## 🚀 Getting Started

Make sure you have Python installed along with the required scientific libraries:

```bash
pip install numpy matplotlib

  
<img width="1450" height="720" alt="image" src="https://github.com/user-attachments/assets/3709ab11-5e46-4e8f-b4c2-ebd2f32315ee" />
