import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================
# 1. QUANTUM SYSTEM & LAUNCH PARAMETERS
# ==========================================
# Effective quantum scale (allows visible de Broglie wavelengths)
hbar = 0.08      # Planck constant scale
m = 1.0          # Particle mass
g = 9.81         # Uniform gravity acceleration

# Launch initial conditions (center of initial wavepacket)
x0, y0 = 0.4, 0.4
px0, py0 = 3.2, -4.2
sigma0 = 0.22    # Initial spatial width of quantum wavepacket

# Calculate flight scale
T_flight = (py0 / (m * g)) + np.sqrt((py0 / (m * g))**2 + 2 * y0 / g)

# High-resolution spatial grid (350 x 350 = 122,500 sub-cells)
Nx, Ny = 350, 350
x_grid = np.linspace(0, 4.5, Nx)
y_grid = np.linspace(0, 2.5, Ny)
dx = x_grid[1] - x_grid[0]
dy = y_grid[1] - y_grid[0]

X, Y = np.meshgrid(x_grid, y_grid)
X_mid = 0.5 * (X[:-1, :-1] + X[1:, 1:])
Y_mid = 0.5 * (Y[:-1, :-1] + Y[1:, 1:])

# ==========================================
# 2. VISUALIZATION SETUP (3 SUBPLOTS)
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 11))

# Subplot 1: Real part of complex wave function Re(Psi)
im_psi = ax1.imshow(np.zeros_like(X), extent=[0, x_grid[-1], 0, y_grid[-1]],
                    origin='lower', aspect='auto', cmap='seismic', vmin=-1.5, vmax=1.5)
ax1.set_title("True Quantum Wave Function $\\text{Re}(\\Psi(x,y,t))$ [de Broglie Phase Oscillations]")
ax1.set_ylabel("Vertical Position $y$ (m)")
fig.colorbar(im_psi, ax=ax1, label=r"$\text{Re}(\Psi)$")

# Subplot 2: Integrated Cell Probability (White = 0, Black = High)
im_prob = ax2.imshow(np.zeros_like(X_mid), extent=[0, x_grid[-1], 0, y_grid[-1]],
                     origin='lower', aspect='auto', cmap='gray_r', vmin=0)
ax2.set_title(f"Integrated Cell Probability ({Nx}x{Ny} = {Nx*Ny} Sub-Cells) [White = 0, Black = High]")
ax2.set_ylabel("Vertical Position $y$ (m)")
fig.colorbar(im_prob, ax=ax2, label="Probability per Cell")

# Subplot 3: Expectation Value Arc <x>(t), <y>(t)
t_traj = np.linspace(0, T_flight, 200)
x_traj = x0 + (px0 / m) * t_traj
y_traj = y0 + (py0 / m) * t_traj - 0.5 * g * t_traj**2
ax3.plot(x_traj, y_traj, 'r--', alpha=0.5, label="Classical Parabolic Trajectory")

(line_exp_path,) = ax3.plot([], [], 'b-', lw=2, label=r"Quantum Path $(\langle x \rangle, \langle y \rangle)$")
(point_exp,) = ax3.plot([], [], 'bo', markersize=8, label="Expectation Center")

ax3.set_xlim(0, x_grid[-1])
ax3.set_ylim(0, y_grid[-1])
ax3.set_xlabel("Horizontal Position $x$ (m)")
ax3.set_ylabel("Vertical Position $y$ (m)")
ax3.set_title(r"Dynamic Expectation Value $(\langle x \rangle(t), \langle y \rangle(t))$ in Motion")
ax3.legend(loc="upper right")
ax3.grid(True)

x_exp_hist, y_exp_hist = [], []

# ==========================================
# 3. EXACT TDSE SOLUTION & ANIMATION LOOP
# ==========================================
def evaluate_wavefunction(t):
    # Quantum dispersion factor (wavepacket spreading rate)
    tau = 2 * m * sigma0**2 / hbar
    s_t = sigma0 * (1 + 1j * (t / tau))
    
    # 1. Horizontal Motion: Free Quantum Gaussian Packet
    xc = x0 + (px0 / m) * t
    psi_x = (1.0 / (2 * np.pi * np.abs(s_t)**2)**0.25) * np.exp(
        -((X - xc)**2) / (4 * sigma0 * s_t) + 1j * px0 * (X - 0.5*(px0/m)*t) / hbar
    )
    
    # 2. Vertical Motion in Uniform Gravity + Hard-Wall Reflection
    yc_pos = y0 + (py0 / m) * t - 0.5 * g * t**2
    py_pos = py0 - m * g * t
    phase_pos = (py_pos * Y - (py0**2/(2*m) + m*g*y0)*t + 0.5*m*g*py0*t**2/m - (1/6)*m*g**2*t**3) / hbar
    psi_y_pos = np.exp(-((Y - yc_pos)**2) / (4 * sigma0 * s_t) + 1j * phase_pos)
    
    # Image wavepacket (-y0) enforcing Dirichlet boundary condition Psi(x,0,t) = 0
    yc_neg = -y0 - (py0 / m) * t + 0.5 * g * t**2
    py_neg = -py0 + m * g * t
    phase_neg = (py_neg * Y - (py0**2/(2*m) + m*g*y0)*t + 0.5*m*g*py0*t**2/m - (1/6)*m*g**2*t**3) / hbar
    psi_y_neg = np.exp(-((Y - yc_neg)**2) / (4 * sigma0 * s_t) + 1j * phase_neg)
    
    # Total Vertical Wavefunction (Incident minus Reflected Image)
    psi_y = psi_y_pos - psi_y_neg
    
    # Full 2D Spatial Wave Function
    Psi = psi_x * psi_y
    Psi[Y <= 0] = 0.0  # Impenetrable wall potential V(y<=0) = inf
    
    # L2 Normalization
    norm = np.sqrt(np.sum(np.abs(Psi)**2) * dx * dy)
    if norm > 0:
        Psi /= norm
    return Psi

def update(frame):
    t_val = (frame / 120) * T_flight
    Psi = evaluate_wavefunction(t_val)
    
    # Integrated Probability per Cell: P_ij = |Psi|^2 * dx * dy
    prob_density = np.abs(Psi)**2
    prob_cell = 0.25 * (prob_density[:-1, :-1] + prob_density[1:, :-1] + 
                        prob_density[:-1, 1:] + prob_density[1:, 1:]) * dx * dy
    
    # Calculate expectation values: <x> = sum(x_ij * P_ij), <y> = sum(y_ij * P_ij)
    exp_x = np.sum(X_mid * prob_cell)
    exp_y = np.sum(Y_mid * prob_cell)
    
    x_exp_hist.append(exp_x)
    y_exp_hist.append(exp_y)
    
    # Update visuals
    im_psi.set_data(np.real(Psi))
    im_psi.set_clim(vmin=np.min(np.real(Psi)), vmax=np.max(np.real(Psi)))
    
    im_prob.set_data(prob_cell)
    im_prob.set_clim(vmin=0, vmax=np.max(prob_cell))
    
    line_exp_path.set_data(x_exp_hist, y_exp_hist)
    point_exp.set_data([exp_x], [exp_y])
    
    return im_psi, im_prob, line_exp_path, point_exp

anim = FuncAnimation(fig, update, frames=120, interval=30, blit=False)
plt.tight_layout()
plt.show()