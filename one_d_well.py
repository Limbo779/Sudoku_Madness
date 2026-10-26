import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp
from scipy.constants import hbar

# 1. Symbolic definition
x, L, n, t, m = sp.symbols('x L n t m')
E_sym = (((hbar**2) * (sp.pi**2)) / (2 * m * (L**2))) * (n**2)
psi_sym = sp.sqrt(2 / L) * sp.sin(((n * sp.pi) / L) * x)

psi_func = sp.lambdify((x, n, L), psi_sym, 'numpy')
E_func = sp.lambdify((n, L, m), E_sym, 'numpy')

# 2. Parameters
N_val = 100
Length = 1.0
Mass = 10.0
fs = 0.001  # Bin width (fs)

# Spatial grid and bin midpoints
X = np.arange(0, Length + fs, fs)
dx = fs
X_mid = 0.5 * (X[:-1] + X[1:])

# Calculate wavefunction & energy
psi_spatial = psi_func(X, N_val, Length)
E_val = E_func(N_val, Length, Mass)
omega = E_val / hbar if E_val > 1e-30 else 2.0 * np.pi

# Compute integrated probability per bin: P_bin = integral_{x_i}^{x_{i+1}} |psi|^2 dx
# Scaled to Percentage (%) where sum over all bins = 100%
prob_density = np.abs(psi_spatial)**2
prob_bin_pct = 0.5 * (prob_density[:-1] + prob_density[1:]) * dx * 100.0

# 3. Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Plot 1: Time-dependent Wavefunction components
(line_real,) = ax1.plot(X, psi_spatial, label=r"$\text{Re}(\Psi(x,t))$", color="tab:blue")
(line_imag,) = ax1.plot(X, np.zeros_like(X), label=r"$\text{Im}(\Psi(x,t))$", color="tab:orange", linestyle="--")
ax1.set_ylabel(r"Wavefunction $\Psi(x,t)$")
ax1.set_ylim(-1.5 * np.max(psi_spatial), 1.5 * np.max(psi_spatial))
ax1.legend(loc="upper right")
ax1.grid(True)
ax1.set_title(f"Time Evolution & Integrated Bin Probability (n = {N_val}, bin width = {fs})")

# Plot 2: Integrated Bin Probability (%)
(line_prob,) = ax2.plot(X_mid, prob_bin_pct, color="tab:green", label=r"Bin Probability (%)")
ax2.set_xlabel("Position $x$")
ax2.set_ylabel("Probability per Bin (%)")
ax2.set_ylim(0, 1.2 * np.max(prob_bin_pct))  # Max peak is now ~0.2%
ax2.legend(loc="upper right")
ax2.grid(True)

def update(frame):
    t_val = frame * 0.05
    phase = np.exp(-1j * omega * t_val)
    psi_t = psi_spatial * phase
    
    # Update integrated bin probabilities vectorially
    p_dens = np.abs(psi_t)**2
    p_bin_pct = 0.5 * (p_dens[:-1] + p_dens[1:]) * dx * 100.0
    
    line_real.set_ydata(np.real(psi_t))
    line_imag.set_ydata(np.imag(psi_t))
    line_prob.set_ydata(p_bin_pct)
    return line_real, line_imag, line_prob

anim = FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.tight_layout()
plt.show()

print(np.matmul(X_mid,np.transpose(prob_bin_pct)))